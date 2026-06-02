"""v7.html の目的地名（Dakota House 等）にも Google Maps リンクを追加。"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path

PATH = Path(r'C:/Users/kyosu/worldカップ旅行/travel-guide-v7.html')
html = PATH.read_text(encoding='utf-8')

# 目的地名 -> Google Mapsクエリ
DESTINATIONS = [
    # === NYC ===
    ('🎸 Dakota House（ダコタハウス）',         'Dakota+Building+1+W+72nd+St+New+York'),
    ('🍓 Strawberry Fields（ストロベリーフィールズ）', 'Strawberry+Fields+Central+Park+New+York'),
    ('🗻 Top of the Rock',                     'Top+of+the+Rock+Observation+Deck+New+York'),
    ('🛍️ FAO Schwarz（FAOシュワルツ）',         'FAO+Schwarz+Rockefeller+Center+New+York'),
    ('🗽 自由の女神 クラウン集合',              'Statue+of+Liberty+New+York'),
    ('🏝️ Ellis Island（エリス島・移民博物館）', 'Ellis+Island+National+Monument+New+York'),
    ('🍝 Locanda Verde（ロカンダ・ヴェルデ）',  'Locanda+Verde+377+Greenwich+St+New+York'),
    ('🎬 DUMBO 映画聖地',                       'DUMBO+Brooklyn+New+York'),
    ("🏛️ Old St. Patrick's Cathedral（旧セント・パトリック大聖堂）", 'Old+St+Patricks+Cathedral+263+Mulberry+St'),
    ('🍷 Mulberry Street Bar（外観のみ）',      'Mulberry+Street+Bar+176+Mulberry+New+York'),
    ('🐉 Chinatown（チャイナタウン）通過のみ',  'Chinatown+New+York+Canal+Street'),
    ('🥯 恭祐 単独ミッション：Best Bagel &amp; Coffee 調達', 'Best+Bagel+Coffee+225+W+35th+St+New+York'),

    # === Dallas / Arlington ===
    ('🎢 Six Flags Over Texas 入園',            'Six+Flags+Over+Texas+Arlington'),
    ('🎢 Tormenta Rampaging Run',               'Six+Flags+Over+Texas+Arlington'),
    ('🌊 Hurricane Harbor 入園',                'Hurricane+Harbor+Arlington+Texas'),
    ('🦐 Pappadeaux Seafood Kitchen',           'Pappadeaux+Seafood+Kitchen+Arlington'),
    ('🏟️ スタジアム入場開始',                   'AT%26T+Stadium+Arlington+TX'),
    ('🏈 自由時間（Globe Life Field 外観など）', 'Globe+Life+Field+Arlington+TX'),

    # === Disneyland ===
    ('🏰 開園ダッシュ',                         'Disneyland+Park+Anaheim'),

    # === LA Range Rover Day ===
    ('🌟 Hollywood Walk of Fame（ハリウッド殿堂）', 'Hollywood+Walk+of+Fame+Los+Angeles'),
    ('🎬 TCL Chinese Theatre（手形・足型）',     'TCL+Chinese+Theatre+Hollywood'),
    ('🎬 Hollywood Sign ビューポイント',         'Hollywood+Sign+Los+Angeles'),
    ('🍔 ランチ：In-N-Out Hollywood',            'In-N-Out+Burger+Hollywood+Sunset+Blvd'),
    ('🛍️ The Grove（ショッピング）',            'The+Grove+Los+Angeles'),
    ('🔭 Griffith Observatory（グリフィス天文台）', 'Griffith+Observatory+Los+Angeles'),
    ('🛒 Costco Marina Marketplace（お土産爆買い）', 'Costco+Marina+del+Rey+4100+Inglewood'),
    ('🦐 Killer Shrimp（ディナー・徒歩5分）',   'Killer+Shrimp+Marina+del+Rey'),

    # === 空港 ===
    ('✈️ JFK 到着',                             'JFK+Airport+New+York'),
    ('✈️ UA1331 EWR → DFW 出発',                'Newark+Liberty+International+Airport'),
    ('🛬 DFW 到着（CT時間）',                   'Dallas+Fort+Worth+Airport'),
    ('🛄 DAL 着・チェックイン',                 'Dallas+Love+Field+Airport'),
    ('🛬 SNA 到着（PDT 太平洋時間）',           'John+Wayne+Airport+Orange+County'),
    ('🛄 LAX 着・チェックイン',                 'LAX+Los+Angeles+International+Airport'),

    # === ホテル（ラベル）===
    ('🏨 Marriott Marquis チェックイン',        'New+York+Marriott+Marquis+1535+Broadway'),
    ('🏨 Courtyard Anaheim チェックイン',       'Courtyard+Anaheim+Theme+Park+Entrance'),
]

def insert_map_link(html, anchor, query):
    """idempotent: anchor 直後に map-link が無ければ挿入する。"""
    link = f' <a class="map-link" href="https://maps.google.com/?q={query}" target="_blank" rel="noopener">📍 Maps</a>'
    out = []
    i = 0
    replaced = 0
    while True:
        idx = html.find(anchor, i)
        if idx < 0:
            out.append(html[i:])
            break
        end = idx + len(anchor)
        lookahead = html[end:end+40]
        out.append(html[i:end])
        if '<a class="map-link"' not in lookahead:
            out.append(link)
            replaced += 1
        i = end
    return ''.join(out), replaced

total = 0
missing = []
for name, q in DESTINATIONS:
    html, n = insert_map_link(html, name, q)
    if n:
        print(f'  +{n}  {name[:55]}')
        total += n
    else:
        missing.append(name)

PATH.write_text(html, encoding='utf-8')
print(f'\n=== {total} links inserted ===')
if missing:
    print(f'(未検出 {len(missing)}件 = 既にリンク済 or 文字列不一致)')
    for m in missing[:5]:
        print(f'  - {m[:60]}')
