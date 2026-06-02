"""v7.html の各日マップを Leaflet + OpenStreetMap（CartoDB Positron）に置換。
  実際の緯度経度でピンを配置し、タイルに透明度を付けてルートが際立つようにする。"""
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path

PATH = Path(r'C:/Users/kyosu/worldカップ旅行/travel-guide-v7.html')
html = PATH.read_text(encoding='utf-8')

# ============ 1. head に Leaflet CDN を追加 ============
LEAFLET_HEAD = '''<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" crossorigin=""/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" crossorigin=""></script>
'''
if 'leaflet.css' not in html:
    html = html.replace('</head>', LEAFLET_HEAD + '</head>')
    print('+ Leaflet CDN injected')

# ============ 2. CSS 追加 ============
LEAFLET_CSS = '''
/* ============ LEAFLET DAY MAP ============ */
.leaflet-map{height:440px;width:100%;max-width:720px;margin:0 auto 14px;border-radius:10px;border:1px solid var(--border);box-shadow:var(--shadow-sm);background:#eef2f5;position:relative;overflow:hidden}
@media(max-width:960px){.leaflet-map{height:360px}}
.leaflet-container{font-family:var(--font-sans) !important}
.leaflet-tile-pane{opacity:.7}
.leaflet-control-attribution{font-size:9px;background:rgba(255,255,255,.7)}
.day-pin-hub{background:#0f2c5e;color:#fff;border:3px solid #fff;border-radius:50%;width:42px;height:42px;display:flex;align-items:center;justify-content:center;font-size:19px;box-shadow:0 2px 8px rgba(0,0,0,.35)}
.day-pin-stop{background:#c94a3c;color:#fff;border:3px solid #fff;border-radius:50%;width:34px;height:34px;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:700;box-shadow:0 2px 8px rgba(0,0,0,.3);font-family:'Montserrat',sans-serif}
.day-pin-label{position:absolute;top:38px;left:50%;transform:translateX(-50%);white-space:nowrap;background:rgba(255,255,255,.95);padding:2px 7px;border-radius:4px;font-size:10.5px;color:#333;box-shadow:0 1px 3px rgba(0,0,0,.2);font-weight:600;border:1px solid #e8e3d9}
'''
if '.leaflet-map{' not in html:
    html = html.replace('</style>', LEAFLET_CSS + '\n</style>', 1)
    print('+ Leaflet CSS injected')

# ============ 3. 各日SVGを div に置換 ============
day_ids = ['d11','d12','d13','d14','d15','d16','d17','d18','d19']
replaced = 0
for day_id in day_ids:
    sec_start = html.find(f'<section id="{day_id}" class="page">')
    if sec_start < 0:
        print(f'  !! section {day_id} not found')
        continue
    nxt = html.find('<section id="', sec_start + 10)
    if nxt < 0:
        nxt = len(html)
    segment = html[sec_start:nxt]
    # SVG 部分を検索
    svg_start = segment.find('<svg viewBox="0 0 720 460" class="day-map-svg"')
    if svg_start < 0:
        print(f'  !! {day_id}: svg not found')
        continue
    svg_end = segment.find('</svg>', svg_start) + len('</svg>')
    svg_block = segment[svg_start:svg_end]
    new_div = f'<div id="lmap-{day_id}" class="leaflet-map" aria-label="この日のマップ"></div>'
    html = html.replace(svg_block, new_div, 1)
    replaced += 1
    print(f'  + {day_id} SVG → Leaflet div')

print(f'  {replaced}/9 day maps converted')

