"""Build the shop-first home variant from the current published home page."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
HOME = (ROOT / 'index.html').read_text()

cards = {}
for match in re.finditer(r'<article class="y-project-item">.*?</article>', HOME, re.S):
    card = match.group()
    slug_match = re.search(r'href="/projects/([^/]+)/"', card)
    if not slug_match:
        raise ValueError('A project card has no case link')
    slug = slug_match.group(1)
    if slug in cards:
        raise ValueError(f'Duplicate project card: {slug}')
    cards[slug] = card

shops = ['capservice', 'snk', '0not1', 'yodometics']
multi = ['kilev-lab', 'iceflow', 'kosov', 'sananda', 'arhistratig']
remaining = [slug for slug in cards if slug not in shops + multi]
if len(cards) != 23 or len(remaining) != 14 or set(shops + multi + remaining) != set(cards):
    raise ValueError('The home page project list has changed; check the grouping')

start = HOME.index('      <!-- Project 01:')
end = HOME.index('    </main>', start)
body = ['      <div class="y-variant-label" role="heading" aria-level="3">Интернет-магазины</div>']
body.extend('      ' + cards[slug] for slug in shops)
body.append('      <div class="y-variant-label" role="heading" aria-level="3">Многостраничные сайты</div>')
body.extend('      ' + cards[slug] for slug in multi)
body.append('      <div id="extraProjects" style="display:none;flex-direction:column;gap:80px;">')
body.extend('        ' + cards[slug] for slug in remaining)
body.append('      </div>')
body.append('      <div class="y-more-wrap"><button class="y-more-btn" id="moreProjectsBtn" '
            'type="button" aria-controls="extraProjects" aria-expanded="false" '
            'onclick="toggleExtraProjects()">( + ОСТАЛЬНЫЕ ПРОЕКТЫ · ЕЩЁ 14 РАБОТ )</button></div>')

variant = HOME[:start] + '\n\n'.join(body) + '\n\n' + HOME[end:]
variant = variant.replace('</head>', '<meta name="robots" content="noindex,follow">'
                          '<link rel="stylesheet" href="/assets/shop-variant.css"></head>', 1)
variant = variant.replace("btn.textContent = '( — СКРЫТЬ ДОПОЛНИТЕЛЬНЫЕ ПРОЕКТЫ )';",
                          "btn.textContent = '( — СКРЫТЬ ОСТАЛЬНЫЕ ПРОЕКТЫ )';\n        btn.setAttribute('aria-expanded', 'true');")
variant = variant.replace("btn.textContent = '( + ПОКАЗАТЬ ВСЕ ПРОЕКТЫ · ЕЩЁ 13 РАБОТ )';",
                          "btn.textContent = '( + ОСТАЛЬНЫЕ ПРОЕКТЫ · ЕЩЁ 14 РАБОТ )';\n        btn.setAttribute('aria-expanded', 'false');")

target = ROOT / 'shops' / 'index.html'
target.parent.mkdir(exist_ok=True)
target.write_text(variant)
print(f'Built {target.relative_to(ROOT)}: {len(shops)} shops, {len(multi)} multipage, {len(remaining)} hidden')
