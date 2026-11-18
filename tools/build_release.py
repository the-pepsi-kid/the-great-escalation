"""Build offline HTML, vector print proofs, manual and references from one catalog."""
import base64, html, json, math, pathlib, re, shutil
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab import rl_config
rl_config.useA85=False
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject
import jsonschema

ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT.parent/'outputs/great-escalation'
OUT.mkdir(parents=True,exist_ok=True)
QA=ROOT.parent/'tmp/qa';QA.mkdir(parents=True,exist_ok=True)
INK='#252824';PAPER='#f3eedf';RED='#943d34';TEAL='#377f79'
FONT=pathlib.Path('/usr/share/fonts/truetype/open-sans')
for name,file in [('Body','OpenSans-Regular.ttf'),('Bold','OpenSans-Bold.ttf'),('Italic','OpenSans-Italic.ttf'),('Display','OpenSans-CondBold.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(FONT/file)))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Italic',boldItalic='Bold')
data=json.loads((ROOT/'data/cards.json').read_text())
jsonschema.Draft202012Validator(json.loads((ROOT/'data/cards.schema.json').read_text())).validate(data)
cards=data['cards'];by_id={c['id']:c for c in cards}
def browser_art_path(card):
    web=ROOT/'art/web'/pathlib.Path(card['illustration']['path']).name
    return web if web.is_file() else ROOT/card['illustration']['path']
art={c['id']:'data:image/jpeg;base64,'+base64.b64encode(browser_art_path(c).read_bytes()).decode() for c in cards if (ROOT/c['illustration']['path']).exists()}

def blocks(md):
    lines=md.splitlines();out=[];i=0
    while i<len(lines):
        line=lines[i].strip()
        if not line or line.startswith('<!--'):i+=1;continue
        if line.startswith('|'):
            table=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                cells=[x.strip() for x in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r'[-: ]+',x) for x in cells):table.append(cells)
                i+=1
            out.append(('table',table));continue
        m=re.match(r'^(#{1,4}) (.+)',line)
        if m:out.append(('h'+str(len(m[1])),m[2]));i+=1;continue
        if re.match(r'^\d+\. ',line) or line.startswith('- '):
            ordered=bool(re.match(r'^\d+\. ',line));items=[]
            while i<len(lines) and ((bool(re.match(r'^\d+\. ',lines[i].strip())) if ordered else lines[i].strip().startswith('- '))):
                items.append(re.sub(r'^(\d+\. |- )','',lines[i].strip()));i+=1
            out.append(('ol' if ordered else 'ul',items));continue
        p=[line];i+=1
        while i<len(lines) and lines[i].strip() and not re.match(r'^(#|\||\d+\. |- |<!--)',lines[i].strip()):p.append(lines[i].strip());i+=1
        out.append(('p',' '.join(p)))
    return out
def inline(text):
    s=html.escape(text);s=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s);return s
def to_html(bs):
    s=[]
    for typ,val in bs:
        if typ=='table':s.append('<table><thead><tr>'+''.join('<th>'+inline(x)+'</th>' for x in val[0])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+inline(x)+'</td>' for x in row)+'</tr>' for row in val[1:])+'</tbody></table>')
        elif typ in ['ol','ul']:s.append('<'+typ+'>'+''.join('<li>'+inline(x)+'</li>' for x in val)+'</'+typ+'>')
        else:s.append('<'+typ+'>'+inline(val)+'</'+typ+'>')
    return ''.join(s)
manual=(ROOT/'docs/RULES.md').read_text().replace('<!--EXAMPLE-->',(ROOT/'docs/EXAMPLE_GAME.md').read_text())
(ROOT/'docs/RULES_COMPLETE.md').write_text(manual)
manual_blocks=blocks(manual)
font_css=''
for family,file in [('Escalation Sans','OpenSans-Regular.ttf'),('Escalation Condensed','OpenSans-CondBold.ttf')]:
    font_css+="@font-face{font-family:'"+family+"';src:url(data:font/ttf;base64,"+base64.b64encode((FONT/file).read_bytes()).decode()+") format('truetype');font-display:swap;}"
css=(ROOT/'src/style.css').read_text().replace('/*__FONTS__*/',font_css)
content=(ROOT/'src/template.html').read_text()
for marker,value in [('STYLE',css),('MANUAL','<article class="manual">'+to_html(manual_blocks)+'</article>'),('DATA',json.dumps(data,ensure_ascii=False).replace('</','<\\/')),('ART',json.dumps(art)),('ENGINE',(ROOT/'src/engine.js').read_text()),('APP',(ROOT/'src/app.js').read_text())]:
    content=content.replace('/*__'+marker+'__*/',value)
