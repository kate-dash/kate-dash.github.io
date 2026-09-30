"""Rebuild the static portfolio from editable project text and prepared images."""
from html import escape
from pathlib import Path
import json

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
PROJECTS = json.loads((ROOT / "portfolio-content.json").read_text())
IMAGES = json.loads((ROOT / "image-sources.json").read_text())
BRANDING = json.loads((ROOT / "branding-stories.json").read_text())


def e(value):
    return escape(str(value), quote=True)


FAVICON = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='12' fill='%231b1d1b'/%3E%3Cpath d='M16 18h32v7H23v8h22v7H23v7h25v7H16z' fill='%23f3f5f0'/%3E%3C/svg%3E"
METRIKA_ID = 113051818
METRIKA_SCRIPT = f'''<!-- Yandex.Metrika counter -->
<script type="text/javascript">
    (function(m,e,t,r,i,k,a){{
        m[i]=m[i]||function(){{(m[i].a=m[i].a||[]).push(arguments)}};
        m[i].l=1*new Date();
        for (var j = 0; j < document.scripts.length; j++) {{if (document.scripts[j].src === r) {{ return; }} }}
        k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)
    }})(window, document,'script','https://mc.yandex.ru/metrika/tag.js?id={METRIKA_ID}', 'ym');
    ym({METRIKA_ID}, 'init', {{ssr:true, webvisor:true, clickmap:true, ecommerce:"dataLayer", referrer: document.referrer, url: location.href, accurateTrackBounce:true, trackLinks:true}});
</script>
<!-- /Yandex.Metrika counter -->'''
METRIKA_NOSCRIPT = (f'<noscript><div><img src="https://mc.yandex.ru/watch/{METRIKA_ID}" '
                    'style="position:absolute; left:-9999px;" alt=""></div></noscript>')


def head(title, description):
    return (f'<!doctype html><html lang="ru"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<meta name="theme-color" content="#1b1d1b">'
            f'<meta name="description" content="{e(description)}"><title>{e(title)}</title>'
            f'<link rel="icon" type="image/svg+xml" href="{FAVICON}">'
            f'<link rel="stylesheet" href="/assets/style.css">'
            f'<link rel="stylesheet" href="/assets/yaeger-direction.css">'
            f'<link rel="stylesheet" href="/assets/portfolio-extensions.css">'
            f'{METRIKA_SCRIPT}</head>')


def header(is_home=False):
    prefix = "#" if is_home else "/#"
    return (f'<header class="site-header wrap"><a class="brand" href="/">Екатерина<span>Зайцева</span></a>'
            f'<nav class="nav" aria-label="Основная навигация"><a href="{prefix}projects">Проекты</a>'
            f'<a href="{prefix}about">Обо мне</a></nav></header>')


