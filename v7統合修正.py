"""v7 の3点最終修正:
  ① 残り4つの emoji カードを実写カード化（Guardians/WEB SLINGERS/Pirates Lair/Animation Building）
  ② ディズニーチケット表の「10+」を「大人」表示に
  ③ 費用ページに ANA/Southwest の実金額を反映"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path

PATH = Path(r'C:/Users/kyosu/worldカップ旅行/travel-guide-v7.html')
html = PATH.read_text(encoding='utf-8')

# ========= ① emoji → 実写カード（4枚） =========
CARD_REPLACEMENTS = [
    # Guardians of the Galaxy（紫emoji → guardians-breakout.jpg）
    (
        '''  <figure class="attr-card">
    <div class="thumb emoji purple">🎢<span class="badge-corner">絶叫</span></div>
    <div class="body">
      <h4>Guardians of the Galaxy – Mission: BREAKOUT!</h4>
      <p>旧 Tower of Terror を改装。高さ55mから急降下。スリル系ファン必須。</p>
      <span class="area">Avengers Campus</span>
    </div>
  </figure>''',
        '''  <figure class="attr-card">
    <div class="thumb">
      <img src="images/guardians-breakout.jpg" alt="Guardians of the Galaxy – Mission: BREAKOUT!" loading="lazy">
      <span class="badge-corner">絶叫</span>
    </div>
    <div class="body">
      <h4>🎢 Guardians of the Galaxy – Mission: BREAKOUT!</h4>
      <p>旧 Tower of Terror を改装。高さ55mから急降下。スリル系ファン必須。</p>
      <span class="area">Avengers Campus</span>
    </div>
  </figure>'''
    ),
    # WEB SLINGERS（orange emoji → web-slingers.jpg）
    (
        '''  <figure class="attr-card">
    <div class="thumb emoji orange">🕷️<span class="badge-corner">家族OK</span></div>
    <div class="body">
      <h4>WEB SLINGERS: A Spider-Man Adventure</h4>
      <p>インタラクティブ・シューティング。腕を振って実際にウェブを放つ動き。</p>
      <span class="area">Avengers Campus</span>
    </div>
  </figure>''',
        '''  <figure class="attr-card">
    <div class="thumb">
      <img src="images/web-slingers.jpg" alt="Avengers Campus" loading="lazy">
      <span class="badge-corner">家族OK</span>
    </div>
    <div class="body">
      <h4>🕷️ WEB SLINGERS: A Spider-Man Adventure</h4>
      <p>インタラクティブ・シューティング。腕を振って実際にウェブを放つ動き。</p>
      <span class="area">Avengers Campus</span>
    </div>
  </figure>'''
    ),
    # Pirates Lair on Tom Sawyer Island
    (
        '''  <figure class="attr-card">
    <div class="thumb emoji green">🏴‍☠️<span class="badge-corner pri">みな実</span></div>
    <div class="body">
      <h4>Pirates Lair on Tom Sawyer Island</h4>
      <p>子供大喜びの探検型アトラクション。島を船で渡って秘密の洞窟へ。</p>
      <span class="area">Frontierland</span>
    </div>
  </figure>''',
        '''  <figure class="attr-card">
    <div class="thumb">
      <img src="images/pirates-lair.jpg" alt="Tom Sawyer Island raft" loading="lazy">
      <span class="badge-corner pri">みな実</span>
    </div>
    <div class="body">
      <h4>🏴‍☠️ Pirates Lair on Tom Sawyer Island</h4>
      <p>子供大喜びの探検型アトラクション。島を船で渡って秘密の洞窟へ。</p>
      <span class="area">Frontierland</span>
    </div>
  </figure>'''
    ),
    # Disney Animation Building
    (
        '''  <figure class="attr-card">
    <div class="thumb emoji dark">🎬<span class="badge-corner pri">涼しい</span></div>
    <div class="body">
      <h4>Disney Animation Building</h4>
      <p>Turtle Talk with Crush（ニモの亀とライブ会話）・Sorcerer\'s Workshop。室内で休憩にも。</p>
      <span class="area">Hollywood Land</span>
    </div>
  </figure>''',
        '''  <figure class="attr-card">
    <div class="thumb">
      <img src="images/animation-building.jpg" alt="Disney Animation Building" loading="lazy">
      <span class="badge-corner pri">涼しい</span>
    </div>
    <div class="body">
      <h4>🎬 Disney Animation Building</h4>
      <p>Turtle Talk with Crush（ニモの亀とライブ会話）・Sorcerer\'s Workshop。室内で休憩にも。</p>
      <span class="area">Hollywood Land</span>
    </div>
  </figure>'''
    ),
]

n_cards = 0
for old, new in CARD_REPLACEMENTS:
    if old in html:
        html = html.replace(old, new)
        n_cards += 1
print(f'① emoji → 実写カード: {n_cards}/{len(CARD_REPLACEMENTS)}')

# ========= ② 「10+」→「大人（39歳）」 =========
# d15 と d16 の Park Reservation テーブル
OLD_AGE = '''    <tr><td>恭祐</td><td>18+</td><td><code>082063065453666048</code></td></tr>
    <tr><td>えり子</td><td>10+</td><td><code>082063065453666048</code></td></tr>'''
NEW_AGE = '''    <tr><td>恭祐</td><td>大人</td><td><code>082063065453666048</code></td></tr>
    <tr><td>えり子</td><td>大人</td><td><code>082063065453666048</code></td></tr>'''
n_age = 0
if OLD_AGE in html:
    html = html.replace(OLD_AGE, NEW_AGE)
    n_age += 1

OLD_AGE2 = '''    <tr><td>恭祐</td><td>18+</td><td><code>082063065487220480</code></td></tr>
    <tr><td>えり子</td><td>10+</td><td><code>082063065487220480</code></td></tr>'''
NEW_AGE2 = '''    <tr><td>恭祐</td><td>大人</td><td><code>082063065487220480</code></td></tr>
    <tr><td>えり子</td><td>大人</td><td><code>082063065487220480</code></td></tr>'''
if OLD_AGE2 in html:
    html = html.replace(OLD_AGE2, NEW_AGE2)
    n_age += 1

# 予約管理ページのDisney内訳で「10+」に対応する Adult を明記
OLD_DESC = 'Kids Summer Offer $168×2 + 2-Day Adult $403×2'
NEW_DESC = 'Kids\' Summer Offer (年齢3-9) $168×2 + 2-Day Adult (年齢10+) $403×2'
# これはもう記載済のため追加不要
# 内訳行の整合は保つ

# 子供の 3-9 も「子供（8歳/7歳）」に分かりやすく
OLD_KIDS = '''    <tr><td>ゆうしん</td><td>3-9</td><td><code>082063065386557184</code></td></tr>
    <tr><td>みな実</td><td>3-9</td><td><code>082063065386557184</code></td></tr>'''
NEW_KIDS = '''    <tr><td>ゆうしん（8歳）</td><td>子供</td><td><code>082063065386557184</code></td></tr>
    <tr><td>みな実（7歳）</td><td>子供</td><td><code>082063065386557184</code></td></tr>'''
if OLD_KIDS in html:
    html = html.replace(OLD_KIDS, NEW_KIDS)
    n_age += 1

OLD_KIDS2 = '''    <tr><td>ゆうしん</td><td>3-9</td><td><code>082063065420111616</code></td></tr>
    <tr><td>みな実</td><td>3-9</td><td><code>082063065420111616</code></td></tr>'''
NEW_KIDS2 = '''    <tr><td>ゆうしん（8歳）</td><td>子供</td><td><code>082063065420111616</code></td></tr>
    <tr><td>みな実（7歳）</td><td>子供</td><td><code>082063065420111616</code></td></tr>'''
if OLD_KIDS2 in html:
    html = html.replace(OLD_KIDS2, NEW_KIDS2)
    n_age += 1

# 予約管理ページの詳細表
OLD_RESV = '''    <tr><th>日程</th><th>パーク</th><th>子供（ゆうしん・みな実）</th><th>大人（恭祐・えり子）</th></tr>
    <tr><td>6/15 (月)</td><td>California Adventure</td><td><code>082063065386557184</code></td><td><code>082063065453666048</code></td></tr>
    <tr><td>6/16 (火)</td><td>Disneyland Park</td><td><code>082063065420111616</code></td><td><code>082063065487220480</code></td></tr>'''
# そのまま（既に 大人/子供 表記）
print(f'② 年齢表記修正: {n_age}/4')

# ========= ③ 費用ページに ANA + Southwest の実金額を反映 =========
OLD_FLIGHTS = '''    <table class="tb">
      <tr><th>区間</th><th>便名</th><th>予約番号</th><th>金額</th></tr>
      <tr><td>関空 → 羽田 → JFK（往路）</td><td>NH094 + NH110</td><td><code>DT2RSF</code></td><td>ANA 別途予約済</td></tr>
      <tr><td>EWR → DFW (6/12 21:09)</td><td>UA1331</td><td><code>DZRMNG</code></td><td>ANA 発券内</td></tr>
      <tr><td>DAL → DEN → SNA (6/15)</td><td>Southwest WN1300/WN4175</td><td><code>CF846Y</code></td><td>Southwest 別途予約済</td></tr>
      <tr><td class="w-bold">LAX → HND (6/19 · 復路)</td><td class="w-bold">Delta DL0007 A350-900 Comfort Classic × 4</td><td><code>HPO4P4</code></td><td class="w-bold c-acc">$5,500</td></tr>
      <tr><td>HND → KIX (6/20 18:25)</td><td>NH095</td><td><code>DX58X4</code></td><td>¥46,140（既払）</td></tr>
      <tr><td class="w-bold">航空券（Delta 分）小計</td><td colspan="2"></td><td class="w-bold c-acc">$5,500</td></tr>
    </table>
    <p class="small muted">※ Delta DL0007 は概算。実支払額がわかれば差し替え。ANA・Southwest は別途予約済で航空券小計には含めず参考表記。</p>'''

NEW_FLIGHTS = '''    <table class="tb">
      <tr><th>区間</th><th>便名</th><th>予約番号</th><th>金額（実領収額）</th></tr>
      <tr><td>関空 → 羽田 → JFK（往路）</td><td>NH094 + NH110</td><td><code>DT2RSF</code></td><td>¥154,420（ANA決済完了）</td></tr>
      <tr><td>EWR → DFW (6/12 21:09)</td><td>UA1331（ANA発券）</td><td><code>DZRMNG</code></td><td>¥3,560（ANA決済完了）</td></tr>
      <tr><td>DAL → DEN → SNA (6/15)</td><td>Southwest WN1300/WN4175</td><td><code>CF846Y</code></td><td>$288.20（Base $73.40/人×4）</td></tr>
      <tr><td class="w-bold">LAX → HND (6/19 · 復路)</td><td class="w-bold">Delta DL0007 A350-900 Comfort Classic × 4</td><td><code>HPO4P4</code></td><td class="w-bold c-acc">$5,490.00（$1,372.50×4）</td></tr>
      <tr><td>HND → KIX (6/20 18:25)</td><td>NH095</td><td><code>DX58X4</code></td><td>¥46,140（ANA決済完了）</td></tr>
      <tr><td class="w-bold">航空券 合計</td><td colspan="2">USD + JPY</td><td class="w-bold c-acc">$5,778 + ¥204,120（約 $7,086 相当）</td></tr>
    </table>
    <p class="small muted">※ 全便実領収額。円ドル換算は $1=¥156。ANA国際 ¥154,420 / ANA-UA ¥3,560 / Southwest $288.20 / Delta $5,490 / ANA国内 ¥46,140。</p>'''

if OLD_FLIGHTS in html:
    html = html.replace(OLD_FLIGHTS, NEW_FLIGHTS)
    print('③ 航空券実金額を反映')
else:
    print('③ !! 航空券ブロックが一致しない')

# サマリー小計（右上の "$5,500（Delta 復路）"）
OLD_SUM = '<span class="cat-total">$5,500（Delta 復路）</span>'
NEW_SUM = '<span class="cat-total">$7,086 相当（全便）</span>'
html = html.replace(OLD_SUM, NEW_SUM)

# 総額 ($13,858-14,525) を新たに加算
# 現地+Delta → 現地+全航空券
# 以前: $8,358 (現地) + $5,500 (Delta) = $13,858-14,525
# 新: 航空券全部で $7,086 + 現地 $8,358-9,025 = $15,444-16,111
OLD_TOTAL = '''<span class="amount">13,858 – 14,525</span>
    </div>
    <div class="grand-total-jpy">約 ¥2,162,000 – 2,266,000（$1 = ¥156換算）</div>'''
NEW_TOTAL = '''<span class="amount">15,444 – 16,111</span>
    </div>
    <div class="grand-total-jpy">約 ¥2,409,000 – 2,513,000（$1 = ¥156換算）</div>'''
if OLD_TOTAL in html:
    html = html.replace(OLD_TOTAL, NEW_TOTAL)
    print('④ 総額更新 $15,444-16,111')

# 支払方法カードの事前支払額も更新
OLD_PAID = '<h4>事前支払済</h4><p class="amt-l">約 $10,333</p>'
NEW_PAID = '<h4>事前支払済</h4><p class="amt-l">約 $11,919</p>'
if OLD_PAID in html:
    html = html.replace(OLD_PAID, NEW_PAID)

OLD_BREAKDOWN = 'W杯 $3,426 + Disney $1,142 + Enterprise $265 + Delta $5,500'
NEW_BREAKDOWN = 'W杯 $3,426 + Disney $1,142 + Enterprise $265 + ANA+SW $2,000相当 + Delta $5,490'
html = html.replace(OLD_BREAKDOWN, NEW_BREAKDOWN)

# 1人あたり換算
OLD_PER = '現地費用＋Delta復路で $13,858–14,525 を4人で割ると<strong>1人 $3,465–3,631（約¥540,000–¥566,000）</strong>'
NEW_PER = '現地費用＋全航空券で $15,444–16,111 を4人で割ると<strong>1人 $3,861–4,028（約¥602,000–¥628,000）</strong>'
html = html.replace(OLD_PER, NEW_PER)

PATH.write_text(html, encoding='utf-8')
print(f'\n✅ size={len(html):,}B')