assert not re.search(r'/\*__[A-Z]+__\*/',content)
(ROOT/'index.html').write_text(content)
shutil.copy2(ROOT/'index.html',OUT/'The_Great_Escalation.html')

styles={
 'body':ParagraphStyle('body',fontName='Body',fontSize=9.2,leading=14,textColor=HexColor(INK),spaceAfter=8),
 'h1':ParagraphStyle('h1',fontName='Display',fontSize=39,leading=42,textColor=HexColor(RED),spaceAfter=18),
 'h2':ParagraphStyle('h2',fontName='Display',fontSize=22,leading=26,textColor=HexColor(INK),spaceBefore=18,spaceAfter=10,keepWithNext=True),
 'h3':ParagraphStyle('h3',fontName='Display',fontSize=16,leading=20,spaceBefore=12,spaceAfter=7,keepWithNext=True),
 'cell':ParagraphStyle('cell',fontName='Body',fontSize=8.0,leading=11,textColor=HexColor(INK)),
 'th':ParagraphStyle('th',fontName='Bold',fontSize=8.0,leading=11,textColor=HexColor(PAPER)),
}
def footer(c,doc):
    c.saveState();w,h=c._pagesize;c.setStrokeColor(HexColor('#d4cebc'));c.line(42,35,w-42,35);c.setFont('Body',7);c.setFillColor(HexColor('#6c6b60'));c.drawString(42,22,'THE GREAT ESCALATION / PLAYTEST 0.1.0');c.drawRightString(w-42,22,str(doc.page));c.restoreState()
def pdf_manual(bs,path):
    story=[]
    for typ,val in bs:
        if typ=='table':
            n=len(val[0]);widths={2:[135,393],3:[100,60,368],4:[45,105,310,68]}.get(n,[528/n]*n)
            if val[0][0]=='Round end':widths=[176]*3
            if val[0][0]=='Path':widths=[105,423]
            rows=[[Paragraph(inline(x),styles['th'] if i==0 else styles['cell']) for x in r] for i,r in enumerate(val)]
            table=Table(rows,colWidths=widths,repeatRows=1,hAlign='LEFT');table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor(INK)),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),('LINEBELOW',(0,0),(-1,-1),.4,HexColor('#d4cebc')),('ROWBACKGROUNDS',(0,1),(-1,-1),[HexColor('#f3eedf'),HexColor('#faf7ef')])]))
            story.extend([table,Spacer(1,10)])
        elif typ in ['ol','ul']:
            for idx,text in enumerate(val,1):story.append(Paragraph((str(idx)+'. ' if typ=='ol' else '- ')+inline(text),styles['body']))
        else:story.append(Paragraph(inline(val),styles.get(typ,styles['body'])))
    SimpleDocTemplate(str(path),pagesize=(612,792),rightMargin=42,leftMargin=42,topMargin=42,bottomMargin=50,title='The Great Escalation - Field Manual',author='The Great Escalation').build(story,onFirstPage=footer,onLaterPages=footer)
pdf_manual(manual_blocks,ROOT/'print/Field_Manual.pdf')

