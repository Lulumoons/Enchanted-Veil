"""Rebuild index.html sections from products.py, keeping hero, editor's note, footer disclosure and JS untouched."""
import re
from products import LUXE, SECTIONS, AFFILIATE_TAG
ROMAN = "I II III IV V VI VII VIII IX X XI XII".split()
html = open("index.html", encoding="utf-8").read()

def card(i, it):
    asin, kind, title, desc = it
    return (f'<article class="card reveal"><div class="ph"><img src="assets/products/{asin}.jpg" alt="Product photo: {kind.lower()}" '
            f'loading="lazy" width="750" height="1000"><span class="num">{i:02d}</span></div><div class="cb"><span class="kind">{kind}</span>'
            f'<h3>{title}</h3><span class="rule"></span><p>{desc}</p><a class="btn" data-asin="{asin}" href="https://www.amazon.com/dp/{asin}" '
            f'target="_blank" rel="sponsored noopener">Discover on Amazon <span aria-hidden="true">&rarr;</span></a></div></article>')

def grid(items): return '<div class="grid">' + "".join(card(i+1, it) for i, it in enumerate(items)) + '</div>'

# Luxe grid
html = re.sub(r'(<section class="cat luxe" id="luxe">.*?</div>)<div class="grid">.*?</div></div></section>',
              lambda m: m.group(1) + grid(LUXE) + '</div></section>', html, count=1, flags=re.S)
# Chapter sections
secs = []
for n, s in enumerate(SECTIONS):
    plain = re.sub(r"&amp;", "&", s["title"])
    secs.append(f'<section class="cat {s["cls"]}" id="{s["id"]}"><div class="wrap">\n'
        f'<figure class="banner reveal"><img src="assets/{s["banner"]}" alt="Painted still life for {plain}" loading="lazy"><figcaption>'
        f'<span class="chapter">Chapter {ROMAN[n]}</span><h2>{s["title"]}</h2><span class="eyebrow">{s["eyebrow"]}</span></figcaption></figure>\n'
        f'<p class="lede reveal">{s["lede"]}</p>{grid(s["items"])}</div></section>')
start = html.index('<section class="cat t', html.index('id="note"'))
end = html.index('<footer>')
html = html[:start] + "\n".join(secs) + "\n\n" + html[end:]
# Nav (header + footer)
links = '<a href="#christmas">The Christmas Edit</a><a href="#luxe">The Luxe Collection</a>' + "".join(f'<a href="#{s["id"]}">{s["title"]}</a>' for s in SECTIONS)
HEADER = [("christmas","Christmas"),("luxe","The Luxe Collection"),("emeralds","Emeralds"),("rubies","Rubies"),("rare","Rare Treasures"),("pearls","Pearls"),("blue","Something Blue"),("tiaras","Bridal Pearls"),("honeymoon","Honeymoon")]
hlinks = "".join(f'<a href="#{i}">{t}</a>' for i, t in HEADER)
html = re.sub(r'(<header class="top"><a class="logo" href="#top">Enchanted Veil</a><nav>).*?(</nav>)', lambda m: m.group(1)+hlinks+m.group(2), html, flags=re.S)
html = re.sub(r'(<nav class="fnav">).*?(</nav>)', lambda m: m.group(1)+links+m.group(2), html, flags=re.S)
html = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="A romantic edit of fine bridal jewels: emeralds, rubies, pearls, sapphires, tiaras, cathedral veils and heirloom keepsakes.">', html)
html = re.sub(r'const AFFILIATE_TAG = "[^"]*";', f'const AFFILIATE_TAG = "{AFFILIATE_TAG}";', html)
open("index.html", "w", encoding="utf-8").write(html)
print("built", len(LUXE) + sum(len(s["items"]) for s in SECTIONS), "cards")
