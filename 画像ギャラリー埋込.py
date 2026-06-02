"""v7.html の各日ページに「📸 本日のスポット」画像ギャラリーを挿入。"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path

PATH = Path(r'C:/Users/kyosu/worldカップ旅行/travel-guide-v7.html')
html = PATH.read_text(encoding='utf-8')

# ========= CSS（一度だけ追加）=========
GALLERY_CSS = '''
/* ============ PLACE GALLERY ============ */
.place-gallery{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin:14px 0 24px}
.place-card{margin:0;background:var(--card);border:1px solid var(--border);border-radius:10px;overflow:hidden;box-shadow:var(--shadow-sm);transition:.2s;display:flex;flex-direction:column}
.place-card:hover{transform:translateY(-2px);box-shadow:var(--shadow)}
.place-card img{width:100%;aspect-ratio:4/3;object-fit:cover;display:block;background:var(--border-l)}
.place-card figcaption{padding:10px 12px;display:flex;flex-direction:column;gap:2px}
.place-card figcaption strong{font-family:var(--font-serif);font-size:14px;color:var(--primary);font-weight:700;line-height:1.3}
.place-card figcaption span.jp{font-size:11.5px;color:var(--ink-l);line-height:1.5}
.place-card figcaption span.tag{font-family:var(--font-mono);font-size:10px;color:var(--accent);letter-spacing:.08em;margin-top:4px;font-weight:600}
.place-card.wide{grid-column:span 2}
@media(max-width:700px){.place-card.wide{grid-column:span 1}}
'''
if '.place-gallery{' not in html:
    html = html.replace('</style>', GALLERY_CSS + '\n</style>', 1)
    print('+ CSS injected')

# ========= 各日に挿入するギャラリー =========
GALLERIES = {
    'd11': ('📸 本日のスポット', [
        ('central-park.jpg',      'Dakota House',            'ダコタハウス（ジョン・レノン住居）', '⭐ Tier 1'),
        ('strawberry-fields.jpg', 'Strawberry Fields',       'ストロベリーフィールズ（IMAGINEの追悼園）', '⭐ Tier 1'),
        ('top-of-rock.jpg',       'Top of the Rock',         '30 Rockefeller Plaza（展望台）', 'Tier 2'),
        ('times-square.jpg',      'Times Square',            'タイムズスクエア（ホテル目の前）', 'BONUS'),
    ]),
    'd12': ('📸 本日のスポット（De Niro DAY）', [
        ('bagel.jpg',             'Best Bagel & Coffee',     '朝食テイクアウト（徒歩8分）', '🥯 朝食'),
        ('statue-of-liberty.jpg', '自由の女神 Crown Access', 'Crown までの354段を登頂', '🗽 10:00'),
        ('ellis-island.jpg',      'Ellis Island',            'アメリカ移民博物館', '🏝️ 12:00'),
        ('italian-food.jpg',      'Locanda Verde',           'デ・ニーロ共同オーナーの名店', '🍝 13:30'),
        ('de-niro.jpg',           'Robert De Niro',          'Tribeca Film Festival開催中・遭遇率MAX', '🎬 本日のキー'),
        ('dumbo-manhattan.jpg',   'DUMBO 映画聖地',          'ワンス・アポン・ア・タイム・イン・アメリカ ポスター撮影地', '🎬 15:20'),
        ('old-st-patricks.jpg',   "Old St. Patrick's",       'Mean Streets（デ・ニーロ主演）ロケ地', '🏛️ 16:30'),
        ('little-italy.jpg',      'Little Italy / Mott St',  'ゴッドファーザー巡礼・137 Mott（果物店）', '🍊 16:45-17:30'),
    ]),
    'd13': ('📸 本日のスポット（Dallas ダブルパーク）', [
        ('roller-coaster.jpg',    'Six Flags Over Texas',    '午前の世界記録コースター（Tormenta Rampaging Run 309ft）', '🎢 10:00'),
        ('water-park.jpg',        'Hurricane Harbor',        '午後は波プール・Hook\'s Lagoon・Wahoo Racer', '🌊 14:30'),
        ('seafood.jpg',           'Pappadeaux Seafood',      'ケイジャン名物 Redfish Ponchartrain', '🦐 19:45'),
    ]),
    'd14': ('📸 本日のスポット（W杯試合日）', [
        ('stadium.jpg',           'AT&T Stadium',            'Block 440 / Row 19 / Seat 7-10', '⚽ 15:00 CDT'),
        ('globe-life-field.jpg',  'Globe Life Field',        'MLBレンジャーズ球場（試合前の外観散策）', '🏈 09:30'),
    ]),
    'd17': ('📸 本日のスポット（Disneyland）', [
        ('disneyland-castle.jpg', 'Sleeping Beauty Castle',  'ディズニーランドのシンボル', '🏰 09:00'),
        ('marina-sunset.jpg',     'Marina del Rey',          '夜に移動・翌日の拠点', '🌅 22:00'),
    ]),
    'd18': ('📸 本日のスポット（Range Rover DAY）', [
        ('range-rover.jpg',       'Range Rover',             'Enterprise Marina でピックアップ', '🚗 08:00'),
        ('hollywood-sign.jpg',    'Hollywood Sign',          'Ovation Hollywood屋上から眺望', '🎬 10:30'),
        ('tcl-chinese.jpg',       'TCL Chinese Theatre',     'ジョニー・デップらの手形・足型200以上', '🎬 10:00'),
        ('in-n-out.jpg',          'In-N-Out Burger',         'Double-Double + Animal Style', '🍔 11:30'),
        ('the-grove.jpg',         'The Grove',               '無料トロリー・噴水ショー・Apple/Nordstrom', '🛍️ 13:00'),
        ('griffith.jpg',          'Griffith Observatory',    'LA全景・「ラ・ラ・ランド」ロケ地', '🔭 14:30'),
    ]),
    'd19': ('📸 本日のスポット（帰国日）', [
        ('marina-sunset.jpg',     'Marina del Rey 朝',       '最後のアメリカの朝', '🌅 07:00'),
        ('airplane.jpg',          'LAX → HND',               'Delta DL0007 Airbus A350-900 / 11時間40分', '✈️ 10:20'),
    ]),
}

def make_gallery(heading, items):
    cards = []
    for img, name, desc, tag in items:
        cards.append(
            f'    <figure class="place-card">\n'
            f'      <img src="images/{img}" alt="{name}" loading="lazy">\n'
            f'      <figcaption>\n'
            f'        <strong>{name}</strong>\n'
            f'        <span class="jp">{desc}</span>\n'
            f'        <span class="tag">{tag}</span>\n'
            f'      </figcaption>\n'
            f'    </figure>'
        )
    return (
        f'\n  <h2>{heading}</h2>\n'
        f'  <div class="place-gallery">\n'
        + '\n'.join(cards)
        + '\n  </div>\n'
    )

# 挿入位置: 各 <section id="dXX" class="page"> の中で、<h2>🗺️ この日のマップ</h2> の直前に入れる
inserted = 0
for day_id, (heading, items) in GALLERIES.items():
    # 既に挿入済みなら飛ばす（idempotent）
    probe = f'<section id="{day_id}" class="page">'
    sec_start = html.find(probe)
    if sec_start < 0:
        print(f'  !! {day_id} not found')
        continue
    nxt = html.find('<section id="', sec_start + 10)
    if nxt < 0: nxt = len(html)
    segment = html[sec_start:nxt]
    if f'📸 本日のスポット' in segment or f'📸 本日のスポット（' in segment:
        # 特定の見出しチェック
        if heading.split('（')[0] in segment:
            print(f'  -- {day_id}: already inserted')
            continue
    # マップの直前に挿入
    anchor = '<h2>🗺️ この日のマップ</h2>'
    anchor_pos = html.find(anchor, sec_start, nxt)
    if anchor_pos < 0:
        # マップがなければ <h2>タイムライン の前に
        anchor2 = '<h2>タイムライン / Timeline'
        anchor_pos = html.find(anchor2, sec_start, nxt)
        if anchor_pos < 0:
            print(f'  !! {day_id}: no anchor')
            continue

    block = make_gallery(heading, items)
    html = html[:anchor_pos] + block + '  ' + html[anchor_pos:]
    inserted += 1
    print(f'  + {day_id}: {len(items)} 枚挿入 ({heading[:20]})')

PATH.write_text(html, encoding='utf-8')
print(f'\n✅ {inserted} days updated; size={len(html):,}B')
