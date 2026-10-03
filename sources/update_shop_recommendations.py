"""Show related stores at the end of each e-commerce case."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SHOPS = [
    ('capservice', 'KAP Service'),
    ('snk', 'SNK'),
    ('0not1', '0not1 / Zero Not One'),
    ('yodometics', 'Yodometics'),
]

for slug, _ in SHOPS:
    path = ROOT / 'projects' / slug / 'index.html'
    html = path.read_text()
    links = ''.join(
        f'<a href="/projects/{other_slug}/">{name}'
        '<svg viewBox="0 0 24 24" aria-hidden="true">'
        '<path d="M5 19 19 5M8 5h11v11"/></svg></a>'
        for other_slug, name in SHOPS if other_slug != slug
    )
    block = (
        '<nav class="shop-recommendations wrap" aria-label="Другие интернет-магазины">'
        '<h2>Другие интернет-магазины</h2>'
        f'<div class="shop-recommendations-links">{links}</div>'
        '<a class="shop-recommendations-back" href="/shops/#works">'
        'Вся подборка магазинов</a></nav>'
    )
    html, count = re.subn(
        r'<a class="next wrap" href="/projects/[^/]+/">.*?</a>(?=</main>)',
        block,
        html,
        count=1,
        flags=re.S,
    )
    if count != 1:
        raise ValueError(f'Could not replace next-project link in {path}')
    path.write_text(html)
    print(f'Updated {path.relative_to(ROOT)}')