def para(text,size=8.0,leading=None,font='Body',color=INK):return Paragraph(inline(text),ParagraphStyle('p',fontName=font,fontSize=size,leading=leading or size*1.25,textColor=HexColor(color)))
layout_stats=[]
def draw_face(c,card,x=0,y=0):
    c.saveState();c.translate(x,y)
    c.setFillColor(HexColor(card['color']));c.rect(0,0,198,270,fill=1,stroke=0)
    c.setFillColor(HexColor(PAPER));c.rect(9,9,180,252,fill=1,stroke=0)
    c.setFillColor(HexColor(INK));c.setFont('Body',5.8);c.drawString(18,251,'THE GREAT ESCALATION');c.drawRightString(180,251,'ALPHA 0.1')
    title=para(card['name'],12,12.6,'Display');tw,th=title.wrap(137,40);title.drawOn(c,18,240-th)
    c.setFillColor(HexColor(card['color']));c.circle(174,232,9,stroke=0,fill=1);c.setFillColor(HexColor(PAPER));c.setFont('Bold',10);c.drawCentredString(174,228.4,str(card['effects'][0]['n'] if card['type']=='Incident' else card['cost']))
    f=para(card['flavor'],7.0,8.4,'Italic');fw,fh=f.wrap(162,100)
    r=para(card['rules_short'],8.0,10.0);rw,rh=r.wrap(162,200)
    restriction=para('Requires: '+card['restriction'],7.2,8.7,'Bold') if card['condition'] else None
    sh=restriction.wrap(162,100)[1]+4 if restriction else 0
    flavor_y=29
    rules_y=flavor_y+fh+10
    body_height=rh+sh
    art_bottom=rules_y+body_height+17
    art_top=236-th-7
    art_height=art_top-art_bottom
    if art_height<35:raise ValueError(f"Card text does not fit: {card['id']} art_height={art_height}")
    layout_stats.append({'id':card['id'],'art_height_pt':round(art_height,1),'rules_height_pt':rh,'font_pt':8.0})
    if card['id'] in art:
        img=ImageReader(str(ROOT/card['illustration']['path']));iw,ih=img.getSize();scale=max(162/iw,art_height/ih);ww,hh=iw*scale,ih*scale
        c.saveState();clip=c.beginPath();clip.rect(18,art_bottom,162,art_height);c.clipPath(clip,stroke=0,fill=0);c.drawImage(img,18+(162-ww)/2,art_bottom+(art_height-hh)/2,ww,hh);c.restoreState()
    else:
        c.setFillColor(HexColor('#e5decc'));c.rect(18,art_bottom,162,art_height,fill=1,stroke=0)
        c.setStrokeColor(HexColor('#d1c5ad'));c.setLineWidth(.35)
        for dx in range(0,163,9):c.line(18+dx,art_bottom,18+dx,art_top)
        for dy in range(0,int(art_height)+1,9):c.line(18,art_bottom+dy,180,art_bottom+dy)
        c.setFillColor(HexColor('#82765e'));c.setFont('Display',17);c.drawCentredString(99,art_bottom+art_height/2+2,card['id'].replace('TGE-',''))
        c.setFont('Body',5.5);c.drawCentredString(99,art_bottom+art_height/2-9,'ILLUSTRATION PENDING')
    bar_y=art_bottom-12;c.setFillColor(HexColor(card['color']));c.rect(18,bar_y,162,10,fill=1,stroke=0);c.setFillColor(HexColor(PAPER));c.setFont('Bold',5.3)
    label={'M':'MEDIA','D':'INFRASTRUCTURE','P':'POLITICAL / CORPORATE','C':'CONSPIRACY','H':'IT COUNTERMEASURE','W':'WILDCARD'}[card['category_code']]
    c.drawString(22,bar_y+3,label);c.drawRightString(176,bar_y+3,card['type'].upper())
    r.drawOn(c,18,rules_y+sh)
    if restriction:restriction.drawOn(c,18,rules_y)
    c.setStrokeColor(HexColor('#d4cebc'));c.setLineWidth(.4);c.line(18,flavor_y+fh+5,180,flavor_y+fh+5)
    f.drawOn(c,18,flavor_y)
    c.setFillColor(HexColor('#6c6b60'));c.setFont('Body',5.5);c.drawString(18,17,card['id']);c.drawRightString(180,17,'ROUND START' if card['type']=='Incident' else 'YOUR TURN / 1 ACTION')
    c.restoreState()

def draw_back(c,incident=False,x=0,y=0):
    c.saveState();c.translate(x,y);color=RED if incident else INK;c.setFillColor(HexColor(color));c.rect(0,0,198,270,fill=1,stroke=0)
    c.setStrokeColor(HexColor('#c2b083'));c.setLineWidth(1);c.rect(17,17,164,236,fill=0,stroke=1);c.rect(21,21,156,228,fill=0,stroke=1)
    c.setStrokeColor(Color(.85,.79,.64,alpha=.13));c.setLineWidth(.45)
    for i in range(29,175,12):c.line(i,29,i,241)
    for i in range(29,242,12):c.line(29,i,169,i)
    c.setFillColor(HexColor(PAPER));c.setFont('Display',15);c.drawCentredString(99,187,'THE GREAT');c.setFont('Display',31);c.drawCentredString(99,154,'ESCALATION')
    c.setFillColor(HexColor('#e2ac4a'));c.rect(82,109,8,17,fill=1,stroke=0);c.rect(95,109,8,26,fill=1,stroke=0);c.rect(108,109,8,38,fill=1,stroke=0)
    c.setFont('Body',7);c.setFillColor(HexColor(PAPER));c.drawCentredString(99,89,'INFRASTRUCTURE INCIDENT' if incident else 'ACTION / SUPPORT / NARRATIVE');c.setFont('Body',5.8);c.drawCentredString(99,55,'THE NETWORK IS STILL DOWN.');c.drawCentredString(99,43,'PLAYTEST EDITION 0.1.0')
    c.restoreState()

