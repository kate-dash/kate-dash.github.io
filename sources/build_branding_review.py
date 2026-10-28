from pathlib import Path
import json,re,html
import pypdfium2 as pdf
from PIL import Image
R=Path('/Users/ekaterinazaitseva/Documents/Портфолио/github-pages-deploy')
D=Path('/Users/ekaterinazaitseva/Documents/Design')
A=R/'assets/branding-review';A.mkdir(exist_ok=True)
data=[
 dict(slug='unity-branding',name='Unity',pdf=str(D/'Unity/Unity brand/Unity Style 2024/Unity style_26.04.24.pdf'),year='2024',industry='Кэмп, школа и верёвочный парк на Бали',scope=['Логотип','Фирменный стиль','Гайдлайн','Дизайн лендинга'],hero=6,summary='Разработала айдентику Unity и дизайн лендинга. Объединила кэмп, школу и верёвочный парк в одну систему с изменяемым логотипом, яркой палитрой и набором тематических иконок.',sections=[
 ('Айдентика в действии','Система работает на разных масштабах: от небольшой маркировки на посуде до печатных материалов и наружной рекламы. Общий характер сохраняют крупная буква U, цвет и линейная графика.',[8,5,13]),
 ('Один бренд — несколько направлений','Развёрнутый логотип собирается из букв и иконок. Для Camp, Park и School меняются тематические элементы, а композиционный принцип остаётся общим. Компактные версии позволяют переносить знак на небольшие носители.',[3,4,7,9]),
 ('Цвет, шрифт и графика','В гайдлайне зафиксированы насыщенные цвета и типографика Lens Grotesk. Иконки могут работать внутри логотипа и как самостоятельные элементы: на одежде, плакатах и других материалах.',[2,10,11,12,14,15]),
 ],questions=['Подтвердить год дизайна лендинга: 2024 относится к версии стиля.','Уточнить, какие носители были реализованы, а какие остались визуализациями.']),
 dict(slug='svetlana-delle',name='Svetlana Delle',pdf=str(D/'Portfolio/Branding portfolio/Delle_Svetlana_Guideline.pdf'),year='Уточняется',industry='Личный бренд · голосовые и музыкальные практики',scope=['Логотип','Фирменный стиль','Гайдлайн','Дизайн лендинга'],hero=13,summary='Создала айдентику личного бренда Svetlana Delle и дизайн лендинга. Визуальную систему построила вокруг темы голоса: плавных градиентов, волн, кругов и выразительной типографики.',sections=[
 ('Личный бренд в коммуникации','Гайдлайн связывает печатные материалы, оформление публикаций и цифровые носители. Мягкие цветовые переходы и тонкая графика помогают сохранять узнаваемость при смене формата.',[7,12]),
 ('Имя, монограмма и печать','Для разных задач подготовлены несколько знаков: полное имя Svetlana Delle, монограмма YARA для музыкальных продуктов и печать. В руководстве объясняется, когда использовать каждый вариант и как сочетать знак с именем.',[3,4,5,6]),
 ('Голос как графический принцип','Волновые строки и круговые композиции отсылают к звуку. Палитра соединяет песочные и терракотовые оттенки с холодными фиолетовыми; градиенты продолжают идею перетекания. Для акцентов используется Bazaart, для текста — Gilroy Regular.',[8,9,10]),
 ],questions=['Уточнить год проекта.','Подтвердить, какие применения были выпущены.']),
 dict(slug='kosov-branding',name='Kosov Group',pdf=str(D/'Portfolio/Branding portfolio/Kosov group style 2 copy.pdf'),year='2022',industry='Девелопмент и работа с территориями',scope=['Логотип','Фирменный стиль','Гайдлайн','Арт-дирекшн сайта'],hero=7,summary='Разработала фирменный стиль Kosov Group вокруг идеи «Всё начинается с земли». Топографические линии, отпечаток пальца и знак плюса связывают землю, человека и разные направления компании.',sections=[
 ('Ландшафт как часть айдентики','Фотографии природных территорий становятся основой коммуникации. Поверх них работают топографические линии и сетка плюсов: графика связывает отдельные изображения в единую систему.',[4,8,5]),
 ('Земля и человек','В знаке соединены образы топографической карты и отпечатка пальца. Это поддерживает идею участия человека в развитии территории. Плюс объединяет направления деятельности компании.',[2,3]),
 ('Гибкая графическая система','Знак и название допускают разные взаимные положения. Паттерн существует в двух вариантах — линии и разметка: их можно использовать отдельно или сочетать в одной композиции.',[6,9]),
 ],questions=['Уточнить личное распределение работы над лендингом: ранее Екатерина указала арт-дирекшн совместно с дизайнером и верстальщиком.']),
 dict(slug='avioagroalliance-branding',name='АвиоАгроАльянс',pdf=str(D/'Portfolio/AAA_guidelines 1.pdf'),year='Уточняется',industry='Авиация и виноградарство',scope=['Фирменный стиль','Гайдлайн','Дизайн лендинга'],hero=9,summary='Разработала фирменный стиль на основе предоставленного логотипа. Градиенты неба, силуэт самолёта и линия полёта объединяют авиационное направление компании, деловые материалы и оформление винных этикеток.',sections=[
 ('От авиации до винной этикетки','Стиль показан на разных носителях: самолёте, печатных материалах, бейджах и бутылках вина. Один набор элементов позволяет связать разные направления компании.',[4,2,11]),
 ('Небо, силуэт и траектория','Основой стали градиенты, напоминающие восход и закат. Самолёт и белый след дополняют цветовые переходы. Для сдержанных носителей предусмотрено использование графики без градиентного фона.',[5,10]),
 ('Правила использования','Исходный логотип предоставил заказчик. В гайдлайне я определила его цветовые варианты и сочетания с фоном, описала применение шрифта Jost и подготовила систему деловых носителей.',[3,7]),
 ('Цифровое применение','В руководстве показано применение стиля на первом экране сайта: градиент, крупный заголовок и авиационная графика. Здесь представлен именно этот экран, а не полный макет лендинга.',[8]),
 ],questions=['Уточнить год проекта.','Уточнить описание бизнес-направлений компании и найти полный макет лендинга.'])
]
manifest=[]
for p in data:
 doc=pdf.PdfDocument(p['pdf']);pages=sorted(set([p['hero']]+[n for _,_,nums in p['sections'] for n in nums]))
 for n in pages:
  pg=doc[n-1];im=pg.render(scale=2200/pg.get_width()).to_pil().convert('RGB');out=A/f'{p["slug"]}-{n:02}.webp';im.save(out,'WEBP',quality=90,method=6)
  manifest.append(dict(asset=str(out.relative_to(R)),source=p['pdf'],page=n,width=im.width,height=im.height))
 # Complete PDF copy, kept local in sources for reproducible exports.

