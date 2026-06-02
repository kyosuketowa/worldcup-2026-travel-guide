"""v7.html の3点修正:
  1) d15 重複した California Adventure アトラクションセクション削除
  2) 残った CA アトラクションを画像カード化
  3) 費用ページに Delta 航空券の行を追加（往路 ANA も含めて総額再計算）"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path

PATH = Path(r'C:/Users/kyosu/worldカップ旅行/travel-guide-v7.html')
html = PATH.read_text(encoding='utf-8')

# =====================================================
# ① d15 の最初（古い6枚）CA アトラクションセクションを削除
# =====================================================
OLD1 = '''<h2>🎢 California Adventure 必訪アトラクション</h2>
<div class="grid grid-2">
  <div class="card accent"><h4>🎢 Guardians of the Galaxy – Mission: BREAKOUT!</h4><p class="small">絶叫系・旧 Tower of Terror</p></div>
  <div class="card"><h4>🚗 Radiator Springs Racers</h4><p class="small">Cars ファミリー向け・Lightning Lane 必須</p></div>
  <div class="card"><h4>🕷️ WEB SLINGERS: A Spider-Man Adventure</h4><p class="small">インタラクティブシューティング</p></div>
  <div class="card"><h4>🧚 Pixar Pal-A-Round</h4><p class="small">海沿いの大観覧車</p></div>
  <div class="card gold"><h4>🎭 World of Color ⭐<\\h4><p class="small">夜のナイトショー（必見・21:00頃）</p></div>
  <div class="card"><h4>🌶️ Cars Land</h4><p class="small">Radiator Springs の街並み再現</p></div>
</div>'''

if OLD1 in html:
    html = html.replace(OLD1, '')
    print('+ 重複した古い California Adventure ブロック削除')
else:
    print('  -- 古い重複ブロックが見つからない（すでに除去済みか）')

# =====================================================
# ② 残った CA アトラクションを画像カード化
# =====================================================
OLD2 = '''<h2>🎢 California Adventure 必訪アトラクション</h2>
<div class="grid grid-2">
  <div class="card accent"><h4>🎢 Guardians of the Galaxy – Mission: BREAKOUT!</h4><p class="small">絶叫系・旧 Tower of Terror を改装・高さ55m・急降下</p></div>
  <div class="card accent"><h4>🚗 Radiator Springs Racers</h4><p class="small">Cars ファミリー向け・屋外レース・Lightning Lane 必須</p></div>
  <div class="card"><h4>🕷️ WEB SLINGERS: A Spider-Man Adventure</h4><p class="small">インタラクティブシューティング・Avengers Campus</p></div>
  <div class="card"><h4>🧚 Pixar Pal-A-Round（旧 Mickey\'s Fun Wheel）</h4><p class="small">海沿いの大観覧車・固定 or 揺れる選択可</p></div>
  <div class="card gold"><h4>🎭 World of Color ⭐<\\h4><p class="small">夜の噴水ショー（必見・21:00頃・Paradise Bay）</p></div>
  <div class="card"><h4>🌶️ Cars Land</h4><p class="small">Radiator Springs 街並み再現・「カーズ」の世界</p></div>
  <div class="card"><h4>🏴‍☠️ Pirates Lair on Tom Sawyer Island</h4><p class="small">子供大喜び・探検型アトラクション</p></div>
  <div class="card"><h4>🎬 Disney Animation Building</h4><p class="small">Turtle Talk with Crush ・Sorcerer\'s Workshop</p></div>
</div>'''

NEW2 = '''<h2>🎢 California Adventure 必訪アトラクション</h2>
<div class="attr-grid">

  <figure class="attr-card">
    <div class="thumb emoji purple">🎢<span class="badge-corner">絶叫</span></div>
    <div class="body">
      <h4>Guardians of the Galaxy – Mission: BREAKOUT!</h4>
      <p>旧 Tower of Terror を改装。高さ55mから急降下。スリル系ファン必須。</p>
      <span class="area">Avengers Campus</span>
    </div>
  </figure>

  <figure class="attr-card">
    <div class="thumb">
      <img src="images/radiator-springs.jpg" alt="Radiator Springs Racers" loading="lazy">
      <span class="badge-corner gold">⭐ LL必須</span>
    </div>
    <div class="body">
      <h4>🚗 Radiator Springs Racers</h4>
      <p>「カーズ」世界のスピード対決レース。屋外・一番人気。Lightning Lane 最優先で予約。</p>
      <span class="area">Cars Land</span>
    </div>
  </figure>

  <figure class="attr-card">
    <div class="thumb emoji orange">🕷️<span class="badge-corner">家族OK</span></div>
    <div class="body">
      <h4>WEB SLINGERS: A Spider-Man Adventure</h4>
      <p>インタラクティブ・シューティング。実際に web を放つ動き。</p>
      <span class="area">Avengers Campus</span>
    </div>
  </figure>

  <figure class="attr-card">
    <div class="thumb emoji pink">🎡<span class="badge-corner pri">景色</span></div>
    <div class="body">
      <h4>Pixar Pal-A-Round</h4>
      <p>旧 Mickey\'s Fun Wheel。海沿いの大観覧車。固定 or 揺れる選択可。</p>
      <span class="area">Pixar Pier</span>
    </div>
  </figure>

  <figure class="attr-card">
    <div class="thumb">
      <img src="images/world-of-color.jpg" alt="World of Color" loading="lazy">
      <span class="badge-corner gold">MUST</span>
    </div>
    <div class="body">
      <h4>🎭 World of Color ⭐</h4>
      <p>夜の噴水＋光＋炎のナイトショー。1200の噴水と大型スクリーン。必見。</p>
      <span class="area">Paradise Bay · 21:00</span>
    </div>
  </figure>

  <figure class="attr-card">
    <div class="thumb emoji orange">🌶️<span class="badge-corner">エリア</span></div>
    <div class="body">
      <h4>Cars Land</h4>
      <p>Radiator Springs の街並みを完全再現。カーズの世界観に没入できる。</p>
      <span class="area">Cars Land</span>
    </div>
  </figure>

  <figure class="attr-card">
    <div class="thumb emoji green">🏴‍☠️<span class="badge-corner pri">みな実</span></div>
    <div class="body">
      <h4>Pirates Lair on Tom Sawyer Island</h4>
      <p>子供大喜びの探検型アトラクション。島を船で渡って秘密の洞窟へ。</p>
      <span class="area">Frontierland</span>
    </div>
  </figure>

  <figure class="attr-card">
    <div class="thumb emoji dark">🎬<span class="badge-corner pri">涼しい</span></div>
    <div class="body">
      <h4>Disney Animation Building</h4>
      <p>Turtle Talk with Crush（ニモの亀とライブ会話）・Sorcerer\'s Workshop。室内で休憩にも。</p>
      <span class="area">Hollywood Land</span>
    </div>
  </figure>

</div>'''

if OLD2 in html:
    html = html.replace(OLD2, NEW2)
    print('+ California Adventure アトラクション 8件を画像カード化')
else:
    print('  !! 対象ブロックが見つからない')

# =====================================================
# ③ 費用ページに Delta 行を追加 + 総額再計算
# =====================================================
# 航空券セクションを探して、新しい航空券総額表を追加
# 現在の budget は "参考表記" だけなので、きちんと金額入りの表に
OLD_FLIGHTS = '''<details class="budget-cat" open>
  <summary>
    <span class="cat-icon">✈️</span>
    <span class="cat-name">1. 航空券（Flights）</span>
    <span class="cat-total">小計 参照 下記</span>
  </summary>
  <table class="tb">
    <tr><th>区間</th><th>便名</th><th>予約番号</th></tr>
    <tr><td>関空 → 羽田 → JFK</td><td>NH094 + NH110</td><td>DT2RSF</td></tr>
    <tr><td>EWR → DFW (6/12 21:09)</td><td>UA1331</td><td>DZRMNG</td></tr>
    <tr><td>DAL → DEN → SNA (6/15)</td><td>WN1300/WN4175</td><td>CF846Y</td></tr>
    <tr><td>LAX → HND (6/19 10:20)</td><td>Delta DL0007 (A350-900)</td><td>HPO4P4</td></tr>
    <tr><td>HND → ITM (6/20 18:25)</td><td>NH095</td><td>DX58X4</td></tr>
  </table>
  <p class="small muted">※ 金額は予約済のため本総額には含めず参考表記</p>
</details>'''

NEW_FLIGHTS = '''<details class="budget-cat" open>
  <summary>
    <span class="cat-icon">✈️</span>
    <span class="cat-name">1. 航空券（Flights）</span>
    <span class="cat-total">$5,500（概算）</span>
  </summary>
  <table class="tb">
    <tr><th>区間</th><th>便名</th><th>予約番号</th><th>金額（概算）</th></tr>
    <tr><td>関空 → 羽田 → JFK（往路）</td><td>NH094 + NH110</td><td><code>DT2RSF</code></td><td>別途 ANA 予約済</td></tr>
    <tr><td>EWR → DFW (6/12 21:09)</td><td>UA1331</td><td><code>DZRMNG</code></td><td>ANA発券内</td></tr>
    <tr><td>DAL → DEN → SNA (6/15)</td><td>Southwest WN1300/WN4175</td><td><code>CF846Y</code></td><td>別途 Southwest 予約済</td></tr>
    <tr><td class="w-bold">LAX → HND (6/19 · 復路)</td><td class="w-bold">Delta DL0007 A350-900 Comfort Classic ×4</td><td><code>HPO4P4</code></td><td class="w-bold c-acc">$5,500</td></tr>
    <tr><td>HND → ITM (6/20 18:25)</td><td>NH095</td><td><code>DX58X4</code></td><td>¥46,140</td></tr>
    <tr><td class="w-bold">航空券（Delta）小計</td><td colspan="2"></td><td class="w-bold c-acc">$5,500</td></tr>
  </table>
  <p class="small muted">※ Delta は概算・実際の支払額がわかれば差し替え。ANA・Southwest 往路は別途予約済で本総額に含めず。</p>
</details>'''

if OLD_FLIGHTS in html:
    html = html.replace(OLD_FLIGHTS, NEW_FLIGHTS)
    print('+ 航空券セクションに Delta 金額 $5,500 を明示')
else:
    print('  !! 航空券セクションが見つからない')

# =====================================================
# ④ 総額も更新（現地費用 $8,358-9,025 + Delta $5,500 = $13,858-14,525）
# =====================================================
OLD_TOTAL = '''<div class="grand-total-amount">
    <span class="currency">$</span>
    <span class="amount">8,358 – 9,025</span>
  </div>
  <div class="grand-total-jpy">約 ¥1,304,000 – 1,408,000（$1 = ¥156換算）</div>'''

NEW_TOTAL = '''<div class="grand-total-amount">
    <span class="currency">$</span>
    <span class="amount">13,858 – 14,525</span>
  </div>
  <div class="grand-total-jpy">約 ¥2,162,000 – 2,266,000（$1 = ¥156換算）</div>'''

if OLD_TOTAL in html:
    html = html.replace(OLD_TOTAL, NEW_TOTAL)
    print('+ 総額を Delta $5,500 込みに更新 ($13,858-14,525)')

# 事前支払済 の金額も更新（$4,833 + Delta $5,500 = $10,333）
OLD_PAID = '''<div class="card"><h4>事前支払済</h4><p class="amt-l">約 $4,833</p>'''
NEW_PAID = '''<div class="card"><h4>事前支払済</h4><p class="amt-l">約 $10,333</p>'''
if OLD_PAID in html:
    html = html.replace(OLD_PAID, NEW_PAID)
    print('+ 事前支払済 $4,833 → $10,333 に更新')

# 支払内訳テキストも更新
OLD_BREAKDOWN = 'W杯 $3,426 + Disney $1,142 + Enterprise $265'
NEW_BREAKDOWN = 'W杯 $3,426 + Disney $1,142 + Enterprise $265 + Delta $5,500'
if OLD_BREAKDOWN in html:
    html = html.replace(OLD_BREAKDOWN, NEW_BREAKDOWN)
    print('+ 支払内訳テキストを Delta 込みに更新')

PATH.write_text(html, encoding='utf-8')
print(f'\n✅ size={len(html):,}B')