def boxes(path):
    reader=PdfReader(path);writer=PdfWriter()
    for page in reader.pages:
        page.trimbox=RectangleObject([9,9,189,261]);page.bleedbox=RectangleObject([0,0,198,270]);writer.add_page(page)
    writer.add_metadata({'/Title':'The Great Escalation - 110-card playtest faces','/Subject':'2.5 x 3.5 inch trim; 0.125 inch bleed; all 110 cards individually illustrated'})
    with open(path,'wb') as f:writer.write(f)
face_path=ROOT/'print/Card_Faces_Bleed.pdf'
c=canvas.Canvas(str(face_path),pagesize=(198,270),pageCompression=1)
for card in cards:draw_face(c,card);c.showPage()
c.save();boxes(face_path)
back_path=ROOT/'print/Card_Backs_Bleed.pdf';c=canvas.Canvas(str(back_path),pagesize=(198,270));draw_back(c);c.showPage();draw_back(c,True);c.showPage();c.save();boxes(back_path)

def cropmarks(c,x,y):
    c.saveState();c.setLineWidth(.35);c.setStrokeColor(HexColor('#333333'))
    for xx in [x+9,x+189]:
        for yy,d in [(y+9,-1),(y+261,1)]:c.line(xx,yy+d*3,xx,yy+d*7)
    for yy in [y+9,y+261]:
        for xx,d in [(x+9,-1),(x+189,1)]:c.line(xx+d*3,yy,xx+d*7,yy)
    c.restoreState()
def sheet_header(c,label,idx,total):
    c.setFillColor(HexColor(INK));c.setFont('Display',20);c.drawString(24,754,'THE GREAT ESCALATION');c.setFont('Body',8);c.drawRightString(588,757,f'{label} / SHEET {idx+1} OF {total}');c.setFont('Body',7.4);c.drawString(24,735,'PLAYTEST PROOF / 2.5 x 3.5 in trim / 0.125 in bleed / Print Actual size (100%)')
    c.setFont('Body',7);c.drawString(24,53,'110 individual illustrations complete. All 110 cards playable.');c.drawString(24,40,'Cut at the crop marks. Duplex long-edge. Proof the first front/back before printing all sheets.')
def draw_sheet(c,chunk,index,total,back=False):
    sheet_header(c,'BACK' if back else 'FRONT',index,total)
    for j,card in enumerate(chunk):
        row,col=divmod(j,3);x=9+(2-col if back else col)*198;y=126+(1-row)*270
        if back:draw_back(c,card['type']=='Incident',x,y)
        else:draw_face(c,card,x,y)
        cropmarks(c,x,y)
    c.showPage()
chunks=[cards[i:i+6] for i in range(0,len(cards),6)]
for filename,kind in [('Print_Fronts_6up.pdf','front'),('Print_Backs_6up.pdf','back'),('Print_Deck_Duplex_6up.pdf','duplex')]:
    c=canvas.Canvas(str(ROOT/'print'/filename),pagesize=(612,792),pageCompression=1)
    for i,chunk in enumerate(chunks):
        if kind!='back':draw_sheet(c,chunk,i,len(chunks))
        if kind!='front':draw_sheet(c,chunk,i,len(chunks),True)
    c.save()
samples=[by_id[id] for id in ['TGE-M01','TGE-D01','TGE-P01','TGE-C01','TGE-H01','TGE-W01']]
c=canvas.Canvas(str(ROOT/'print/Art_Style_Reference_6_Cards.pdf'),pagesize=(612,792));draw_sheet(c,samples,0,1);c.save()

