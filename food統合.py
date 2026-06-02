"""v7 の4つの食事セクションを画像カード化"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path

PATH = Path(r'C:/Users/kyosu/worldカップ旅行/travel-guide-v7.html')
html = PATH.read_text(encoding='utf-8')

# ===== CSS: 食品カード用ミニスタイル =====
FOOD_CSS = '''
/* ============ FOOD CARD ============ */
.food-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin:14px 0 24px}
.food-card{background:var(--card);border:1px solid var(--border);border-radius:10px;overflow:hidden;box-shadow:var(--shadow-sm);display:flex;flex-direction:column;transition:.2s}
.food-card:hover{transform:translateY(-2px);box-shadow:var(--shadow)}
.food-card img{width:100%;aspect-ratio:4/3;object-fit:cover;display:block;background:var(--border-l)}
.food-card .body{padding:10px 12px;flex:1}
.food-card h4{margin:0 0 3px;font-family:var(--font-serif);font-size:13.5px;color:var(--primary);font-weight:700;line-height:1.3}
.food-card .desc{font-size:11px;color:var(--ink-l);line-height:1.5;margin:0}
.food-card.star{border-left:3px solid var(--accent)}
.food-card.gold{border-left:3px solid var(--gold);background:linear-gradient(135deg,#fffcf5 0%,#fff 100%)}
'''
if '.food-grid{' not in html:
    html = html.replace('</style>', FOOD_CSS + '\n</style>', 1)

# ===== ① d12 Locanda Verde 推奨メニュー =====
OLD_LOCANDA = '''    <h4>推奨メニュー</h4>
    <ul class="simple">
      <li>Famous Sheep's Milk Ricotta（羊乳リコッタ）$24</li>
      <li>Cacio e Pepe（カチョエペペ）$28</li>
      <li>Grandma Ravioli（おばあちゃんのラビオリ）$32</li>
      <li>Margherita Pizzette（マルゲリータピッツェ・子供用）$22</li>
      <li>Branzino（ヨーロピアンシーバス）$45</li>
      <li>Tiramisu（ティラミス）$15</li>
    </ul>'''

NEW_LOCANDA = '''    <h4>推奨メニュー / Menu</h4>
    <div class="food-grid">
      <figure class="food-card"><img src="images/food-ricotta.jpg" alt="Sheep's Milk Ricotta" loading="lazy"><div class="body"><h4>🧀 Famous Sheep's Milk Ricotta</h4><p class="desc">羊乳リコッタの前菜 · $24</p></div></figure>
      <figure class="food-card"><img src="images/food-cacio-pepe.jpg" alt="Cacio e Pepe" loading="lazy"><div class="body"><h4>🍝 Cacio e Pepe</h4><p class="desc">ローマ伝統のペコリーノチーズ+黒胡椒 · $28</p></div></figure>
      <figure class="food-card"><img src="images/food-ravioli.jpg" alt="Grandma Ravioli" loading="lazy"><div class="body"><h4>🥟 Grandma Ravioli</h4><p class="desc">おばあちゃんのラビオリ · $32</p></div></figure>
      <figure class="food-card"><img src="images/pizza.jpg" alt="Margherita Pizzette" loading="lazy"><div class="body"><h4>🍕 Margherita Pizzette</h4><p class="desc">子供用マルゲリータ · $22</p></div></figure>
      <figure class="food-card star"><img src="images/food-branzino.jpg" alt="Branzino" loading="lazy"><div class="body"><h4>🐟 Branzino</h4><p class="desc">ヨーロピアンシーバスのグリル · $45</p></div></figure>
      <figure class="food-card"><img src="images/food-tiramisu.jpg" alt="Tiramisu" loading="lazy"><div class="body"><h4>🍰 Tiramisu</h4><p class="desc">ティラミス · $15</p></div></figure>
    </div>'''

if OLD_LOCANDA in html:
    html = html.replace(OLD_LOCANDA, NEW_LOCANDA)
    print('① Locanda Verde 6品 画像カード化')

# ===== ② d13 Pappadeaux 必食メニュー =====
OLD_PAP = '''  <h2>Pappadeaux 必食メニュー / Must-Order</h2>
  <div class="grid grid-3">
    <div class="card">
      <h4>前菜（Appetizer）</h4>
      <ul class="simple">
        <li>Pappadeaux Deluxe Platter（盛り合わせ）</li>
        <li>Louisiana Gumbo（ルイジアナ・ガンボ）</li>
        <li>Crawfish Étouffée（ザリガニのエトゥフェ）</li>
      </ul>
    </div>
    <div class="card">
      <h4>メイン（Entrée）</h4>
      <ul class="simple">
        <li>⭐ Redfish Ponchartrain（名物・レッドフィッシュ）</li>
        <li>Shrimp Creole（エビのクレオール）</li>
        <li>Crab Cakes（クラブケーキ）</li>
      </ul>
    </div>
    <div class="card">
      <h4>テキサス限定（Texas Special）</h4>
      <ul class="simple">
        <li>⭐ Texas Twinkies（ハラペーニョ+チーズ+ベーコン）</li>
        <li>🍌 Tres Leches Banana Pudding（デザート）</li>
      </ul>
    </div>'''

NEW_PAP = '''  <h2>Pappadeaux 必食メニュー / Must-Order</h2>
  <div class="food-grid">
    <figure class="food-card"><img src="images/food-gumbo.jpg" alt="Louisiana Gumbo" loading="lazy"><div class="body"><h4>🍲 Louisiana Gumbo</h4><p class="desc">ルイジアナ・ガンボ（シーフード煮込み）</p></div></figure>
    <figure class="food-card"><img src="images/seafood.jpg" alt="Pappadeaux Deluxe Platter" loading="lazy"><div class="body"><h4>🦐 Deluxe Platter</h4><p class="desc">海の幸盛り合わせ前菜</p></div></figure>
    <figure class="food-card"><img src="images/seafood.jpg" alt="Crawfish Étouffée" loading="lazy"><div class="body"><h4>🦞 Crawfish Étouffée</h4><p class="desc">ザリガニのエトゥフェ（伝統ソース）</p></div></figure>
    <figure class="food-card star"><img src="images/food-redfish.jpg" alt="Redfish Ponchartrain" loading="lazy"><div class="body"><h4>⭐ Redfish Ponchartrain</h4><p class="desc">名物 · レッドフィッシュ（本店看板）</p></div></figure>
    <figure class="food-card"><img src="images/seafood.jpg" alt="Shrimp Creole" loading="lazy"><div class="body"><h4>🍤 Shrimp Creole</h4><p class="desc">エビのクレオール風</p></div></figure>
    <figure class="food-card"><img src="images/food-crab-cake.jpg" alt="Crab Cakes" loading="lazy"><div class="body"><h4>🦀 Crab Cakes</h4><p class="desc">メリーランド式クラブケーキ</p></div></figure>
    <figure class="food-card gold"><img src="images/food-jalapeno-popper.jpg" alt="Texas Twinkies" loading="lazy"><div class="body"><h4>⭐ Texas Twinkies</h4><p class="desc">ハラペーニョ+チーズ+ベーコン（テキサス限定）</p></div></figure>
    <figure class="food-card"><img src="images/food-tres-leches.jpg" alt="Tres Leches Banana Pudding" loading="lazy"><div class="body"><h4>🍌 Tres Leches Banana Pudding</h4><p class="desc">デザートの傑作</p></div></figure>'''

if OLD_PAP in html:
    html = html.replace(OLD_PAP, NEW_PAP)
    print('② Pappadeaux 8品 画像カード化')

# ===== ③ d15 California Adventure 食事 =====
OLD_DCA = '''<h2>🍴 California Adventure の絶対食べたいもの</h2>
<div class="grid grid-3">
  <div class="card"><h4>🌶️ Cozy Cone Motel</h4><p class="small">Cars Land のコーン型フードスタンド・チリ・チーズ・ポップコーン</p></div>
  <div class="card"><h4>🥨 Corndog Castle</h4><p class="small">Pixar Pier の巨大コーンドッグ（Paradise Garden）</p></div>
  <div class="card"><h4>🍦 Ghirardelli Soda Fountain</h4><p class="small">Downtown Disney 側・サンフランシスコ発の老舗チョコ店</p></div>
</div>'''

NEW_DCA = '''<h2>🍴 California Adventure の絶対食べたいもの</h2>
<div class="food-grid">
  <figure class="food-card"><img src="images/food-chili-cone.jpg" alt="Cozy Cone Motel" loading="lazy"><div class="body"><h4>🌶️ Cozy Cone Motel</h4><p class="desc">Cars Land のコーン型フードスタンド · チリ/チーズ/ポップコーン</p></div></figure>
  <figure class="food-card"><img src="images/food-corn-dog.jpg" alt="Corndog Castle" loading="lazy"><div class="body"><h4>🥨 Corndog Castle</h4><p class="desc">Pixar Pier の巨大コーンドッグ（Paradise Garden）</p></div></figure>
  <figure class="food-card gold"><img src="images/food-chocolate.jpg" alt="Ghirardelli Soda Fountain" loading="lazy"><div class="body"><h4>🍦 Ghirardelli Soda Fountain</h4><p class="desc">Downtown Disney · SF発の老舗チョコ・サンデー</p></div></figure>
</div>'''

if OLD_DCA in html:
    html = html.replace(OLD_DCA, NEW_DCA)
    print('③ DCA 3品 画像カード化')

# ===== ④ d16 Disneyland Park 食事 =====
OLD_DL = '''<h2>🍴 Disneyland Park の絶対食べたいもの</h2>
<div class="grid grid-3">
  <div class="card gold"><h4>🍗 Plaza Inn フライドチキン</h4><p class="small">Main Street・老舗の名物フライドチキン・ランチに最適</p></div>
  <div class="card gold"><h4>🍛 Blue Bayou Restaurant ⭐</h4><p class="small">Pirates of the Caribbean 内・予約必須の人気店・Monte Cristo</p></div>
  <div class="card"><h4>🍍 Dole Whip（Tiki Juice Bar）</h4><p class="small">Adventureland 名物・パイナップルソフト・行列必至</p></div>
  <div class="card"><h4>🥨 Mickey Pretzel</h4><p class="small">ミッキー形プレッツェル・手軽なおやつ</p></div>
  <div class="card"><h4>🍚 Rancho del Zocalo</h4><p class="small">Frontierland・本格メキシカン・ブリトー/タコス</p></div>
  <div class="card"><h4>🥐 Jolly Holiday Bakery</h4><p class="small">Main Street・Mary Poppins テーマ・朝食にも</p></div>
</div>'''

NEW_DL = '''<h2>🍴 Disneyland Park の絶対食べたいもの</h2>
<div class="food-grid">
  <figure class="food-card gold"><img src="images/food-fried-chicken.jpg" alt="Plaza Inn Fried Chicken" loading="lazy"><div class="body"><h4>🍗 Plaza Inn フライドチキン</h4><p class="desc">Main Street・老舗の名物フライドチキン・ランチに最適</p></div></figure>
  <figure class="food-card gold"><img src="images/food-monte-cristo.jpg" alt="Blue Bayou Monte Cristo" loading="lazy"><div class="body"><h4>🍛 Blue Bayou ⭐ Monte Cristo</h4><p class="desc">Pirates of the Caribbean 内・予約必須の人気店</p></div></figure>
  <figure class="food-card"><img src="images/dole-whip.jpg" alt="Dole Whip" loading="lazy"><div class="body"><h4>🍍 Dole Whip</h4><p class="desc">Adventureland Tiki Juice Bar · パイナップルソフト・行列必至</p></div></figure>
  <figure class="food-card"><img src="images/food-pretzel.jpg" alt="Mickey Pretzel" loading="lazy"><div class="body"><h4>🥨 Mickey Pretzel</h4><p class="desc">ミッキー形プレッツェル・手軽なおやつ</p></div></figure>
  <figure class="food-card"><img src="images/food-burrito.jpg" alt="Rancho del Zocalo" loading="lazy"><div class="body"><h4>🌯 Rancho del Zocalo</h4><p class="desc">Frontierland・本格メキシカン・ブリトー/タコス</p></div></figure>
  <figure class="food-card"><img src="images/food-pastry.jpg" alt="Jolly Holiday Bakery" loading="lazy"><div class="body"><h4>🥐 Jolly Holiday Bakery</h4><p class="desc">Main Street・Mary Poppins テーマ・朝食にも</p></div></figure>
</div>'''

if OLD_DL in html:
    html = html.replace(OLD_DL, NEW_DL)
    print('④ Disneyland 6品 画像カード化')

PATH.write_text(html, encoding='utf-8')
print(f'\n✅ size={len(html):,}B')
