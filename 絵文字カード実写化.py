"""v7.html の全emoji attr-cardを、新しく取得した実写真カードに置換。"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path

PATH = Path(r'C:/Users/kyosu/worldカップ旅行/travel-guide-v7.html')
html = PATH.read_text(encoding='utf-8')

replacements = []

# ============ d15: Cars Land emoji → real photo ============
OLD_CARS = '''  <figure class="attr-card">
    <div class="thumb emoji orange">🌶️<span class="badge-corner">エリア</span></div>
    <div class="body">
      <h4>Cars Land</h4>
      <p>Radiator Springs の街並みを完全再現。「カーズ」の世界に没入できる。</p>
      <span class="area">Cars Land</span>
    </div>
  </figure>'''
NEW_CARS = '''  <figure class="attr-card">
    <div class="thumb">
      <img src="images/cars-land.jpg" alt="Cars Land" loading="lazy">
      <span class="badge-corner">エリア</span>
    </div>
    <div class="body">
      <h4>🌶️ Cars Land</h4>
      <p>Radiator Springs の街並みを完全再現。「カーズ」の世界に没入できる。</p>
      <span class="area">Cars Land</span>
    </div>
  </figure>'''
replacements.append(('d15 Cars Land', OLD_CARS, NEW_CARS))

# ============ d16: 5枚の emoji → 実写 ============
# Rise of Resistance → rise-resistance.jpg (Millennium Falcon)
OLD_RISE = '''  <figure class="attr-card">
    <div class="thumb emoji dark">⚔️<span class="badge-corner">⭐ 朝一番</span></div>
    <div class="body">
      <h4>Star Wars: Rise of the Resistance</h4>
      <p>ゆうしん向け最新・最人気。開園ダッシュで Lightning Lane 最優先。</p>
      <span class="area">Star Wars: Galaxy\'s Edge</span>
    </div>
  </figure>'''
NEW_RISE = '''  <figure class="attr-card">
    <div class="thumb">
      <img src="images/rise-resistance.jpg" alt="Millennium Falcon at Galaxy\'s Edge" loading="lazy">
      <span class="badge-corner gold">⭐ 朝一番</span>
    </div>
    <div class="body">
      <h4>⚔️ Star Wars: Rise of the Resistance</h4>
      <p>ゆうしん向け最新・最人気。Millennium Falcon 見学も可能。開園ダッシュで Lightning Lane 最優先。</p>
      <span class="area">Star Wars: Galaxy\'s Edge</span>
    </div>
  </figure>'''
replacements.append(('d16 Rise of Resistance', OLD_RISE, NEW_RISE))

# it's a small world → small-world.jpg
OLD_SW = '''  <figure class="attr-card">
    <div class="thumb emoji pink">🧸<span class="badge-corner pri">みな実</span></div>
    <div class="body">
      <h4>it\'s a small world</h4>
      <p>世界の子供達のアニマトロニクス。涼しい屋内で昼休憩にも。</p>
      <span class="area">Fantasyland</span>
    </div>
  </figure>'''
NEW_SW = '''  <figure class="attr-card">
    <div class="thumb">
      <img src="images/small-world.jpg" alt="it\'s a small world facade" loading="lazy">
      <span class="badge-corner pri">みな実</span>
    </div>
    <div class="body">
      <h4>🧸 it\'s a small world</h4>
      <p>金色の装飾が美しいファサード。世界の子供達のアニマトロニクス。涼しい屋内で昼休憩にも。</p>
      <span class="area">Fantasyland</span>
    </div>
  </figure>'''
replacements.append(('d16 Small World', OLD_SW, NEW_SW))

# Haunted Mansion → haunted-mansion.jpg
OLD_HM = '''  <figure class="attr-card">
    <div class="thumb emoji dark">👻<span class="badge-corner">人気</span></div>
    <div class="body">
      <h4>Haunted Mansion</h4>
      <p>999人の幽霊が住む屋敷。怖すぎずジョーク多め。</p>
      <span class="area">New Orleans Square</span>
    </div>
  </figure>'''
NEW_HM = '''  <figure class="attr-card">
    <div class="thumb">
      <img src="images/haunted-mansion.jpg" alt="Haunted Mansion exterior" loading="lazy">
      <span class="badge-corner">人気</span>
    </div>
    <div class="body">
      <h4>👻 Haunted Mansion</h4>
      <p>999人の幽霊が住む屋敷。怖すぎずジョーク多め。</p>
      <span class="area">New Orleans Square</span>
    </div>
  </figure>'''
replacements.append(('d16 Haunted Mansion', OLD_HM, NEW_HM))

# Tiana's Bayou Adventure → tianas-bayou.jpg
OLD_TB = '''  <figure class="attr-card">
    <div class="thumb emoji green">🐰<span class="badge-corner">新</span></div>
    <div class="body">
      <h4>Tiana\'s Bayou Adventure</h4>
      <p>旧スプラッシュマウンテンを改装。水しぶきに注意（ポンチョ推奨）。</p>
      <span class="area">Critter Country</span>
    </div>
  </figure>'''
NEW_TB = '''  <figure class="attr-card">
    <div class="thumb">
      <img src="images/tianas-bayou.jpg" alt="Splash Mountain final drop" loading="lazy">
      <span class="badge-corner">新</span>
    </div>
    <div class="body">
      <h4>🐰 Tiana\'s Bayou Adventure</h4>
      <p>旧スプラッシュマウンテンを改装。急降下あり、水しぶきに注意（ポンチョ推奨）。</p>
      <span class="area">Critter Country</span>
    </div>
  </figure>'''
replacements.append(('d16 Tiana\'s Bayou', OLD_TB, NEW_TB))

# Indiana Jones Adventure → indy-adventure.jpg
OLD_IJ = '''  <figure class="attr-card">
    <div class="thumb emoji orange">🗡️<span class="badge-corner">絶叫</span></div>
    <div class="body">
      <h4>Indiana Jones Adventure</h4>
      <p>ジープで古代寺院探検。スリル系ファンに。</p>
      <span class="area">Adventureland</span>
    </div>
  </figure>'''
NEW_IJ = '''  <figure class="attr-card">
    <div class="thumb">
      <img src="images/indy-adventure.jpg" alt="Indiana Jones Adventure queue" loading="lazy">
      <span class="badge-corner">絶叫</span>
    </div>
    <div class="body">
      <h4>🗡️ Indiana Jones Adventure</h4>
      <p>ジープで古代寺院探検。スリル系ファンに。Adventureland のジャングル雰囲気。</p>
      <span class="area">Adventureland</span>
    </div>
  </figure>'''
replacements.append(('d16 Indiana Jones', OLD_IJ, NEW_IJ))

# ============ d15 の残り emoji カード（Guardians, WEB SLINGERS, Pixar Pal, Pirates Lair, Animation Building）============
# Guardians → 新 guardians-breakout.jpg が無いのでそのまま

# Pixar Pal-A-Round → pixar-pier.jpg (Paradise Pier Hotel)
OLD_PPR = '''  <figure class="attr-card">
    <div class="thumb emoji pink">🎡<span class="badge-corner pri">景色</span></div>
    <div class="body">
      <h4>Pixar Pal-A-Round</h4>
      <p>旧 Mickey\'s Fun Wheel。海沿いの大観覧車。固定 or 揺れるゴンドラ選択可。</p>
      <span class="area">Pixar Pier</span>
    </div>
  </figure>'''
NEW_PPR = '''  <figure class="attr-card">
    <div class="thumb">
      <img src="images/pixar-pier.jpg" alt="Paradise Pier area" loading="lazy">
      <span class="badge-corner pri">景色</span>
    </div>
    <div class="body">
      <h4>🎡 Pixar Pal-A-Round</h4>
      <p>旧 Mickey\'s Fun Wheel。海沿いの大観覧車。固定 or 揺れるゴンドラ選択可。</p>
      <span class="area">Pixar Pier</span>
    </div>
  </figure>'''
replacements.append(('d15 Pixar Pal-A-Round', OLD_PPR, NEW_PPR))

# 適用
applied = 0
for label, old, new in replacements:
    if old in html:
        html = html.replace(old, new)
        print(f'  ✅ {label}')
        applied += 1
    else:
        print(f'  -- {label}: 見つからない')

PATH.write_text(html, encoding='utf-8')
print(f'\n=== {applied}/{len(replacements)} 適用 (size={len(html):,}B) ===')
