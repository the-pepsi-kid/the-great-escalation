"""Typeset the entire individual illustration collection, uncropped, with reliable labels."""
from pathlib import Path
import json,math,shutil
from reportlab import rl_config
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
rl_config.useA85=False
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT.parent/'outputs/great-escalation'
cards=json.loads((ROOT/'data/cards.json').read_text())['cards']
font=Path('/usr/share/fonts/truetype/open-sans')
pdfmetrics.registerFont(TTFont('AtlasBody',str(font/'OpenSans-Regular.ttf')))
pdfmetrics.registerFont(TTFont('AtlasDisplay',str(font/'OpenSans-CondBold.ttf')))
target=ROOT/'print/Full_Illustrated_Card_Atlas.pdf'
c=canvas.Canvas(str(target),pagesize=(612,792),pageCompression=1)
c.setTitle('The Great Escalation - Complete 110-Card Illustration Atlas')
c.setAuthor('The Great Escalation')
pages=math.ceil(len(cards)/12)
for page in range(pages):
    c.setFillColor(HexColor('#252824'));c.setFont('AtlasDisplay',24);c.drawString(32,756,'THE GREAT ESCALATION')
    c.setFont('AtlasBody',8);c.drawString(32,739,'COMPLETE ILLUSTRATION ATLAS / 110 INDIVIDUAL SCENES / ART REVISION 1')
    for index,card in enumerate(cards[page*12:(page+1)*12]):
        row,col=divmod(index,3);x=32+col*184;top=710-row*164
        style=ParagraphStyle('title',fontName='AtlasDisplay',fontSize=11.5,leading=12.7,textColor=HexColor('#252824'))
        title=Paragraph(card['name'].replace('&','&amp;'),style);w,h=title.wrap(176,32);title.drawOn(c,x,top-h)
        image_y=top-148;c.setStrokeColor(HexColor(card['color']));c.setLineWidth(2);c.line(x-4,image_y,x-4,image_y+117.33)
        c.drawImage(ImageReader(str(ROOT/card['illustration']['path'])),x,image_y,width=176,height=117.33,preserveAspectRatio=True,anchor='c')
        c.setFillColor(HexColor('#6c6b60'));c.setFont('AtlasBody',6.6);c.drawString(x,image_y-11,card['id']+' / '+card['category'])
    c.setStrokeColor(HexColor('#d4cebc'));c.setLineWidth(.4);c.line(32,38,580,38)
    c.setFillColor(HexColor('#6c6b60'));c.setFont('AtlasBody',7);c.drawString(32,24,'Every illustration is original to this project. Card rules are typeset separately.')
    c.drawRightString(580,24,f'{page+1} / {pages}');c.showPage()
c.save();shutil.copy2(target,OUT/target.name)
print(json.dumps({'atlas_pages':pages,'illustrations':len(cards),'file_MB':round(target.stat().st_size/1048576,2)}))
