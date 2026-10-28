"""Build four independent branding drafts; never edit home or collections."""
from pathlib import Path
import json,re,html
import pypdfium2 as pdf
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'sources/branding-round2.json'
data=json.loads(SOURCE.read_text())
asset_dir=ROOT/'assets/branding-round2';asset_dir.mkdir(exist_ok=True)
base=(ROOT/'projects/avioagroalliance/index.html').read_text()
header=re.search(r'<header.*?</header>',base,re.S).group()
cta=re.search(r'<section class="case-end-cta.*?</section>',base,re.S).group()
footer=re.search(r'<footer.*?</footer>',base,re.S).group()
e=html.escape
manifest=[]
for p in data['projects']:
 doc=pdf.PdfDocument(p['pdf']);slug=p['slug']
 def export(n,crop=None,hero=False):
  page=doc[n-1];im=page.render(scale=2400/page.get_width()).to_pil().convert('RGB')
  if crop:
   w,h=im.size;im=im.crop(tuple(round(v*(w if i%2==0 else h)) for i,v in enumerate(crop)))
  name=f'{slug}-hero.webp' if hero else f'{slug}-{n:02}.webp'
  out=asset_dir/name;im.save(out,'WEBP',quality=91,method=6)
  manifest.append(dict(asset=str(out.relative_to(ROOT)),source=p['pdf'],page=n,crop=crop,width=im.width,height=im.height))
  return f'/assets/branding-round2/{name}',im.size
 if p.get('application_hero'):
  hero='/' + p['application_hero']
  hero_size=Image.open(ROOT/p['application_hero']).size
 else:
  hero,hero_size=export(p['hero']['page'],p['hero'].get('crop'),True)
 allpages=sorted({n for s in p['sections'] for n in s['pages']})
 images={n:export(n) for n in allpages}
 facts='<dl class="project-overview-facts"><div><dt>Сфера</dt><dd>'+e(p['industry'])+'</dd></div><div class="scope-field"><dt>Моя работа</dt><dd><ul class="scope-list">'+''.join('<li>'+e(s)+'</li>' for s in p['scope'])+'</ul></dd></div><div><dt>Год</dt><dd>'+p['year']+'</dd></div></dl>'
 hero_html=f'<section class="brand-hero"><div class="wrap"><a class="back" href="/#works">Все проекты</a><div class="brand-hero-meta"><span>Брендинг · Визуальная система</span></div><h1>{e(p["name"])}</h1><div class="project-overview">{facts}<div class="project-overview-main"><div class="case-tags"><span class="tag">Айдентика</span><span class="tag">Логотип</span><span class="tag">Визуальная система</span></div><p>{e(p["summary"])}</p></div></div><img class="brand-hero-image" src="{hero}" width="{hero_size[0]}" height="{hero_size[1]}" alt="{e(p["name"])} — пример применения айдентики"></div></section>'
 sections=[]
 for i,s in enumerate(p['sections']):
  figures=[]
  for j,n in enumerate(s['pages']):
   src,(w,h)=images[n];wide=' brand-slide-wide' if len(s['pages'])%2 and j==0 else ''
   figures.append(f'<figure class="brand-slide{wide}"><img src="{src}" width="{w}" height="{h}" loading="lazy" alt="{e(p["name"])} — {e(s["title"])}, страница {n}"></figure>')
  sections.append(f'<section class="brand-section wrap"><div class="brand-section-heading"><span>{i+1:02} / {e(s["title"])}</span><div><h2>{e(s["title"])}</h2><p>{e(s["text"])}</p></div></div><div class="brand-gallery">'+''.join(figures)+'</div></section>')
 def application_section(app):
  w,h=Image.open(ROOT/app['asset']).size
  return f'<section class="brand-section wrap"><div class="brand-section-heading"><span>Визуализации применения</span><div><h2>{e(app["title"])}</h2><p>{e(app["text"])}</p></div></div><div class="brand-gallery"><figure class="brand-slide brand-slide-wide"><img src="/{app["asset"]}" width="{w}" height="{h}" loading="lazy" alt="{e(app["alt"])}"></figure></div></section>'
 if p.get('applications'):
  stationery,digital=p['applications']
  sections=[application_section(stationery),sections[0],application_section(digital),*sections[1:]]
 sections.insert(3 if p.get('applications') else 1,'<div class="review-mid-cta wrap">Есть похожая задача? <a href="https://t.me/kate_dash" target="_blank" rel="noopener">Написать в Telegram <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 19 19 5M8 5h11v11"/></svg></a></div>')
 head='<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><meta name="description" content="'+e(p['summary'])+'"><title>'+e(p['name'])+' — брендинг | Екатерина Дашкова</title>'+''.join(f'<link rel="stylesheet" href="/assets/{s}.css">' for s in ['style','yaeger-direction','portfolio-extensions','branding-story','case-system','branding-review'])+'</head>'
 folder=ROOT/'projects'/slug;folder.mkdir(exist_ok=True)
 (folder/'index.html').write_text(head+'<body class="brand-case branding-review">'+header+'<main>'+hero_html+''.join(sections)+cta+'</main>'+footer+'</body></html>')
(ROOT/'sources/branding-round2-assets.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
print(f'Created {len(data["projects"])} pages, {len(manifest)} assets')
