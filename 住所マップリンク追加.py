"""v7.html 内の全住所に Google Maps リンクを挿入する（idempotent）。"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path

PATH = Path(r'C:/Users/kyosu/worldカップ旅行/travel-guide-v7.html')
html = PATH.read_text(encoding='utf-8')

# 1. CSS 追加（一度だけ）
MAP_CSS = '''.map-link{display:inline-flex;align-items:center;gap:3px;margin-left:6px;padding:2px 8px;font-size:10.5px;text-decoration:none;background:#fff;border:1px solid var(--border);border-radius:4px;color:var(--primary);vertical-align:baseline;transition:.15s;font-family:var(--font-mono);font-weight:600;letter-spacing:.02em;white-space:nowrap}
.map-link:hover{background:var(--primary);color:#fff;text-decoration:none;border-color:var(--primary)}
.info .val .map-link,.tl-body .d .map-link{margin-left:8px}
'''
if '.map-link{' not in html:
    html = html.replace('</style>', MAP_CSS + '\n</style>', 1)

# 2. 住所 → Google Maps クエリ
ADDRESSES = [
    # NYC
    ('1535 Broadway, New York, NY 10036',                     '1535+Broadway+New+York+NY+10036'),
    ('1535 Broadway, NY 10036',                               'Marriott+Marquis+1535+Broadway+New+York'),
    ('225 W 35th St',                                         'Best+Bagel+Coffee+225+W+35th+St+New+York'),
    ('1 W 72nd St, New York, NY 10023',                       'Dakota+Building+1+W+72nd+St+New+York'),
    ('377 Greenwich St, NY 10013',                            'Locanda+Verde+377+Greenwich+St+New+York'),
    ('39-21 Washington St, Brooklyn, NY 11201',               'Manhattan+Bridge+View+DUMBO+Brooklyn+NY'),
    ('263 Mulberry St',                                       'Old+St+Patricks+Cathedral+263+Mulberry+St+New+York'),
    ('176½ Mulberry St',                                      'Mulberry+Street+Bar+176+Mulberry+New+York'),
    ('128 Mott Street',                                       '128+Mott+St+New+York+NY'),
    ('137 Mott Street',                                       '137+Mott+St+New+York+NY'),
    # Dallas / Arlington
    ('1500 Nolan Ryan Expressway, Arlington, TX 76011',       'Courtyard+Arlington+1500+Nolan+Ryan+Expressway'),
    ('2201 E Road to Six Flags St, Arlington, TX 76011',      'Six+Flags+Over+Texas+Arlington'),
    ('1800 E Lamar Blvd, Arlington, TX 76006',                'Hurricane+Harbor+Arlington+Texas'),
    ('1304 E Copeland Rd, Arlington, TX 76011',               'Pappadeaux+1304+E+Copeland+Rd+Arlington'),
    ('1 AT&amp;T Way, Arlington, TX',                         'AT%26T+Stadium+Arlington+TX'),
    ('1 AT&T Way, Arlington, TX',                             'AT%26T+Stadium+Arlington+TX'),
    # Anaheim / LA
    ('1420 S Harbor Blvd, Anaheim, CA 92802',                 'Courtyard+Anaheim+Theme+Park+Entrance+1420+S+Harbor+Blvd'),
    ('4100 Admiralty Way, Marina del Rey, CA 90292',          'Marriott+Marina+del+Rey+4100+Admiralty+Way'),
    ('3240 Washington Blvd, Marina Del Rey, CA 90292',        'Enterprise+Rent-A-Car+3240+Washington+Blvd+Marina+del+Rey'),
    # LA ドライブ
    ('6801 Hollywood Blvd',                                   'Hollywood+Walk+of+Fame+Ovation+Hollywood'),
    ('6925 Hollywood Blvd',                                   'TCL+Chinese+Theatre+6925+Hollywood+Blvd'),
    ('7009 Sunset Blvd',                                      'In-N-Out+Burger+Hollywood+7009+Sunset+Blvd'),
    ('189 The Grove Dr',                                      'The+Grove+189+The+Grove+Dr+Los+Angeles'),
    ('2800 E Observatory Rd',                                 'Griffith+Observatory+2800+E+Observatory+Rd'),
    ('4100 Inglewood Blvd',                                   'Costco+Marina+Marketplace+4100+Inglewood+Blvd'),
    ('523 Washington Blvd',                                   'Killer+Shrimp+523+Washington+Blvd+Marina+del+Rey'),
    # timeline 内の短いLocanda住所
    ('377 Greenwich St · The Greenwich Hotel',                '377+Greenwich+St+Tribeca+New+York'),
]

def insert_map_link(html, address, query):
    """idempotent: 既に直後にmap-link が無い箇所だけに挿入する。"""
    link = f' <a class="map-link" href="https://maps.google.com/?q={query}" target="_blank" rel="noopener">📍 Maps</a>'
    out = []
    i = 0
    replaced = 0
    while True:
        idx = html.find(address, i)
        if idx < 0:
            out.append(html[i:])
            break
        end = idx + len(address)
        lookahead = html[end:end+40]
        out.append(html[i:end])
        if '<a class="map-link"' not in lookahead:
            out.append(link)
            replaced += 1
        i = end
    return ''.join(out), replaced

total = 0
for addr, q in ADDRESSES:
    html, n = insert_map_link(html, addr, q)
    if n:
        print(f'  +{n}  {addr[:60]}')
        total += n

PATH.write_text(html, encoding='utf-8')
print(f'\n=== {total} links inserted ===')
