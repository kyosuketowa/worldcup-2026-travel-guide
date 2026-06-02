"""Hurricane Harbor 画像を別ソースで差し替え。"""
import sys, io, urllib.request, os, json, time
from PIL import Image
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = r'C:/Users/kyosu/worldカップ旅行/images'
HDRS = {'User-Agent':'Mozilla/5.0 MorishitaTravelGuide','Accept':'image/*,application/json'}

def fetch(url):
    r = urllib.request.urlopen(urllib.request.Request(url, headers=HDRS), timeout=30)
    return r.read(), r.headers.get('Content-Type','')

def fetch_json(url):
    return json.loads(fetch(url)[0].decode('utf-8'))

def is_img(data):
    return data[:3] == b'\xff\xd8\xff' or data[:8].startswith(b'\x89PNG')

def save_resized(data, path, max_w=1600):
    im = Image.open(io.BytesIO(data)).convert('RGB')
    if im.size[0] > max_w:
        im = im.resize((max_w, int(im.size[1]*max_w/im.size[0])), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format='JPEG', quality=85, optimize=True)
    with open(path, 'wb') as f:
        f.write(buf.getvalue())
    return len(buf.getvalue())

# 試す候補（複数フォールバック）
CANDIDATES = [
    # 1. Wikipedia の Six Flags Hurricane Harbor Arlington から media-list
    ('wiki-ml', 'Six_Flags_Hurricane_Harbor,_Arlington'),
    # 2. 水系の Pexels ID
    ('pexels',  'https://images.pexels.com/photos/261404/pexels-photo-261404.jpeg?auto=compress&cs=tinysrgb&w=1600'),
    # 3. 別の Pexels
    ('pexels',  'https://images.pexels.com/photos/3046652/pexels-photo-3046652.jpeg?auto=compress&cs=tinysrgb&w=1600'),
    # 4. Water slide Pexels
    ('pexels',  'https://images.pexels.com/photos/1687845/pexels-photo-1687845.jpeg?auto=compress&cs=tinysrgb&w=1600'),
]

def try_wiki_media_list(title):
    blacklist = ['logo','svg','icon','seal','map','diagram']
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

target = os.path.join(BASE, 'water-park.jpg')
for kind, arg in CANDIDATES:
    try:
        if kind == 'wiki-ml':
            url = try_wiki_media_list(arg)
            if not url:
                print(f'  !! wiki-ml {arg}: no usable image')
                continue
        else:
            url = arg
        data, ct = fetch(url)
        if not is_img(data):
            print(f'  !! {url[:60]}: non-image')
            continue
        sz = save_resized(data, target)
        print(f'  OK ({kind}) {sz:,}B  <- {url[-60:]}')
        break
    except Exception as e:
        print(f'  !! {kind} {arg[:40]}: {e}')
        time.sleep(1.2)
