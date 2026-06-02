"""d16 「🎢 Disneyland Park 必訪アトラクション」を画像付きカードに置換。"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path

PATH = Path(r'C:/Users/kyosu/worldカップ旅行/travel-guide-v7.html')
html = PATH.read_text(encoding='utf-8')

# CSSを追加（絵文字カード用）
ATTR_CSS = '''
/* ============ ATTRACTION CARD ============ */
.attr-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px;margin:14px 0 24px}
.attr-card{position:relative;border-radius:12px;overflow:hidden;box-shadow:var(--shadow-sm);background:var(--card);border:1px solid var(--border);display:flex;flex-direction:column;transition:.2s}
.attr-card:hover{transform:translateY(-3px);box-shadow:var(--shadow)}
.attr-card .thumb{position:relative;aspect-ratio:4/3;overflow:hidden;background:var(--border-l)}
.attr-card .thumb img{width:100%;height:100%;object-fit:cover}
.attr-card .thumb.emoji{display:flex;align-items:center;justify-content:center;font-size:72px;background:linear-gradient(135deg,var(--primary-l) 0%,var(--accent) 100%);color:#fff;text-shadow:0 2px 12px rgba(0,0,0,.25)}
.attr-card .thumb.emoji.pink{background:linear-gradient(135deg,#ec4899 0%,#f472b6 100%)}
.attr-card .thumb.emoji.purple{background:linear-gradient(135deg,#7c3aed 0%,#a855f7 100%)}
.attr-card .thumb.emoji.orange{background:linear-gradient(135deg,#ea580c 0%,#fb923c 100%)}
.attr-card .thumb.emoji.green{background:linear-gradient(135deg,#059669 0%,#34d399 100%)}
.attr-card .thumb.emoji.dark{background:linear-gradient(135deg,#1f2937 0%,#4b5563 100%)}
.attr-card .thumb .badge-corner{position:absolute;top:8px;right:8px;background:var(--accent);color:#fff;font-family:var(--font-mono);font-size:10px;font-weight:700;padding:3px 8px;border-radius:4px;letter-spacing:.05em;box-shadow:0 2px 6px rgba(0,0,0,.25)}
.attr-card .thumb .badge-corner.gold{background:var(--gold)}
.attr-card .thumb .badge-corner.pri{background:var(--primary)}
.attr-card .body{padding:12px 14px;flex:1;display:flex;flex-direction:column;gap:4px}
.attr-card .body h4{font-family:var(--font-serif);font-size:14.5px;color:var(--primary);font-weight:700;margin:0;line-height:1.3}
.attr-card .body p{font-size:11.5px;color:var(--ink-l);margin:0;line-height:1.55}
.attr-card .body .area{font-family:var(--font-mono);font-size:10px;color:var(--muted);letter-spacing:.06em;text-transform:uppercase;margin-top:4px}
'''
if '.attr-grid{' not in html:
    html = html.replace('</style>', ATTR_CSS + '\n</style>', 1)
    print('+ CSS added')

# d16 の古い必訪アトラクション grid を探して置換
OLD = '''<h2>🎢 Disneyland Park 必訪アトラクション</h2>
<div class="grid grid-2">
  <div class="card accent"><h4>🏰 Sleeping Beauty Castle</h4><p class="small">定番撮影スポット・パーク中央</p></div>
  <div class="card"><h4>🏴‍☠️ Pirates of the Caribbean</h4><p class="small">カリブの海賊・全年齢</p></div>
  <div class="card gold"><h4>⚔️ Star Wars: Rise of the Resistance ⭐</h4><p class="small">ゆうしん向け最新・最人気・朝一番で</p></div>
  <div class="card"><h4>🎢 Space Mountain</h4><p class="small">スペースマウンテン</p></div>
  <div class="card"><h4>🐘 Jungle Cruise</h4><p class="small">ジャングルクルーズ</p></div>
  <div class="card"><h4>🧸 it\'s a small world</h4><p class="small">みな実向け定番</p></div>
  <div class="card"><h4>🏔️ Matterhorn Bobsleds</h4><p class="small">マッターホルン</p></div>
  <div class="card"><h4>👻 Haunted Mansion</h4><p class="small">ホーンテッドマンション</p></div>
  <div class="card"><h4>🎡 Peter Pan\'s Flight</h4><p class="small">ピーター・パン</p></div>
  <div class="card"><h4>🎢 Big Thunder Mountain Railroad</h4><p class="small">ビッグサンダー・マウンテン</p></div>
  <div class="card"><h4>🐰 Tiana\'s Bayou Adventure</h4><p class="small">旧スプラッシュマウンテン</p></div>
  <div class="card"><h4>🗡️ Indiana Jones Adventure</h4><p class="small">インディ・ジョーンズ</p></div>
</div>'''

NEW = '''<h2>🎢 Disneyland Park 必訪アトラクション</h2>
<div class="attr-grid">

  <figure class="attr-card">
    <div class="thumb">
      <img src="images/disneyland-castle.jpg" alt="Sleeping Beauty Castle" loading="lazy">
      <span class="badge-corner gold">MUST</span>
    </div>
    <div class="body">
      <h4>🏰 Sleeping Beauty Castle</h4>
      <p>パーク中央のシンボル。家族全員の記念撮影は必須。</p>
      <span class="area">Central Plaza</span>
    </div>
  </figure>

  <figure class="attr-card">
    <div class="thumb emoji dark">⚔️<span class="badge-corner">⭐ 朝一番</span></div>
    <div class="body">
      <h4>Star Wars: Rise of the Resistance</h4>
      <p>ゆうしん向け最新・最人気。開園ダッシュで Lightning Lane 最優先。</p>
      <span class="area">Star Wars: Galaxy\'s Edge</span>
    </div>
  </figure>

  <figure class="attr-card">
    <div class="thumb">
      <img src="images/space-mountain.jpg" alt="Space Mountain" loading="lazy">
      <span class="badge-corner">絶叫</span>
    </div>
    <div class="body">
      <h4>🎢 Space Mountain</h4>
      <p>暗闇の宇宙を駆ける定番屋内コースター。LL2番目推奨。</p>
      <span class="area">Tomorrowland</span>
    </div>
  </figure>

  <figure class="attr-card">
    <div class="thumb">
      <img src="images/pirates-caribbean.jpg" alt="Pirates of the Caribbean" loading="lazy">
      <span class="badge-corner pri">全年齢</span>
    </div>
    <div class="body">
      <h4>🏴‍☠️ Pirates of the Caribbean</h4>
      <p>カリブの海賊のアニマトロニクス船旅。Blue Bayou Restaurant 併設。</p>
      <span class="area">New Orleans Square</span>
    </div>
  </figure>

  <figure class="attr-card">
    <div class="thumb">
      <img src="images/matterhorn.jpg" alt="Matterhorn Bobsleds" loading="lazy">
      <span class="badge-corner">絶叫</span>
    </div>
    <div class="body">
      <h4>🏔️ Matterhorn Bobsleds</h4>
      <p>世界初のチューブラー鋼鉄コースター（1959年）。Yeti と雪山を駆け下りる。</p>
      <span class="area">Fantasyland</span>
    </div>
  </figure>

  <figure class="attr-card">
    <div class="thumb">
      <img src="images/big-thunder.jpg" alt="Big Thunder Mountain" loading="lazy">
      <span class="badge-corner">家族OK</span>
    </div>
    <div class="body">
      <h4>🎢 Big Thunder Mountain Railroad</h4>
      <p>西部開拓時代の鉱山鉄道。怖すぎず楽しめる。</p>
      <span class="area">Frontierland</span>
    </div>
  </figure>

  <figure class="attr-card">
    <div class="thumb">
      <img src="images/peter-pan.jpg" alt="Peter Pan's Flight" loading="lazy">
      <span class="badge-corner pri">みな実</span>
    </div>
    <div class="body">
      <h4>🧚 Peter Pan\'s Flight</h4>
      <p>ネバーランドへの空の旅。小さい子も楽しめる。Fantasyland 定番。</p>
      <span class="area">Fantasyland</span>
    </div>
  </figure>

  <figure class="attr-card">
    <div class="thumb">
      <img src="images/jungle-cruise.jpg" alt="Jungle Cruise" loading="lazy">
      <span class="badge-corner pri">全年齢</span>
    </div>
    <div class="body">
      <h4>🐘 Jungle Cruise</h4>
      <p>船長のジョークと動物でみんな笑える。ファミリー定番。</p>
      <span class="area">Adventureland</span>
    </div>
  </figure>

  <figure class="attr-card">
    <div class="thumb emoji pink">🧸<span class="badge-corner pri">みな実</span></div>
    <div class="body">
      <h4>it\'s a small world</h4>
      <p>世界の子供達のアニマトロニクス。涼しい屋内で昼休憩にも。</p>
      <span class="area">Fantasyland</span>
    </div>
  </figure>

  <figure class="attr-card">
    <div class="thumb emoji dark">👻<span class="badge-corner">人気</span></div>
    <div class="body">
      <h4>Haunted Mansion</h4>
      <p>999人の幽霊が住む屋敷。怖すぎずジョーク多め。</p>
      <span class="area">New Orleans Square</span>
    </div>
  </figure>

  <figure class="attr-card">
    <div class="thumb emoji green">🐰<span class="badge-corner">新</span></div>
    <div class="body">
      <h4>Tiana\'s Bayou Adventure</h4>
      <p>旧スプラッシュマウンテンを改装。水しぶきに注意（ポンチョ推奨）。</p>
      <span class="area">Critter Country</span>
    </div>
  </figure>

  <figure class="attr-card">
    <div class="thumb emoji orange">🗡️<span class="badge-corner">絶叫</span></div>
    <div class="body">
      <h4>Indiana Jones Adventure</h4>
      <p>ジープで古代寺院探検。スリル系ファンに。</p>
      <span class="area">Adventureland</span>
    </div>
  </figure>

</div>'''

if OLD in html:
    html = html.replace(OLD, NEW)
    print('+ d16 必訪アトラクション 12件を画像カード化')
else:
    print('  !! 既存ブロックが見つからない')

PATH.write_text(html, encoding='utf-8')
print(f'\n✅ size={len(html):,}B')
