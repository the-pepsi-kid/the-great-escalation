"""Prepare individually generated art for print and offline delivery. No creative alterations."""
from pathlib import Path
from PIL import Image
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1]
records=json.loads(Path(sys.argv[1]).read_text())
manifest_path=ROOT/'art/generation_manifest.json'
manifest=json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
web=ROOT/'art/web';web.mkdir(exist_ok=True)
for rec in records:
    if not rec.get('source'):continue
    source=Path(rec['source']);dest=ROOT/'art'/(rec['id']+'.jpg')
    im=Image.open(source).convert('RGB');original=im.size
    if not dest.exists():
        im.thumbnail((1024,1024),Image.Resampling.LANCZOS)
        im.save(dest,quality=90,optimize=True)
    master=Image.open(dest).convert('RGB')
    thumb=master.copy();thumb.thumbnail((450,450),Image.Resampling.LANCZOS)
    thumb.save(web/(rec['id']+'.jpg'),quality=82,optimize=True)
    manifest[rec['id']]={'id':rec['id'],'name':rec['name'],'asset':'art/'+dest.name,'web_asset':'art/web/'+dest.name,'source_dimensions':list(original),'asset_dimensions':list(master.size),'source_png_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'asset_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'generation':'individual built-in image generation','status':'illustrated'}
manifest_path.write_text(json.dumps(manifest,indent=2))
print(json.dumps({'generated_assets_ingested':len(manifest),'art_files_now':len(list((ROOT/'art').glob('TGE-*.jpg'))),'ready_new_images':len(records)}))