def home():
    cards = []
    for i, p in enumerate(PROJECTS, 1):
        featured = " featured" if i <= 2 else ""
        branding = p["slug"] in BRANDING
        card_class = " brand-work" if branding else ""
        visual = (f'<img class="brand-cover" src="/assets/{e(p["slug"])}-cover.webp" alt="Превью проекта {e(p["title"])}" loading="lazy">'
                  if branding else
                  f'<div class="browser"><div class="browser-top"><i class="dot"></i><i class="dot"></i><i class="dot"></i></div>'
                  f'<img src="/assets/{e(p["slug"])}-cover.webp" alt="Превью проекта {e(p["title"])}" loading="lazy"></div>')
        cards.append(f'<a class="project-card{featured}{card_class}" href="/projects/{e(p["slug"])}/">'
                     f'<div class="project-info"><span>{i:02d} / {e(p["type"])}</span>'
                     f'<h3>{e(p["title"])} ↗</h3><p>{e(p["summary"])}</p>'
                     f'<span class="scope">{" · ".join(e(t) for t in p["tags"])}</span></div>'
                     f'<div class="project-visual" style="background:{e(p["color"])}">'
                     f'{visual}</div></a>')
    return (head("Екатерина Зайцева — дизайн сайтов", "Екатерина Зайцева — портфолио веб-дизайнера. Лендинги и многостраничные сайты.")
            + '<body class="home-page">' + header(True) + '<main>'
            + '<section class="hero wrap" id="hero"><div class="hero-art" aria-hidden="true">'
            + '<div class="hero-shot hero-shot-a"><img src="/assets/naglyadno-cover.webp" alt=""></div>'
            + '<div class="hero-shot hero-shot-b"><img src="/assets/oiva-cover.webp" alt=""></div></div>'
            + '<h1>ЕКАТЕРИНА<br>ЗАЙЦЕВА</h1><div class="hero-bottom"><p>Дизайнер сайтов. Проекты для цифровых продуктов, брендов и сервисов.</p>'
            + '<div class="hero-place"><span>Россия</span><span>(Веб-дизайнер)</span></div></div></section>'
            + '<section class="projects wrap" id="projects"><div class="works-heading"><h2>ПРОЕКТЫ</h2><div>'
            + f'<p>Сайты, лендинги и фирменные стили. Внутри кейсов — выбранные страницы, адаптивные версии, детали визуальной системы и истории проектов.</p><span>({len(PROJECTS)} проектов)</span>'
            + '</div></div><div class="project-list">' + ''.join(cards) + '</div></section>'
            + '<section class="about" id="about"><div class="wrap"><div class="about-lead">Я создаю сайты, в которых выразительный визуальный язык работает вместе с логикой продукта.</div>'
            + '<div class="about-content"><div class="eyebrow">(ОБО МНЕ)</div><div><p>Меня зовут Екатерина. Я работаю с цифровыми сервисами и разными темами: нахожу главное, выстраиваю сценарий страницы и превращаю интерфейсы, тексты и графику в цельную историю.</p>'
            + '<div class="about-services"><span>(ЧЕМ ЗАНИМАЮСЬ)</span><ul><li>Лендинги и сайты</li><li>Структура и прототипы</li><li>Визуальные системы</li><li>Адаптивный дизайн</li></ul></div>'
            + '<p>Мне близок дизайн, который помогает посетителю быстро разобраться в содержании. Тексты этого раздела пока черновые — позже здесь появится моя история и подход к работе.</p>'
            + '</div></div></div></section></main><footer class="footer wrap"><div><span>Есть идея для сайта?</span><strong>Давайте сделаем<br>её наглядной.</strong></div>'
            + '<div class="footer-bottom"><span>Екатерина Зайцева · 2026</span><a href="#hero">Наверх ↑</a></div></footer></body></html>')


def viewer(p, item, i):
    label = item["label"]
    mobile = item["mobile"]
    ident = f'view-{i}'
    frame_class = "phone" if mobile else "screen"
    top = '<div class="phone-top"></div>' if mobile else '<div class="screen-top"><i class="dot"></i><i class="dot"></i><i class="dot"></i></div>'
    body_class = "phone-body" if mobile else "screen-body"
    return (f'<section class="case-viewer"><div class="viewer-title"><h2>{e(label)}</h2><span>Прокрутите внутри макета ↓</span></div>'
            f'<div class="{frame_class}" id="{ident}">{top}<div class="{body_class}" tabindex="0" aria-label="Прокручиваемый макет: {e(p["title"])} — {e(label)}">'
            f'<img src="/assets/{e(item["asset"])}" alt="{e(p["title"])} — {e(label)}" width="{item["width"]}" height="{item["height"]}" loading="{ "eager" if i == 1 else "lazy" }"></div></div>'
            f'<div class="viewer-controls"><span>{e(label)} · {item.get("design_width", item["width"])} px</span><button class="expand" data-expand="{ident}" aria-expanded="false">Показать весь сайт</button></div></section>')


def branding_case(p, number, next_p):
    story = BRANDING[p['slug']]
    slug = p['slug']
    sections = []
    for section in story['sections']:
        figures = []
        for item in IMAGES[slug]:
            if item['group'] != section['group']:
                continue
            wide = ' brand-slide-wide' if item.get('wide') else ''
            figures.append(f'<figure class="brand-slide{wide}">'
                           f'<img src="/assets/{e(item["asset"])}" width="{item["width"]}" height="{item["height"]}" loading="lazy" alt="{e(p["title"])} — {e(item["label"])}">'
                           f'<figcaption>{e(item["label"])}</figcaption></figure>')
        sections.append(f'<section class="brand-section wrap"><div class="brand-section-heading">'
                        f'<span>{e(section["number"])} / {e(section["title"])}</span>'
                        f'<div><h2>{e(section["title"])}</h2><p>{e(section["text"])}</p></div></div>'
                        f'<div class="brand-gallery">{"".join(figures)}</div></section>')
    brand_head = head(f'{p["title"]} — брендинг в портфолио Екатерины Зайцевой', p['summary']).replace(
        '</head>', '<link rel="stylesheet" href="/assets/branding-story.css"></head>')
    return (brand_head + f'<body class="brand-case brand-{e(slug)}">' + header() + '<main>'
            + f'<section class="brand-hero"><div class="wrap"><a href="/#projects" class="back">← Все проекты</a>'
            + f'<div class="brand-hero-meta"><span>{number:02d} / {len(PROJECTS):02d}</span><span>{e(story["hero_label"])}</span></div>'
            + f'<h1>{e(p["title"])}</h1><p>{e(story["lead"])}</p>'
            + f'<img class="brand-hero-image" src="/assets/{e(slug)}-cover.webp" width="{955 if slug == "renom" else 1400}" height="{544 if slug == "renom" else 862}" alt="{e(p["title"])} — обложка проекта"></div></section>'
            + f'<section class="brand-intro wrap"><span>О проекте</span><p>{e(story["intro"])}</p></section>'
            + ''.join(sections)
            + f'<a class="next wrap" href="/projects/{e(next_p["slug"])}/"><span>Следующий проект</span><strong>{e(next_p["title"])} ↗</strong></a>'
            + '</main><footer class="footer wrap"><span>Портфолио · Екатерина Зайцева</span><span>2026</span></footer></body></html>')