webdir=D/'Portfolio/Web-sites portfolio/Unity '
im=Image.open(webdir/'screencapture-unity-club-2026-02-09-17_42_09.png').convert('RGB');w,h=im.size
im.crop((0,0,w,1900)).resize((1800,round(1900*1800/w))).save(A/'unity-web-first.webp','WEBP',quality=90)
im=Image.open(webdir/'screencapture-unity-club-2026-02-09-17_42_09-2.png').convert('RGB');im.thumbnail((1800,3000));im.save(A/'unity-web-detail.webp','WEBP',quality=90)
manifest.extend([dict(asset='assets/branding-review/unity-web-first.webp',source=str(webdir/'screencapture-unity-club-2026-02-09-17_42_09.png'),region='Первый экран, y=0..1900; дизайн не изменён'),dict(asset='assets/branding-review/unity-web-detail.webp',source=str(webdir/'screencapture-unity-club-2026-02-09-17_42_09-2.png'))])
# Keep Delle page based on her PDF as requested; no additional web mockup.
old=(R/'projects/avioagroalliance/index.html').read_text()
header=re.search(r'<header.*?</header>',old,re.S).group()
cta=re.search(r'<section class="case-end-cta.*?</section>',old,re.S).group()
footer=re.search(r'<footer.*?</footer>',old,re.S).group()
esc=html.escape
for p in data:
 def figure(n,wide=False):
  asset=f'/assets/branding-review/{p["slug"]}-{n:02}.webp';im=Image.open(R/asset.lstrip('/'));return f'<figure class="brand-slide{ " brand-slide-wide" if wide else ""}"><img src="{asset}" width="{im.width}" height="{im.height}" loading="lazy" alt="{esc(p["name"])} — страница {n} гайдлайна"></figure>'
 meta=f'<dl class="project-overview-facts"><div><dt>Сфера</dt><dd>{esc(p["industry"])}</dd></div><div class="scope-field"><dt>Моя работа</dt><dd><ul class="scope-list">'+''.join(f'<li>{esc(s)}</li>' for s in p['scope'])+f'</ul></dd></div><div><dt>Год</dt><dd>{p["year"]}</dd></div></dl>'
 hero=f'<section class="brand-hero"><div class="wrap"><a href="/#works" class="back">Все проекты</a><div class="brand-hero-meta"><span>Фирменный стиль · Гайдлайн</span></div><h1>{esc(p["name"])}</h1><div class="project-overview">{meta}<div class="project-overview-main"><div class="case-tags"><span class="tag">Брендинг</span><span class="tag">Гайдлайн</span><span class="tag">Веб-дизайн</span></div><p>{esc(p["summary"])}</p></div></div><img class="brand-hero-image" src="/assets/branding-review/{p["slug"]}-{p["hero"]:02}.webp" alt="{esc(p["name"])} — применение айдентики"></div></section>'
 sections=[]
 for i,(title,body,nums) in enumerate(p['sections']):
  gallery=''.join(figure(n,len(nums)%2==1 and j==0) for j,n in enumerate(nums))
  sections.append(f'<section class="brand-section wrap"><div class="brand-section-heading"><span>{i+1:02} / {esc(title)}</span><div><h2>{esc(title)}</h2><p>{esc(body)}</p></div></div><div class="brand-gallery">{gallery}</div></section>')
 if p['slug']=='unity-branding':
  sections.append('<section class="brand-section wrap"><div class="brand-section-heading"><span>04 / Сайт</span><div><h2>Айдентика на сайте</h2><p>Разработала дизайн лендинга Unity. На первом экране и во внутренних блоках продолжается система бренда: насыщенные цвета, тематические иконки и фотографии жизни кэмпа. Ниже — два фрагмента существующего сайта.</p></div></div><div class="brand-gallery"><figure class="brand-slide brand-slide-wide"><img src="/assets/branding-review/unity-web-first.webp" loading="lazy" alt="Unity — первый экран сайта"></figure><figure class="brand-slide brand-slide-wide review-web-detail"><img src="/assets/branding-review/unity-web-detail.webp" loading="lazy" alt="Unity — блок о жизни в кэмпе и форма связи"></figure></div></section>')
 if p['slug']=='kosov-branding':
  sections.append('<section class="brand-section wrap"><div class="brand-section-heading"><span>04 / Сайт</span><div><h2>Продолжение стиля в вебе</h2><p>Айдентика стала основой сайта Kosov Group. Над сайтом работала в роли арт-директора вместе с дизайнером и верстальщиком. Макеты сайта и дополнительные материалы собраны в <a href="/projects/kosov/">основном кейсе Kosov Group</a>.</p></div></div></section>')
 # One calm mid-case contact.
 sections.insert(1,'<div class="review-mid-cta wrap">Есть похожая задача? <a href="https://t.me/kate_dash" target="_blank" rel="noopener">Написать в Telegram <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 19 19 5M8 5h11v11"/></svg></a></div>')
 head='<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><meta name="description" content="'+esc(p['summary'])+'"><title>'+esc(p['name'])+' — брендинг | Екатерина Дашкова</title>'+''.join(f'<link rel="stylesheet" href="/assets/{s}.css">' for s in ['style','yaeger-direction','portfolio-extensions','branding-story','case-system','branding-review'])+'</head>'
 target=R/'projects'/p['slug'];target.mkdir(exist_ok=True)
 (target/'index.html').write_text(head+'<body class="brand-case branding-review">'+header+'<main>'+hero+''.join(sections)+cta+'</main>'+footer+'</body></html>')
(R/'sources/branding-review.json').write_text(json.dumps({'status':'Прямые ссылки для проверки; не добавлять на главную до согласования','projects':data,'assets':manifest},ensure_ascii=False,indent=2))
print('Generated four review cases and',len(manifest),'assets')