reference='''# THE GREAT ESCALATION - TABLE REFERENCE

## A turn

Gain 3 Influence (+1 if Credibility 4+, -1 if Panic 12+). Draw 1. Take 2 actions. End when ready. Discard newest cards until hand size is 8.

| Basic action | Cost | Result |
| --- | --- | --- |
| Find Funding | 0 | Gain 2 Influence. |
| Repair | 1 | Repair 2. Restore 1 Stability. Verified work: +1 Accountability. Resolution: +1 Accountability, +1 Credibility, +1 more Stability. |
| Verify | 1 | Unknown real: +1 Accountability, +1 Credibility, Panic -1. Rumor: same reward, Panic -2; sponsor -1 Reach and +1 Blame; discard rumor. |
| Report | 1 | Real incident only. Gain 1 Reach + stored boost (maximum 5). Consume boost. Panic +1. |
| Monetize | 1 | Real incident and Panic 6+. Gain 2 Leverage; +1 Liability; Panic +1. |
| Reassure | 0 | Panic -2. Credibility +1. |

Every basic action also costs one action. Card Repair, Verify and Audit effects use the same normal rewards.

## Audit and containment

Audit issues in this order: oldest sponsored rumor, then Liability, then all report boost as one issue. Audited Liability becomes Blame and costs 1 Leverage and 1 Credibility. Any productive audit gives the actor 1 Accountability and 1 Credibility; replace verification rewards, do not add both. A shield blocks a whole audit or one theft/transfer automatically. Each separate card component still resolves.

Containment lasts through this round. The incident stays in play but causes no severity damage or round-end Panic. Maximum two supports; a third retires the oldest. Support triggers reset each own turn.

## Round end

Add uncontained real severity; damage = ceil(total / 4), +1 if Panic is already 12+. Reduce Stability. Then Panic rises by uncontained real count, maximum +3. If no real incidents remain, Stability +2 and Panic -2. Stability zero now: everyone loses. Otherwise after round 8 score, or reveal ceil(players / 2) new incidents and continue.

## Scoring and limits

| Path | Prestige |
| --- | --- |
| Restoration | 2 x Accountability + Credibility |
| Narrative | floor(5 x Reach / 2) + Credibility |
| Exploitation | max(0, 2 x Leverage + floor(Influence / 3) - 2 x Blame - Liability) |

Use only your highest lane. Ties: higher Credibility, then lower Blame + Liability, then shared victory. Influence cap 15, Credibility 6, Panic 18, Stability 24, Shields 3, boost 3. Severity cap 8. Accountability and Blame are durable. Real queue limit = players + 2. There is no rumor-slot cap.
'''
(ROOT/'docs/REFERENCE.md').write_text(reference)
pdf_manual(blocks(reference),ROOT/'print/Rules_Reference.pdf')

c=canvas.Canvas(str(ROOT/'print/Score_Trackers.pdf'),pagesize=(612,792));sheet_header(c,'PENCIL TRACKERS',0,1)
c.setFont('Body',9);c.drawString(28,699,'Use pencil to record values. Highest lane is your Prestige; do not add the lanes.')
for i in range(6):
    y=660-i*83;c.setStrokeColor(HexColor('#b8af9b'));c.rect(24,y-56,564,74,fill=0,stroke=1);c.setFont('Display',13);c.drawString(34,y,'INSTITUTION '+str(i+1)+'   _________________________');c.setFont('Body',8);c.drawString(34,y-17,'Influence _____   Credibility _____   Accountability _____   Reach _____   Leverage _____');c.drawString(34,y-32,'Liability _____   Blame _____   Shields _____   Boost _____   Supports __________________');c.drawString(34,y-46,'Restoration ________   Narrative ________   Exploitation ________   Prestige (highest) ________')
c.setFont('Display',13);c.drawString(28,122,'ROUND _____ / 8      PANIC _____ / 18      STABILITY _____ / 24');c.showPage();c.save()

json.dump({'cards':110,'illustrated':len(art),'pending_art':110-len(art),'minimum_art_height_pt':min(x['art_height_pt'] for x in layout_stats),'rules_font_pt':8.0,'trim_inches':[2.5,3.5],'bleed_inches':.125,'face_pages':len(PdfReader(face_path).pages),'duplex_pages':len(PdfReader(ROOT/'print/Print_Deck_Duplex_6up.pdf').pages),'manual_pages':len(PdfReader(ROOT/'print/Field_Manual.pdf').pages)},open(ROOT/'docs/print-validation.json','w'),indent=2)
for filename in ['Field_Manual.pdf','Print_Deck_Duplex_6up.pdf','Art_Style_Reference_6_Cards.pdf']:
    shutil.copy2(ROOT/'print'/filename,OUT/filename)
print(json.dumps({'html_MB':round((ROOT/'index.html').stat().st_size/1048576,2),'illustrated':len(art),'pending':110-len(art),'faces':110,'duplex_sheets':len(chunks),'manual_pages':len(PdfReader(ROOT/'print/Field_Manual.pdf').pages),'minimum_art_height_pt':min(x['art_height_pt'] for x in layout_stats)},indent=2))