# ============ 4. 末尾にデータ + 初期化 JS を追加 ============
DAY_MAPS_JS = '''
<script>
(function(){
  if (typeof L === 'undefined') { console.warn('Leaflet not loaded'); return; }

  // 緯度経度データ（実測値）
  var DAY_MAPS = {
    d11: {
      pins: [
        {type:'hub', name:'Marriott Marquis', lat:40.7589, lng:-73.9851},
        {type:'stop', n:1, time:'15:20', name:'ダコタハウス', lat:40.7762, lng:-73.9760},
        {type:'stop', n:2, time:'15:35', name:'ストロベリーフィールズ', lat:40.7756, lng:-73.9751},
        {type:'stop', n:3, time:'16:30', name:'Top of the Rock', lat:40.7587, lng:-73.9787},
        {type:'stop', n:4, time:'17:30', name:'FAO Schwarz', lat:40.7640, lng:-73.9731}
      ],
      routes: [
        {from:0, to:1, mode:'subway', label:'🚇 地下鉄 15分'},
        {from:1, to:2, mode:'walk', label:'🚶 徒歩 1分'},
        {from:2, to:0, mode:'subway', label:'🚇 地下鉄 15分'},
        {from:0, to:3, mode:'walk', label:'🚶 徒歩 5分'},
        {from:3, to:4, mode:'walk', label:'🚶 徒歩 3分'},
        {from:4, to:0, mode:'walk', label:'🚶 徒歩 8分'}
      ]
    },
    d12: {
      pins: [
        {type:'hub', name:'Marriott Marquis', lat:40.7589, lng:-73.9851},
        {type:'stop', n:1, time:'07:00', name:'Best Bagel & Coffee', lat:40.7537, lng:-73.9901},
        {type:'stop', n:2, time:'10:00', name:'自由の女神（Battery Park集合）', lat:40.7033, lng:-74.0170},
        {type:'stop', n:3, time:'12:00', name:'Ellis Island', lat:40.6995, lng:-74.0396},
        {type:'stop', n:4, time:'13:30', name:'Locanda Verde', lat:40.7207, lng:-74.0101},
        {type:'stop', n:5, time:'15:20', name:'DUMBO（ワンス・アポン・ア・タイム）', lat:40.7032, lng:-73.9886},
        {type:'stop', n:6, time:'16:30', name:"Old St. Patrick's Cathedral", lat:40.7235, lng:-73.9950},
        {type:'stop', n:7, time:'16:45', name:'128 Mott St（メッツビル）', lat:40.7187, lng:-73.9976},
        {type:'stop', n:8, time:'16:55', name:'137 Mott St（果物店）', lat:40.7190, lng:-73.9974},
        {type:'stop', n:9, time:'17:05', name:'Mulberry Street Bar', lat:40.7196, lng:-73.9967},
        {type:'stop', n:10, time:'21:09', name:'EWR 空港', lat:40.6895, lng:-74.1745}
      ],
      routes: [
        {from:0, to:1, mode:'walk', label:'🚶 徒歩 8分'},
        {from:1, to:0, mode:'walk', label:'🚶 徒歩 8分'},
        {from:0, to:2, mode:'uber', label:'🚕 Uber XL 45分'},
        {from:2, to:3, mode:'ferry', label:'⛴ フェリー'},
        {from:3, to:4, mode:'uber', label:'🚕 Uber 10分'},
        {from:4, to:5, mode:'uber', label:'🚕 Uber 15分'},
        {from:5, to:6, mode:'uber', label:'🚕 Uber 15分'},
        {from:6, to:7, mode:'walk', label:'🚶 徒歩 2分'},
        {from:7, to:8, mode:'walk', label:'🚶 徒歩 1分'},
        {from:8, to:9, mode:'walk', label:'🚶 徒歩 2分'},
        {from:9, to:0, mode:'uber', label:'🚕 Uber 30分（ホテル戻り）'},
        {from:0, to:10, mode:'uber', label:'🚕 Uber XL 60分'}
      ]
    },
    d13: {
      pins: [
        {type:'hub', name:'Courtyard Arlington', lat:32.7541, lng:-97.0845},
        {type:'stop', n:1, time:'10:00', name:'Six Flags Over Texas', lat:32.7558, lng:-97.0706},
        {type:'stop', n:2, time:'14:30', name:'Hurricane Harbor', lat:32.7620, lng:-97.0793},
        {type:'stop', n:3, time:'19:45', name:'Pappadeaux Seafood', lat:32.7478, lng:-97.0888}
      ],
      routes: [
        {from:0, to:1, mode:'walk', label:'🚶 徒歩 22分'},
        {from:1, to:0, mode:'walk', label:'🚶 徒歩 22分'},
        {from:0, to:2, mode:'walk', label:'🚶 徒歩 12分'},
        {from:2, to:0, mode:'walk', label:'🚶 徒歩 12分'},
        {from:0, to:3, mode:'walk', label:'🚶 徒歩 10分'}
      ]
    },
    d14: {
      pins: [
        {type:'hub', name:'Courtyard Arlington', lat:32.7541, lng:-97.0845},
        {type:'stop', n:1, time:'09:30', name:'Globe Life Field', lat:32.7473, lng:-97.0817},
        {type:'stop', n:2, time:'12:30', name:'AT&T Stadium（Block 440）', lat:32.7478, lng:-97.0929}
      ],
      routes: [
        {from:0, to:1, mode:'walk', label:'🚶 徒歩 20分'},
        {from:1, to:2, mode:'walk', label:'🚶 徒歩 10分'},
        {from:2, to:0, mode:'walk', label:'🚶 徒歩 25分（試合後）'}
      ]
    },
    d15: {
      pins: [
        {type:'hub', name:'Courtyard Arlington', lat:32.7541, lng:-97.0845},
        {type:'stop', n:1, time:'07:30', name:'DAL Love Field', lat:32.8471, lng:-96.8518},
        {type:'stop', n:2, time:'12:50', name:'SNA Orange County', lat:33.6762, lng:-117.8675},
        {type:'stop', n:3, time:'14:30', name:'Courtyard Anaheim', lat:33.8047, lng:-117.9191}
      ],
      routes: [
        {from:0, to:1, mode:'uber', label:'🚕 Uber 30分'},
        {from:1, to:2, mode:'flight', label:'✈️ Southwest 5h5m（DEN乗継）'},
        {from:2, to:3, mode:'uber', label:'🚕 Uber XL 25分'}
      ]
    },
    d16: {
      pins: [
        {type:'hub', name:'Courtyard Anaheim', lat:33.8047, lng:-117.9191},
        {type:'stop', n:1, time:'午後', name:'Downtown Disney', lat:33.8094, lng:-117.9214}
      ],
      routes: [
        {from:0, to:1, mode:'walk', label:'🚶 徒歩 5分'},
        {from:1, to:0, mode:'walk', label:'🚶 徒歩 5分'}
      ]
    },
    d17: {
      pins: [
        {type:'hub', name:'Courtyard Anaheim（朝出発）', lat:33.8047, lng:-117.9191},
        {type:'stop', n:1, time:'09:00', name:'Disneyland Park', lat:33.8121, lng:-117.9190},
        {type:'stop', n:2, time:'22:00', name:'Marriott Marina del Rey', lat:33.9791, lng:-118.4516}
      ],
      routes: [
        {from:0, to:1, mode:'walk', label:'🚶 徒歩 5分'},
        {from:1, to:0, mode:'walk', label:'🚶 徒歩 5分（夜）'},
        {from:0, to:2, mode:'uber', label:'🚕 Uber XL 45-60分・$95-125'}
      ]
    },
    d18: {
      pins: [
        {type:'hub', name:'Marriott Marina del Rey', lat:33.9791, lng:-118.4516},
        {type:'stop', n:0, time:'08:00', name:'Enterprise（Range Roverピックアップ）', lat:33.9850, lng:-118.4512},
        {type:'stop', n:1, time:'09:45', name:'Hollywood Walk of Fame', lat:34.1016, lng:-118.3416},
        {type:'stop', n:2, time:'10:00', name:'TCL Chinese Theatre', lat:34.1022, lng:-118.3410},
        {type:'stop', n:3, time:'10:30', name:'Hollywood Sign ビュー（Ovation）', lat:34.1018, lng:-118.3408},
        {type:'stop', n:4, time:'11:30', name:'In-N-Out Hollywood', lat:34.0983, lng:-118.3365},
        {type:'stop', n:5, time:'13:00', name:'The Grove', lat:34.0725, lng:-118.3576},
        {type:'stop', n:6, time:'14:30', name:'Griffith Observatory', lat:34.1184, lng:-118.3004},
        {type:'stop', n:7, time:'16:30', name:'Costco Marina Marketplace', lat:33.9832, lng:-118.4360},
        {type:'stop', n:8, time:'17:30', name:'Enterprise 返却', lat:33.9850, lng:-118.4512},
        {type:'stop', n:9, time:'19:30', name:'Killer Shrimp', lat:33.9785, lng:-118.4526}
      ],
      routes: [
        {from:0, to:1, mode:'uber', label:'🚕 Uber 5分'},
        {from:1, to:2, mode:'car', label:'🚗 Range Rover 35分'},
        {from:2, to:3, mode:'walk', label:'🚶 徒歩 2分'},
        {from:3, to:4, mode:'car', label:'🚗 10分'},
        {from:4, to:5, mode:'car', label:'🚗 5分'},
        {from:5, to:6, mode:'car', label:'🚗 15分'},
        {from:6, to:7, mode:'car', label:'🚗 25分'},
        {from:7, to:8, mode:'car', label:'🚗 30分'},
        {from:8, to:9, mode:'car', label:'🚗 5分'},
        {from:9, to:0, mode:'uber', label:'🚕 Uber 5分'},
        {from:0, to:10, mode:'walk', label:'🚶 徒歩 5分'}
      ]
    },
    d19: {
      pins: [
        {type:'hub', name:'Marriott Marina del Rey', lat:33.9791, lng:-118.4516},
        {type:'stop', n:1, time:'08:00', name:'LAX 空港', lat:33.9425, lng:-118.4081},
        {type:'stop', n:2, time:'翌14:00', name:'羽田 HND（機中泊）', lat:35.5494, lng:139.7798}
      ],
      routes: [
        {from:0, to:1, mode:'uber', label:'🚕 Uber XL 20分'},
        {from:1, to:2, mode:'flight', label:'✈️ Delta DL0007 11時間40分'}
      ]
    }
  };

  var MODE_STYLE = {
    walk:    {color:'#059669', weight:4, dashArray:'3 6'},
    subway:  {color:'#1e4a8f', weight:5},
    uber:    {color:'#f97316', weight:4, dashArray:'10 6'},
    car:     {color:'#c94a3c', weight:5},
    flight:  {color:'#0f2c5e', weight:3, dashArray:'12 7'},
    ferry:   {color:'#0891b2', weight:3, dashArray:'5 4'}
  };

  function hubIcon() {
    return L.divIcon({
      html: '<div class="day-pin-hub">🏨</div>',
      className: '',
      iconSize: [42, 42],
      iconAnchor: [21, 21]
    });
  }
  function stopIcon(n) {
    return L.divIcon({
      html: '<div class="day-pin-stop">' + n + '</div>',
      className: '',
      iconSize: [34, 34],
      iconAnchor: [17, 17]
    });
  }

  var initialized = {};
  function initMap(dayId) {
    if (initialized[dayId]) {
      try { initialized[dayId].invalidateSize(); } catch(e){}
      return;
    }
    var cfg = DAY_MAPS[dayId];
    var el = document.getElementById('lmap-' + dayId);
    if (!cfg || !el) return;

    var map = L.map(el, {
      scrollWheelZoom: false,
      zoomControl: true,
      attributionControl: true
    });

    // CartoDB Positron（淡色タイル・透明度込みで下地として見やすい）
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
      attribution: '© OpenStreetMap · © CARTO',
      maxZoom: 18,
      subdomains: 'abcd'
    }).addTo(map);

    var bounds = [];
    cfg.pins.forEach(function(p) {
      var icon = p.type === 'hub' ? hubIcon() : stopIcon(p.n);
      var m = L.marker([p.lat, p.lng], {icon: icon, title: p.name}).addTo(map);
      var popup = '<div style="font-size:13px;line-height:1.5">' +
        (p.type === 'hub' ? '🏨 <strong>' + p.name + '</strong>（出発・帰着）' :
         '<strong>' + p.n + '</strong> ' + (p.time ? '<span style="color:#666">'+p.time+'</span> ' : '') + p.name) +
        '</div>';
      m.bindPopup(popup);
      bounds.push([p.lat, p.lng]);
    });

    cfg.routes.forEach(function(r) {
      var a = cfg.pins[r.from];
      var b = cfg.pins[r.to];
      if (!a || !b) return;
      var style = MODE_STYLE[r.mode] || {color:'#999', weight:3};
      var poly = L.polyline([[a.lat, a.lng], [b.lat, b.lng]], Object.assign({opacity: 0.82}, style)).addTo(map);
      poly.bindTooltip(r.label, {permanent:false, direction:'center', className:'rte-tooltip'});
    });

    if (bounds.length > 1) {
      map.fitBounds(bounds, {padding: [30, 30], maxZoom: 15});
    }
    initialized[dayId] = map;
  }

  // showPage 切替時にマップを初期化／再描画
  function onShow() {
    var active = document.querySelector('.page.active');
    if (!active) return;
    if (DAY_MAPS[active.id]) {
      setTimeout(function(){ initMap(active.id); }, 120);
    }
  }
  // ページ class 変更を監視
  var obs = new MutationObserver(onShow);
  obs.observe(document.body, {attributes:true, subtree:true, attributeFilter:['class']});
  window.addEventListener('load', onShow);
})();
</script>
'''

if 'DAY_MAPS = {' not in html:
    html = html.replace('</body>', DAY_MAPS_JS + '</body>')
    print('+ DAY_MAPS JS injected')

# ============ 5. 使われなくなった transport-key を各マップから残しておく（凡例として便利）============
# もとの SVG 下にあった <div class="transport-key"> は残すので、そのまま

PATH.write_text(html, encoding='utf-8')
print(f'\n✅ saved  size={len(html):,}B')
