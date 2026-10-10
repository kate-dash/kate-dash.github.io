"""Build shareable project collections from the current home-page cards."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
HOME = (ROOT / 'index.html').read_text()

cards = {}
for match in re.finditer(r'<article class="y-project-item">.*?</article>', HOME, re.S):
    card = match.group()
    link = re.search(r'href="/projects/([^/]+)/"', card)
    if not link:
        raise ValueError('A project card has no case link')
    slug = link.group(1)
    if slug in cards:
        raise ValueError(f'Duplicate project card: {slug}')
    if not (ROOT / 'projects' / slug / 'index.html').is_file():
        raise ValueError(f'Missing case page: {slug}')
    cards[slug] = card

# This case remains in the client collections and at its direct URL, but is
# intentionally absent from the home page until its presentation is ready.
hidden_card = (ROOT / 'sources' / 'life-revival-card.html').read_text().strip()
hidden_link = re.search(r'href="/projects/([^/]+)/"', hidden_card)
if not hidden_link or hidden_link.group(1) != 'life-revival':
    raise ValueError('Invalid hidden Life Revival card')
if 'life-revival' in cards:
    raise ValueError('Life Revival should be hidden from the home page')
ordered_cards = list(cards.items())
insert_at = next(index + 1 for index, (slug, _) in enumerate(ordered_cards) if slug == '3r-agency')
ordered_cards.insert(insert_at, ('life-revival', hidden_card))
cards = dict(ordered_cards)

if len(cards) != 24:
    raise ValueError(f'Expected 24 project cards, found {len(cards)}; review collections')

COLLECTIONS = {
    'shops': {
        'title': 'Интернет-магазины',
        'description': 'Интернет-магазины для кофе, косметики и одежды: каталог, карточки товаров, сценарии выбора и покупки.',
        'projects': ['capservice', 'snk', '0not1', 'yodometics'],
        'related_heading': 'Также многостраничные сайты',
        'related': ['kilev-lab', 'iceflow', 'kosov', 'sananda', 'arhistratig'],
    },
    'multipage': {
        'title': 'Многостраничные сайты',
        'description': 'Сайты с несколькими разделами и сценариями: услуги, продукты, проекты, каталог и личный кабинет.',
        'projects': ['kilev-lab', 'iceflow', 'kosov', 'sananda', 'arhistratig', 'capservice', 'snk'],
    },
    'landings': {
        'title': 'Продающие лендинги',
        'description': 'Посадочные страницы, которые объясняют продукт или услугу и ведут посетителя к целевому действию.',
        'projects': ['oiva', 'naglyadno', '3r-agency', 'life-revival', 'bali', 'wowflat', 'credu'],
    },
    'branding': {
        'title': 'Брендинг',
        'description': 'Логотипы, фирменный стиль и визуальные системы в цифровых и печатных материалах.',
        'projects': ['renom', 'status-compliance', 'avioagroalliance', '3r-agency', 'life-revival', 'kosov', 'credu'],
    },
    'real-estate': {
        'title': 'Недвижимость',
        'description': 'Сайты и визуальные концепции для девелопмента, продажи и аренды недвижимости.',
        'projects': ['bali', 'phuket', 'wowflat', 'kosov', 'phuket-simple'],
    },
}

start = HOME.index('      <!-- Project 01:')
end = HOME.index('    </main>', start)
function_re = re.compile(r'    function toggleExtraProjects\(\) \{.*?\n    \}', re.S)

for route, data in COLLECTIONS.items():
    primary = data['projects']
    related = data.get('related', [])
    featured = primary + related
    if len(featured) != len(set(featured)) or not set(featured) <= set(cards):
        raise ValueError(f'Invalid project list for {route}')
    remaining = [slug for slug in cards if slug not in featured]

    content = ['      ' + cards[slug] for slug in primary]
    if related:
        content.append(
            '      <div class="y-collection-group-label" role="heading" aria-level="3">'
            + data['related_heading'] + '</div>'
        )
        content.extend('      ' + cards[slug] for slug in related)
    content.append('      <div id="extraProjects" style="display:none;flex-direction:column;gap:80px;">')
    content.extend('        ' + cards[slug] for slug in remaining)
    content.append('      </div>')
    content.append(
        '      <div class="y-more-wrap"><button class="y-more-btn" id="moreProjectsBtn" '
        'type="button" aria-controls="extraProjects" aria-expanded="false" '
        'onclick="toggleExtraProjects()">'
        f'( + ОСТАЛЬНЫЕ ПРОЕКТЫ · ЕЩЁ {len(remaining)} РАБОТ )'
        '</button></div>'
    )

    page = HOME[:start] + '\n\n'.join(content) + '\n\n' + HOME[end:]
    page = page.replace(
        '<title>Екатерина Дашкова — Дизайн сайтов & UI/UX</title>',
        f'<title>{data["title"]} — проекты Екатерины Дашковой</title>'
        f'<meta name="description" content="{data["description"]}">',
        1,
    )
    page = page.replace(
        '<div class="y-works-hero-title">\n        <h2>WORKS</h2>',
        f'<div class="y-works-hero-title y-collection-title">\n        <h2>{data["title"]}</h2>',
        1,
    )
    page, desc_count = re.subn(
        r'(<div class="y-works-hero-desc">\s*<p>).*?(</p>)',
        lambda match: match.group(1) + data['description'] + match.group(2),
        page,
        count=1,
        flags=re.S,
    )
    if desc_count != 1:
        raise ValueError('Could not replace collection intro')
    page = page.replace(
        f'href="/{route}/">{data["title"]}</a>',
        f'href="/{route}/" aria-current="page">{data["title"]}</a>',
        1,
    )
    function = (
        '    function toggleExtraProjects() {\n'
        '      var box = document.getElementById("extraProjects");\n'
        '      var btn = document.getElementById("moreProjectsBtn");\n'
        '      var expanded = btn.getAttribute("aria-expanded") === "true";\n'
        '      box.style.display = expanded ? "none" : "flex";\n'
        '      btn.setAttribute("aria-expanded", String(!expanded));\n'
        '      btn.textContent = expanded\n'
        f'        ? "( + ОСТАЛЬНЫЕ ПРОЕКТЫ · ЕЩЁ {len(remaining)} РАБОТ )"\n'
        '        : "( — СКРЫТЬ ОСТАЛЬНЫЕ ПРОЕКТЫ )";\n'
        '    }'
    )
    page, function_count = function_re.subn(function, page, count=1)
    if function_count != 1:
        raise ValueError('Could not replace the project toggle function')

    target = ROOT / route / 'index.html'
    target.parent.mkdir(exist_ok=True)
    target.write_text(page)
    print(f'{route}/: {len(primary)} matching, {len(related)} related, {len(remaining)} hidden')