def three_r_brandbook(p, images):
    story = (ROOT / '3r-branding-section.html').read_text()
    for group in ('identity', 'application'):
        figures = []
        for item in images:
            if item.get('kind') != 'guidebook' or item.get('group') != group:
                continue
            figures.append(f'<figure class="three-r-slide">'
                           f'<img src="/assets/{e(item["asset"])}" width="{item["width"]}" height="{item["height"]}" loading="lazy" alt="3R Agency — {e(item["label"])}">'
                           f'<figcaption>{e(item["label"])}</figcaption></figure>')
        story = story.replace('{{' + group.upper() + '}}', ''.join(figures))
    return story


def case(p, number):
    images = IMAGES[p["slug"]]
    next_p = PROJECTS[number % len(PROJECTS)]
    if p['slug'] in BRANDING:
        return branding_case(p, number, next_p)
    if p["slug"] == "naglyadno":
        story = (ROOT / "naglyadno-story.html").read_text()
        story = story.replace("{{NUMBER}}", f"{number:02d}").replace("{{TOTAL}}", f"{len(PROJECTS):02d}")
        story = story.replace("{{LANDING_VIEWERS}}", "".join(viewer(p, item, i) for i, item in enumerate(images, 1)))
        nag_head = head("Наглядно — лендинг, дашборд и визуальная серия для ВК", p["summary"]).replace(
            '</head>', '<link rel="stylesheet" href="/assets/naglyadno-story.css"></head>')
        return (nag_head
                + '<body class="naglyadno-story">' + header() + '<main>' + story
                + f'<a class="next wrap" href="/projects/{e(next_p["slug"])}/"><span>Следующий проект</span><strong>{e(next_p["title"])} ↗</strong></a>'
                + '</main><footer class="footer wrap"><span>Портфолио · Дизайн сайтов</span><span>2026</span></footer>'
                + '<script src="/assets/site.js"></script></body></html>')
    if p["slug"] == "snk":
        story = (ROOT / "snk-story.html").read_text()
        story = story.replace("{{NUMBER}}", f"{number:02d}").replace("{{TOTAL}}", f"{len(PROJECTS):02d}")
        for i, item in enumerate(images, 1):
            story = story.replace(f"{{{{VIEWER_{i}}}}}", viewer(p, item, i))
        snk_head = head("SNK — интернет-магазин с AI-косметологом", p["summary"]).replace(
            '</head>', '<link rel="stylesheet" href="/assets/snk-story.css"></head>')
        return (snk_head + '<body class="snk-story">' + header() + '<main>' + story
                + f'<a class="next wrap" href="/projects/{e(next_p["slug"])}/"><span>Следующий проект</span><strong>{e(next_p["title"])} ↗</strong></a>'
                + '</main><footer class="footer wrap"><span>Портфолио · Дизайн сайтов</span><span>2026</span></footer>'
                + '<script src="/assets/site.js"></script></body></html>')
    if p["slug"] == "capservice":
        story = (ROOT / "capservice-story.html").read_text()
        story = story.replace("{{NUMBER}}", f"{number:02d}").replace("{{TOTAL}}", f"{len(PROJECTS):02d}")
        for i, item in enumerate(images[:5], 1):
            story = story.replace(f"{{{{VIEWER_{i}}}}}", viewer(p, item, i))
        cap_head = head("CapService — сайт аренды кофемашин для бизнеса", p["summary"]).replace(
            '</head>', '<link rel="stylesheet" href="/assets/capservice-story.css"></head>')
        return (cap_head + '<body class="capservice-story">' + header() + '<main>' + story
                + f'<a class="next wrap" href="/projects/{e(next_p["slug"])}/"><span>Следующий проект</span><strong>{e(next_p["title"])} ↗</strong></a>'
                + '</main><footer class="footer wrap"><span>Портфолио · Дизайн сайтов</span><span>2026</span></footer>'
                + '<script src="/assets/site.js"></script></body></html>')
    if p["slug"] == "kilev-lab":
        story = (ROOT / "kilev-story.html").read_text()
        story = story.replace("{{NUMBER}}", f"{number:02d}").replace("{{TOTAL}}", f"{len(PROJECTS):02d}")
        for i, item in enumerate(images, 1):
            story = story.replace(f"{{{{VIEWER_{i}}}}}", viewer(p, item, i))
        kilev_head = head("Kilev Lab — сайт международного брендингового агентства", p["summary"]).replace(
            '</head>', '<link rel="stylesheet" href="/assets/kilev-story.css"></head>')
        return (kilev_head + '<body class="kilev-story">' + header() + '<main>' + story
                + f'<a class="next wrap" href="/projects/{e(next_p["slug"])}/"><span>Следующий проект</span><strong>{e(next_p["title"])} ↗</strong></a>'
                + '</main><footer class="footer wrap"><span>Портфолио · Дизайн сайтов</span><span>2026</span></footer>'
                + '<script src="/assets/site.js"></script></body></html>')
    if p["slug"] == "iceflow":
        story = (ROOT / "iceflow-story.html").read_text()
        story = story.replace("{{NUMBER}}", f"{number:02d}").replace("{{TOTAL}}", f"{len(PROJECTS):02d}")
        for i, item in enumerate(images, 1):
            story = story.replace(f"{{{{VIEWER_{i}}}}}", viewer(p, item, i))
        iceflow_head = head("Iceflow — сайт бренда напитков", p["summary"]).replace(
            '</head>', '<link rel="stylesheet" href="/assets/iceflow-story.css"></head>')
        return (iceflow_head + '<body class="iceflow-story">' + header() + '<main>' + story
                + f'<a class="next wrap" href="/projects/{e(next_p["slug"])}/"><span>Следующий проект</span><strong>{e(next_p["title"])} ↗</strong></a>'
                + '</main><footer class="footer wrap"><span>Портфолио · Дизайн сайтов</span><span>2026</span></footer>'
                + '<script src="/assets/site.js"></script></body></html>')
    tags = ''.join(f'<span class="tag">{e(t)}</span>' for t in p["tags"])
    website_images = [item for item in images if item.get('kind') != 'guidebook']
    views = ''.join(viewer(p, item, i) for i, item in enumerate(website_images, 1))
    is_three_r = p['slug'] == '3r-agency'
    extra_story = three_r_brandbook(p, images) if is_three_r else ''
    case_head = head(f'{p["title"]} — портфолио Екатерины Зайцевой', p["summary"])
    if is_three_r:
        case_head = case_head.replace('</head>', '<link rel="stylesheet" href="/assets/3r-story.css"></head>')
    body_class = ' class="three-r-story"' if is_three_r else ''
    return (case_head
            + f'<body{body_class}>' + header() + '<main><section class="case-hero wrap">'
            + f'<a href="/#projects" class="back">← Все проекты</a><h1>{e(p["title"])}</h1>'
            + f'<div class="case-summary"><div><div class="eyebrow">{number:02d} / {len(PROJECTS):02d} · {e(p["type"])}</div>'
            + f'<div class="case-tags">{tags}</div></div><p>{e(p["summary"])}</p></div></section>'
            + '<section class="case-display"><div class="display-heading"><span>Дизайн сайта</span><span>Выбранные страницы</span></div>'
            + f'<div class="case-viewers">{views}</div></section>' + extra_story
            + f'<section class="case-text wrap"><h2>О проекте</h2><div class="case-text-body"><p>{e(p["detail"])}</p></div></section>'
            + f'<a class="next wrap" href="/projects/{e(next_p["slug"])}/"><span>Следующий проект</span><strong>{e(next_p["title"])} ↗</strong></a>'
            + '</main><footer class="footer wrap"><span>Портфолио · Дизайн сайтов</span><span>2026</span></footer>'
            + '<script src="/assets/site.js"></script></body></html>')


(DIST / 'index.html').write_text(home().replace('</body>', METRIKA_NOSCRIPT + '</body>'))
for number, project in enumerate(PROJECTS, 1):
    directory = DIST / 'projects' / project['slug']
    directory.mkdir(parents=True, exist_ok=True)
    (directory / 'index.html').write_text(case(project, number).replace('</body>', METRIKA_NOSCRIPT + '</body>'))
print(f'Built {len(PROJECTS)} project pages')
