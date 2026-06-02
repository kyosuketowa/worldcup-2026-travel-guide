"""Disney (d15, d16) のページを画像とコンテンツで充実させる。"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path

PATH = Path(r'C:/Users/kyosu/worldカップ旅行/travel-guide-v7.html')
html = PATH.read_text(encoding='utf-8')

# ========= d15: 既存の「📸 本日のスポット（California Adventure）」ギャラリーを刷新 =========
OLD_D15 = '''<h2>📸 本日のスポット（California Adventure）</h2>
<div class="place-gallery">
  <figure class="place-card"><img src="images/disneyland-castle.jpg" alt="Disney Resort" loading="lazy"><figcaption><strong>Disney California Adventure</strong><span class="jp">ピクサー・カーズ・マーベル</span><span class="tag">🎡 14:30</span></figcaption></figure>
  <figure class="place-card"><img src="images/airplane.jpg" alt="Flight DAL-SNA" loading="lazy"><figcaption><strong>DAL → SNA</strong><span class="jp">Southwest 5時間5分（DEN乗継）</span><span class="tag">✈️ 09:45</span></figcaption></figure>
</div>'''

NEW_D15_GALLERY = '''<h2>📸 カリフォルニア・アドベンチャーの見どころ</h2>
<div class="place-gallery">
  <figure class="place-card wide"><img src="images/dca-entrance.jpg" alt="Disney California Adventure" loading="lazy"><figcaption><strong>Disney California Adventure</strong><span class="jp">ピクサー・カーズ・マーベル・ピア</span><span class="tag">🎡 14:30 入園</span></figcaption></figure>
  <figure class="place-card"><img src="images/radiator-springs.jpg" alt="Radiator Springs Racers" loading="lazy"><figcaption><strong>Radiator Springs Racers</strong><span class="jp">「カーズ」世界のスピード対決レース</span><span class="tag">🚗 15:00</span></figcaption></figure>
  <figure class="place-card"><img src="images/world-of-color.jpg" alt="World of Color" loading="lazy"><figcaption><strong>World of Color ⭐</strong><span class="jp">噴水と光と炎の夜のナイトショー</span><span class="tag">🎭 21:00</span></figcaption></figure>
  <figure class="place-card"><img src="images/mickey-mouse.jpg" alt="Mickey" loading="lazy"><figcaption><strong>Mickey &amp; Friends</strong><span class="jp">キャラクターグリーティング</span><span class="tag">📸 各所</span></figcaption></figure>
</div>

<h2>🎢 California Adventure 必訪アトラクション</h2>
<div class="grid grid-2">
  <div class="card accent"><h4>🎢 Guardians of the Galaxy – Mission: BREAKOUT!</h4><p class="small">絶叫系・旧 Tower of Terror を改装・高さ55m・急降下</p></div>
  <div class="card accent"><h4>🚗 Radiator Springs Racers</h4><p class="small">Cars ファミリー向け・屋外レース・Lightning Lane 必須</p></div>
  <div class="card"><h4>🕷️ WEB SLINGERS: A Spider-Man Adventure</h4><p class="small">インタラクティブシューティング・Avengers Campus</p></div>
  <div class="card"><h4>🧚 Pixar Pal-A-Round（旧 Mickey\'s Fun Wheel）</h4><p class="small">海沿いの大観覧車・固定 or 揺れる選択可</p></div>
  <div class="card gold"><h4>🎭 World of Color ⭐</h4><p class="small">夜の噴水ショー（必見・21:00頃・Paradise Bay）</p></div>
  <div class="card"><h4>🌶️ Cars Land</h4><p class="small">Radiator Springs 街並み再現・「カーズ」の世界</p></div>
  <div class="card"><h4>🏴‍☠️ Pirates Lair on Tom Sawyer Island</h4><p class="small">子供大喜び・探検型アトラクション</p></div>
  <div class="card"><h4>🎬 Disney Animation Building</h4><p class="small">Turtle Talk with Crush ・Sorcerer\'s Workshop</p></div>
</div>

<h2>🍴 California Adventure の絶対食べたいもの</h2>
<div class="grid grid-3">
  <div class="card"><h4>🌶️ Cozy Cone Motel</h4><p class="small">Cars Land のコーン型フードスタンド・チリ・チーズ・ポップコーン</p></div>
  <div class="card"><h4>🥨 Corndog Castle</h4><p class="small">Pixar Pier の巨大コーンドッグ（Paradise Garden）</p></div>
  <div class="card"><h4>🍦 Ghirardelli Soda Fountain</h4><p class="small">Downtown Disney 側・サンフランシスコ発の老舗チョコ店</p></div>
</div>
'''

if OLD_D15 in html:
    html = html.replace(OLD_D15, NEW_D15_GALLERY)
    print('+ d15 ギャラリー + アトラクション + 食事 を拡充')
else:
    print('  !! d15 既存ギャラリーが見つからない')

# ========= d16: Disneyland Park ページの既存ギャラリーを大幅拡充 =========
OLD_D16 = '''<h2>📸 本日のスポット（Disneyland Park）</h2>
<div class="place-gallery">
  <figure class="place-card"><img src="images/disneyland-castle.jpg" alt="Sleeping Beauty Castle" loading="lazy"><figcaption><strong>Sleeping Beauty Castle</strong><span class="jp">Disneyland のシンボル</span><span class="tag">🏰 開園</span></figcaption></figure>
</div>

<h2>Uber費用まとめ / Uber Cost</h2>'''

NEW_D16 = '''<h2>📸 Disneyland Park の見どころ</h2>
<div class="place-gallery">
  <figure class="place-card wide"><img src="images/disneyland-castle.jpg" alt="Sleeping Beauty Castle" loading="lazy"><figcaption><strong>Sleeping Beauty Castle</strong><span class="jp">パーク中央のシンボル・絶対撮影スポット</span><span class="tag">🏰 9:00 開園</span></figcaption></figure>
  <figure class="place-card"><img src="images/space-mountain.jpg" alt="Space Mountain" loading="lazy"><figcaption><strong>Space Mountain</strong><span class="jp">Tomorrowland の超定番絶叫</span><span class="tag">🎢 朝一番</span></figcaption></figure>
  <figure class="place-card"><img src="images/pirates-caribbean.jpg" alt="Pirates of the Caribbean" loading="lazy"><figcaption><strong>Pirates of the Caribbean</strong><span class="jp">全年齢向け・Blue Bayou 併設</span><span class="tag">🏴‍☠️ 昼</span></figcaption></figure>
  <figure class="place-card"><img src="images/matterhorn.jpg" alt="Matterhorn Bobsleds" loading="lazy"><figcaption><strong>Matterhorn Bobsleds</strong><span class="jp">世界初のチューブラー鋼鉄コースター</span><span class="tag">🏔️</span></figcaption></figure>
  <figure class="place-card"><img src="images/big-thunder.jpg" alt="Big Thunder Mountain" loading="lazy"><figcaption><strong>Big Thunder Mountain</strong><span class="jp">西部開拓の鉱山鉄道</span><span class="tag">🎢</span></figcaption></figure>
  <figure class="place-card"><img src="images/peter-pan.jpg" alt="Peter Pan\'s Flight" loading="lazy"><figcaption><strong>Peter Pan\'s Flight</strong><span class="jp">ネバーランドへ空の旅</span><span class="tag">🧚 ファンタジーランド</span></figcaption></figure>
  <figure class="place-card"><img src="images/jungle-cruise.jpg" alt="Jungle Cruise" loading="lazy"><figcaption><strong>Jungle Cruise</strong><span class="jp">船長のジョークと動物で笑える旅</span><span class="tag">🐘 Adventureland</span></figcaption></figure>
  <figure class="place-card"><img src="images/dole-whip.jpg" alt="Dole Whip" loading="lazy"><figcaption><strong>Dole Whip 🍍</strong><span class="jp">パイナップルのソフトクリーム（Adventureland）</span><span class="tag">🍦 名物</span></figcaption></figure>
  <figure class="place-card"><img src="images/fireworks.jpg" alt="Fireworks" loading="lazy"><figcaption><strong>Wondrous Journeys 花火</strong><span class="jp">お城の前で見る夜の特大ショー</span><span class="tag">🎆 21:00</span></figcaption></figure>
</div>

<h2>🍴 Disneyland Park の絶対食べたいもの</h2>
<div class="grid grid-3">
  <div class="card gold"><h4>🍗 Plaza Inn フライドチキン</h4><p class="small">Main Street・老舗の名物フライドチキン・ランチに最適</p></div>
  <div class="card gold"><h4>🍛 Blue Bayou Restaurant ⭐</h4><p class="small">Pirates of the Caribbean 内・予約必須の人気店・Monte Cristo</p></div>
  <div class="card"><h4>🍍 Dole Whip（Tiki Juice Bar）</h4><p class="small">Adventureland 名物・パイナップルソフト・行列必至</p></div>
  <div class="card"><h4>🥨 Mickey Pretzel</h4><p class="small">ミッキー形プレッツェル・手軽なおやつ</p></div>
  <div class="card"><h4>🍚 Rancho del Zocalo</h4><p class="small">Frontierland・本格メキシカン・ブリトー/タコス</p></div>
  <div class="card"><h4>🥐 Jolly Holiday Bakery</h4><p class="small">Main Street・Mary Poppins テーマ・朝食にも</p></div>
</div>

<h2>🎪 パレード・花火・ショー</h2>
<div class="grid grid-2">
  <div class="card accent">
    <h4>🎪 Magic Happens（マジック・ハプンズ）</h4>
    <p class="small"><strong>14:00頃 · Main Street</strong></p>
    <p class="small">最新パレード。Moana、Coco、Frozen など現代ディズニーのキャラが大集合。おすすめ観覧場所: Town Square の Walt Disney 像前・開始30分前確保</p>
  </div>
  <div class="card accent">
    <h4>🎆 Wondrous Journeys（花火）</h4>
    <p class="small"><strong>21:00 · Sleeping Beauty Castle</strong></p>
    <p class="small">Main Street とお城前が特等席。ただし大混雑なので <strong>20:00には場所取り</strong>推奨。夜ショー後は約30分退場</p>
  </div>
  <div class="card">
    <h4>🌊 Fantasmic!</h4>
    <p class="small"><strong>夜・Rivers of America</strong></p>
    <p class="small">ミッキーの夢・水・火・光のショー（上演日要確認）</p>
  </div>
  <div class="card">
    <h4>🎵 Mickey & the Magical Map</h4>
    <p class="small"><strong>昼・Fantasyland Theatre</strong></p>
    <p class="small">屋内ミュージカル・涼しいので昼休憩に最適</p>
  </div>
</div>

<h2>👋 キャラクターグリーティング</h2>
<div class="card">
  <p>Disneyland アプリで当日のキャラクター出現時間・場所が確認できる。</p>
  <ul class="simple" style="padding-left:22px">
    <li>🐭 <strong>Mickey Mouse</strong> - Town Square（Main Street入口）</li>
    <li>👸 <strong>プリンセス</strong> - Fantasy Faire（Fantasyland奥）</li>
    <li>🐻 <strong>Winnie the Pooh</strong> - Critter Country</li>
    <li>🧝 <strong>Tinker Bell</strong> - Pixie Hollow</li>
    <li>⚔️ <strong>Star Wars キャラ</strong> - Star Wars: Galaxy\'s Edge</li>
    <li>🏴‍☠️ <strong>Jack Sparrow</strong> - New Orleans Square（不定期）</li>
  </ul>
</div>

<h2>🛍️ お土産購入のコツ</h2>
<div class="grid grid-2">
  <div class="card">
    <h4>🎩 Main Street Emporium</h4>
    <p class="small">Main Street入口の最大ショップ・閉園まで営業・帰り際にまとめ買い可</p>
  </div>
  <div class="card">
    <h4>🏰 Castle 付近の小ショップ</h4>
    <p class="small">プリンセス関連グッズが集中（みな実向け）</p>
  </div>
  <div class="card">
    <h4>⚔️ Dok-Ondar\'s Den of Antiquities</h4>
    <p class="small">Star Wars グッズ特化・ライトセーバー自作可（要予約・有料$250）</p>
  </div>
  <div class="card">
    <h4>📦 Package Express</h4>
    <p class="small">買った物をパーク出口に届けてくれる無料サービス・荷物持ち歩き不要</p>
  </div>
</div>

<h2>💡 ディズニー訪問のコツ</h2>
<div class="grid grid-2">
  <div class="card warn">
    <h4>⏰ 開園30分前にゲート</h4>
    <p class="small">Rope Drop（開園ダッシュ）で朝一の Star Wars: Rise of the Resistance を狙う</p>
  </div>
  <div class="card warn">
    <h4>📱 モバイルバッテリー必須</h4>
    <p class="small">Disneyland アプリを1日中使う・バッテリー切れ厳禁</p>
  </div>
  <div class="card warn">
    <h4>🧴 サンスクリーン・帽子</h4>
    <p class="small">6月のアナハイムは暑い・SPF50・水分補給こまめに</p>
  </div>
  <div class="card warn">
    <h4>👟 歩きやすい靴</h4>
    <p class="small">1日で10km以上歩く・スニーカー必須</p>
  </div>
</div>

<h2>Uber費用まとめ / Uber Cost</h2>'''

if OLD_D16 in html:
    html = html.replace(OLD_D16, NEW_D16)
    print('+ d16 大幅拡充（ギャラリー9枚 + 食事 + ショー + キャラ + 土産 + tips）')
else:
    print('  !! d16 既存ギャラリー/Uberブロックが見つからない')

PATH.write_text(html, encoding='utf-8')
print(f'\n✅ saved  size={len(html):,}B')
