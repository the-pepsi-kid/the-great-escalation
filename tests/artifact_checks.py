"""Validate the delivered bytes, rather than only the authoring source."""
import base64,collections,json,pathlib,re,subprocess,sys,hashlib
from html.parser import HTMLParser
from pypdf import PdfReader
import jsonschema
ROOT=pathlib.Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'data/cards.json').read_text())
jsonschema.Draft202012Validator(json.loads((ROOT/'data/cards.schema.json').read_text())).validate(data)
checks=[]
def check(name,condition):
    assert condition,name;checks.append({'name':name,'pass':True})
class InspectHTML(HTMLParser):
    def __init__(self):super().__init__();self.ids=[];self.external=[];self.scripts=[];self.script=False;self.tables=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id'in a:self.ids.append(a['id'])
        for k in ['src','href']:
            if re.match(r'https?://',a.get(k,'')):self.external.append(a[k])
        if tag=='script':self.script=True;self.scripts.append('')
        if tag=='table':self.tables+=1
    def handle_endtag(self,tag):
        if tag=='script':self.script=False
    def handle_data(self,s):
        if self.script:self.scripts[-1]+=s
page=(ROOT/'index.html').read_text();parser=InspectHTML();parser.feed(page)
check('HTML static element IDs are unique',len(parser.ids)==len(set(parser.ids)))
check('HTML has no external script, stylesheet, image or link dependencies',not parser.external and not re.search(r'url\([\'\"]?https?://',page))
check('Eight manual tables and the complete engine example are embedded',parser.tables==8 and '431638' in page)
check('All build placeholders were substituted',not re.search(r'/\*__[A-Z]+__\*/',page))
check('All three embedded JavaScript blocks compile',len(parser.scripts)==3)
for i,source in enumerate(parser.scripts):
    p=subprocess.run(['node','-e',"const vm=require('node:vm');new vm.Script(require('node:fs').readFileSync(0,'utf8'));"],input=source,text=True,capture_output=True)
    check('Embedded JavaScript block '+str(i+1)+' compiles',p.returncode==0)
match=re.search(r'const DATA=(.*?); const ART=(.*?);</script>',page,re.S)
embedded=json.loads(match[1]);embedded_art=json.loads(match[2])
check('Offline HTML embeds exactly the current source-of-truth catalog',embedded==data)
check('All 110 actual illustration files match declared completion',len(embedded_art)==110 and sum(c['illustration']['status']!='pending' for c in data['cards'])==110)
check('Every card has a distinct written illustration scene',len({c['illustration']['brief'] for c in data['cards']})==110 and min(len(c['illustration']['brief']) for c in data['cards'])>65)
for c in data['cards']:
    check(c['id']+' asset state is honest',(ROOT/c['illustration']['path']).is_file()==(c['illustration']['status']!='pending'))
manifest=json.loads((ROOT/'art/generation_manifest.json').read_text())
check('110 individually generated source images recorded',len(manifest)==110)
check('110 different source image checksums',len({m['source_png_sha256']for m in manifest.values()})==110)
baseline=json.loads((ROOT/'data/gameplay_fingerprint.json').read_text())
check('Rules engine unchanged by the art update',hashlib.sha256((ROOT/'src/engine.js').read_bytes()).hexdigest()==baseline['engine_sha256'])
mechanics=[{k:v for k,v in c.items()if k!='illustration'}for c in data['cards']]
check('Every card mechanic unchanged by the art update',hashlib.sha256(json.dumps(mechanics,sort_keys=True).encode()).hexdigest()==baseline['mechanics_sha256'])
faces=PdfReader(ROOT/'print/Card_Faces_Bleed.pdf')
check('110 single-card PDF pages',len(faces.pages)==110)
image_hashes=set()
for card,p in zip(data['cards'],faces.pages):
    check(card['id']+' PDF contains its own text',card['id'] in p.extract_text())
    check(card['id']+' has poker-size trim and 0.125-inch bleed',list(map(float,p.mediabox))==[0,0,198,270] and list(map(float,p.trimbox))==[9,9,189,261] and list(map(float,p.bleedbox))==[0,0,198,270])
    images=[x.get_object()for x in p['/Resources'].get('/XObject',{}).values()if x.get_object().get('/Subtype')=='/Image']
    check(card['id']+' printable face contains one high-resolution illustration',len(images)==1 and int(images[0]['/Width'])>=1024)
    check(card['id']+' printable face has no art placeholder','ILLUSTRATION PENDING'not in p.extract_text())
    image_hashes.update(hashlib.sha256(x.get_data()).hexdigest()for x in images)
check('All 110 printable illustrations are distinct',len(image_hashes)==110)
check('Ten-page atlas contains every illustration',len(PdfReader(ROOT/'print/Full_Illustrated_Card_Atlas.pdf').pages)==10)
check('38 duplex pages and 19 front/back sheets',len(PdfReader(ROOT/'print/Print_Deck_Duplex_6up.pdf').pages)==38 and len(PdfReader(ROOT/'print/Print_Fronts_6up.pdf').pages)==19 and len(PdfReader(ROOT/'print/Print_Backs_6up.pdf').pages)==19)
check('Two distinct card back pages',len(PdfReader(ROOT/'print/Card_Backs_Bleed.pdf').pages)==2)
check('Full catalog workbook exported',(ROOT/'data/card_catalog.xlsx').is_file())
check('All 110 images are embedded as valid JPEG data',all(base64.b64decode(v.split(',',1)[1]).startswith(b'\xff\xd8') for v in embedded_art.values()))
result={'passed':len(checks),'total':len(checks),'checks':checks,'note':'Static artifact and PDF checks. These do not replace a live browser walkthrough.'}
(ROOT/'docs/artifact-results.json').write_text(json.dumps(result,indent=2))
print(f'{len(checks)}/{len(checks)} artifact checks passed. Live browser walkthrough remains unverified.')
