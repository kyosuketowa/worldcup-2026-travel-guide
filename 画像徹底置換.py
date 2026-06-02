"""全ロゴ/偽物画像を Wikipedia Commons の実写真で差し替える。
   複数の記事タイトルを試行し、ロゴを避けて大きい画像を優先。"""
import sys, io, urllib.request, os, json, time
from PIL import Image
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = r'C:/Users/kyosu/worldカップ旅行/images'
HDRS = {'User-Agent':'MorishitaTravelGuide/1.0 (contact:beat@example.com)','Accept':'application/json,image/*'}

def fetch_bytes(u):
    r = urllib.request.urlopen(urllib.request.Request(u, headers=HDRS), timeout=40)
    return r.read()

def is_img(d):
    if len(d) < 12: return False
    return d[:3]==b'\xff\xd8\xff' or d[:8].startswith(b'\x89PNG') or (d[:4]==b'RIFF' and d[8:12]==b'WEBP')

def save(data, path, max_w=1400):
    im = Image.open(io.BytesIO(data)).convert('RGB')
    if im.size[0] > max_w:
        im = im.resize((max_w, int(im.size[1]*max_w/im.size[0])), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format='JPEG', quality=85, optimize=True, progressive=True)
    with open(path,'wb') as f: f.write(buf.getvalue())
    return len(buf.getvalue())

def search_commons(query, limit=20):
    """Wikimedia Commons API で画像を検索。"""
    q = urllib.parse.quote(query)
    url = f'https://commons.wikimedia.org/w/api.php?action=query&format=json&list=search&srsearch={q}&srnamespace=6&srlimit={limit}'
    return json.loads(fetch_bytes(url).decode('utf-8'))

def commons_file_url(filename):
    """File:XXX → 実URLを取得。"""
    q = urllib.parse.quote(filename)
    url = f'https://commons.wikimedia.org/w/api.php?action=query&format=json&titles=File:{q}&prop=imageinfo&iiprop=url&iiurlwidth=1400'
    data = json.loads(fetch_bytes(url).decode('utf-8'))
    for _, page in data.get('query', {}).get('pages', {}).items():
        ii = page.get('imageinfo', [])
        if ii:
            return ii[0].get('thumburl') or ii[0].get('url')
    return None

def wiki_media_list(title, blacklist=None, min_size_kb=80):
    """Wikipedia記事の media-list から、ロゴ等を除外して実写真を返す。"""
    blacklist = blacklist or ['logo','svg','icon','seal','map','diagram','chart','poster','coat_of_arms']
    try:
        ml = json.loads(fetch_bytes(f'https://en.wikipedia.org/api/rest_v1/page/media-list/{title}').decode('utf-8'))
    except Exception:
        return None
    for item in ml.get('items', []):
        if item.get('type') != 'image': continue
        n = item.get('title','').lower()
        if any(b in n for b in blacklist): continue
        srcs = item.get('srcset') or []
        if not srcs: continue
        u = srcs[-1]['src']
        if u.startswith('//'): u = 'https:' + u
        try:
            d = fetch_bytes(u)
            if not is_img(d): continue
            if len(d) < min_size_kb * 1024: continue  # 小さい=ロゴを避ける
            return (u, d)
        except Exception:
            continue
    return None

import urllib.parse

