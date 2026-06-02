"""Disney California Adventure + Disneyland Park の写真を Wikipedia から取得。"""
import sys, io, urllib.request, os, json, time
from PIL import Image
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = r'C:/Users/kyosu/worldカップ旅行/images'
HDRS = {
    'User-Agent': 'MorishitaTravelGuide/1.0 (contact: beat.kyosuke.0226@gmail.com)',
    'Accept': 'application/json,image/*',
}

def fetch_bytes(url):
    r = urllib.request.urlopen(urllib.request.Request(url, headers=HDRS), timeout=30)
    return r.read(), r.headers.get('Content-Type','')

def fetch_json(url):
    return json.loads(fetch_bytes(url)[0].decode('utf-8'))

def is_img(data):
    if len(data) < 12: return False
    if data[:3] == b'\xff\xd8\xff': return True
    if data[:8].startswith(b'\x89PNG'): return True
    if data[:4] == b'RIFF' and data[8:12] == b'WEBP': return True
    return False

def resize_save(data, out_path, max_w=1400):
    im = Image.open(io.BytesIO(data)).convert('RGB')
    if im.size[0] > max_w:
        h = int(im.size[1] * max_w / im.size[0])
        im = im.resize((max_w, h), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format='JPEG', quality=85, optimize=True, progressive=True)
    with open(out_path, 'wb') as f:
        f.write(buf.getvalue())
    return len(buf.getvalue())

# Wikipedia summary → original image
def wiki_summary_image(title):
    s = fetch_json(f'https://en.wikipedia.org/api/rest_v1/page/summary/{title}')
    if 'originalimage' in s: return s['originalimage']['source']
    if 'thumbnail' in s: return s['thumbnail']['source']
    return None

# Wikipedia media-list fallback (1st suitable image)
def wiki_media_list_image(title):
    blacklist = ['logo','svg','icon','seal','map','diagram','chart']
    ml = fetch_json(f'https://en.wikipedia.org/api/rest_v1/page/media-list/{title}')
    for item in ml.get('items', []):
        if item.get('type') != 'image': continue
        n = item.get('title','').lower()
        if any(b in n for b in blacklist): continue
        srcs = item.get('srcset') or []
        if srcs:
            u = srcs[-1]['src']
            return ('https:' + u) if u.startswith('//') else u
    return None

def download_image(title, outname, desc):
    fp = os.path.join(BASE, outname)
    if os.path.exists(fp) and os.path.getsize(fp) > 60000:
        print(f'  -- {outname}: already exists')
        return True
    try:
        url = None
        try: url = wiki_summary_image(title)
        except: pass
        if not url:
            url = wiki_media_list_image(title)
        if not url:
            print(f'  !! {outname}: no url')
            return False
        data, ct = fetch_bytes(url)
        if not is_img(data):
            print(f'  !! {outname}: non-image')
            return False
        sz = resize_save(data, fp)
        print(f'  OK {outname:<28} {sz:>7,}B  ({desc})')
        return True
    except Exception as e:
        print(f'  !! {outname}: {e}')
        return False

# Disney 目的地
ITEMS = [
    # California Adventure
    ('Disney_California_Adventure',          'dca-entrance.jpg',       'パーク入口'),
    ('Radiator_Springs_Racers',              'radiator-springs.jpg',   'カーズ・レース'),
    ('Guardians_of_the_Galaxy_–_Mission:_Breakout!', 'guardians-breakout.jpg', 'Guardians 絶叫系'),
    ('World_of_Color',                       'world-of-color.jpg',     'ナイトショー'),
    ('Pixar_Pier',                           'pixar-pier.jpg',         'ピクサー・ピア'),
    ('Cars_Land',                            'cars-land.jpg',          'Radiator Springs 街並み'),
    # Disneyland Park
    ('Space_Mountain_(Disneyland)',          'space-mountain.jpg',     'スペースマウンテン'),
    ('Haunted_Mansion',                      'haunted-mansion.jpg',    'ホーンテッドマンション'),
    ('Pirates_of_the_Caribbean_(attraction)','pirates-caribbean.jpg',  'カリブの海賊'),
    ("It's_a_Small_World",                   'small-world.jpg',        '「小さな世界」'),
    ('Matterhorn_Bobsleds',                  'matterhorn.jpg',         'マッターホルン'),
    ('Big_Thunder_Mountain_Railroad',        'big-thunder.jpg',        'ビッグサンダー'),
    ('Star_Wars:_Rise_of_the_Resistance',    'rise-resistance.jpg',    'Star Wars最新'),
    ('Indiana_Jones_Adventure',              'indy-adventure.jpg',     'インディ・ジョーンズ'),
    ("Peter_Pan's_Flight",                   'peter-pan.jpg',          'ピーター・パン'),
    ('Jungle_Cruise',                        'jungle-cruise.jpg',      'ジャングルクルーズ'),
    ("Tiana's_Bayou_Adventure",              'tianas-bayou.jpg',       '旧スプラッシュ'),
    # Food / extras
    ('Dole_Whip',                            'dole-whip.jpg',          'ドールホイップ'),
    ('Mickey_Mouse',                         'mickey-mouse.jpg',       'ミッキーマウス'),
    ('Fireworks',                            'fireworks.jpg',          '花火'),
]

ok = fail = 0
for title, outname, desc in ITEMS:
    if download_image(title, outname, desc):
        ok += 1
    else:
        fail += 1
    time.sleep(1.3)

print(f'\n=== {ok} ok / {fail} fail ===')