# 各対象について複数ソース試行。成功した時点で保存して次へ。
TARGETS = [
    {
        'out': 'pixar-pier.jpg',
        'title': 'Pixar Pier（海沿いエリア）',
        'attempts': [
            ('wiki', 'Pixar_Pier'),
            ('wiki', 'Paradise_Pier'),
            ('wiki', 'Disney_California_Adventure'),
            ('commons-file', 'Disney California Adventure Park Mickeys Fun Wheel.jpg'),
            ('commons-search', 'Pixar Pier Disneyland ferris wheel'),
        ],
    },
    {
        'out': 'indy-adventure.jpg',
        'title': 'Indiana Jones Adventure 外観',
        'attempts': [
            ('wiki', 'Indiana_Jones_Adventure'),
            ('wiki', 'Adventureland_at_Disneyland'),
            ('commons-file', 'Disneyland Indiana Jones Adventure.jpg'),
            ('commons-search', 'Indiana Jones Adventure Disneyland exterior'),
        ],
    },
    {
        'out': 'rise-resistance.jpg',
        'title': 'Star Wars Galaxy\'s Edge',
        'attempts': [
            ('wiki', "Star_Wars:_Galaxy's_Edge"),
            ('wiki', 'Star_Wars:_Rise_of_the_Resistance'),
            ('commons-search', 'Star Wars Galaxy Edge Disneyland'),
        ],
    },
    {
        'out': 'tianas-bayou.jpg',
        'title': 'Tiana\'s Bayou Adventure / Splash Mountain',
        'attempts': [
            ('wiki', 'Splash_Mountain_(Disneyland)'),
            ('wiki', "Tiana's_Bayou_Adventure"),
            ('wiki', 'Splash_Mountain'),
            ('commons-search', 'Splash Mountain Disneyland'),
        ],
    },
    {
        'out': 'cars-land.jpg',
        'title': 'Cars Land',
        'attempts': [
            ('wiki', 'Cars_Land'),
            ('wiki', 'Radiator_Springs_Racers'),
            ('commons-file', 'Radiator Springs Racers rock formations.jpg'),
            ('commons-search', 'Cars Land Disney California'),
        ],
    },
    {
        'out': 'small-world.jpg',
        'title': "it's a small world",
        'attempts': [
            ('wiki', "It's_a_Small_World"),
            ('wiki', 'Fantasyland_(Disneyland)'),
            ('commons-search', 'its a small world Disneyland facade'),
        ],
    },
    {
        'out': 'mickey-mouse.jpg',
        'title': 'Mickey Mouse（実写キャラ）',
        'attempts': [
            ('commons-search', 'Mickey Mouse character Disneyland'),
            ('commons-search', 'Disneyland Mickey Mouse parade'),
        ],
    },
    {
        'out': 'fireworks.jpg',
        'title': 'Disneyland Castle Fireworks',
        'attempts': [
            ('commons-search', 'Disneyland fireworks castle'),
            ('commons-search', 'Sleeping Beauty Castle fireworks night'),
            ('wiki', 'Disneyland_Forever'),
            ('wiki', 'Disneyland'),
        ],
    },
    {
        'out': 'haunted-mansion.jpg',
        'title': 'Haunted Mansion',
        'attempts': [
            ('wiki', 'The_Haunted_Mansion'),
            ('wiki', 'Haunted_Mansion'),
            ('wiki', 'New_Orleans_Square'),
            ('commons-search', 'Haunted Mansion Disneyland exterior'),
        ],
    },
    {
        'out': 'pirates-caribbean.jpg',
        'title': 'Pirates of the Caribbean 外観（看板以外）',
        'attempts': [
            ('wiki', 'New_Orleans_Square'),
            ('commons-search', 'Pirates Caribbean Disneyland exterior facade'),
        ],
    },
]

def try_attempts(attempts, label):
    """各 attempt を順に試し、成功したら (url, data) を返す。"""
    for kind, arg in attempts:
        try:
            if kind == 'wiki':
                result = wiki_media_list(arg)
                if result:
                    return result
            elif kind == 'commons-file':
                url = commons_file_url(arg)
                if url:
                    d = fetch_bytes(url)
                    if is_img(d) and len(d) > 80*1024:
                        return (url, d)
            elif kind == 'commons-search':
                sres = search_commons(arg)
                for item in sres.get('query', {}).get('search', []):
                    fname = item.get('title','').replace('File:', '')
                    if any(b in fname.lower() for b in ['logo','svg','poster','map','diagram','plan','coat']):
                        continue
                    url = commons_file_url(fname)
                    if not url: continue
                    try:
                        d = fetch_bytes(url)
                        if is_img(d) and len(d) > 80*1024:
                            im = Image.open(io.BytesIO(d))
                            if im.size[0] < 500 or im.size[1] < 400: continue
                            return (url, d)
                    except Exception:
                        continue
        except Exception as e:
            pass
        time.sleep(1.2)
    return None

ok = fail = 0
for t in TARGETS:
    print(f'\n🔄 {t["out"]:<22} ({t["title"]})')
    result = try_attempts(t['attempts'], t['title'])
    if not result:
        print(f'  !! 失敗: {t["out"]}')
        fail += 1
        continue
    url, data = result
    fp = os.path.join(BASE, t['out'])
    sz = save(data, fp)
    print(f'  OK {sz:,}B  <- {url[-70:]}')
    ok += 1
    time.sleep(1.0)

print(f'\n=== 成功 {ok} / 失敗 {fail} ===')
