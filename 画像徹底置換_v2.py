"""全ロゴ画像を Commons 実写真で置換（v2・詳細ログ付き）"""
import sys, io, urllib.request, urllib.parse, os, json, time
from PIL import Image
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = r'C:/Users/kyosu/worldカップ旅行/images'
HDRS = {
    'User-Agent': 'MorishitaTravelGuide/1.0 (contact:beat@example.com) PythonClient',
    'Accept': 'application/json,image/*,*/*;q=0.8',
}

def fetch(u):
    r = urllib.request.urlopen(urllib.request.Request(u, headers=HDRS), timeout=40)
    return r.read()

def is_img(d):
    if len(d) < 12: return False
    return d[:3]==b'\xff\xd8\xff' or d[:8].startswith(b'\x89PNG') or (d[:4]==b'RIFF' and d[8:12]==b'WEBP')

def save_jpeg(data, path, max_w=1400):
    im = Image.open(io.BytesIO(data)).convert('RGB')
    if im.size[0] > max_w:
        im = im.resize((max_w, int(im.size[1]*max_w/im.size[0])), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format='JPEG', quality=85, optimize=True, progressive=True)
    with open(path,'wb') as f: f.write(buf.getvalue())
    return len(buf.getvalue())

def commons_search_filenames(query, limit=30):
    """Commons検索で File:... のタイトル一覧を返す。"""
    q = urllib.parse.quote(query)
    url = f'https://commons.wikimedia.org/w/api.php?action=query&format=json&list=search&srsearch={q}&srnamespace=6&srlimit={limit}'
    data = json.loads(fetch(url).decode('utf-8'))
    return [it.get('title','') for it in data.get('query',{}).get('search',[])]

def commons_thumburl(file_title, width=1400):
    """File:XXX.jpg → サムネURLを取得。"""
    q = urllib.parse.quote(file_title)  # "File:..." そのまま
    url = f'https://commons.wikimedia.org/w/api.php?action=query&format=json&titles={q}&prop=imageinfo&iiprop=url|size&iiurlwidth={width}'
    data = json.loads(fetch(url).decode('utf-8'))
    for _, page in data.get('query', {}).get('pages', {}).items():
        ii = page.get('imageinfo', [])
        if ii:
            return ii[0].get('thumburl') or ii[0].get('url')
    return None

def try_search(queries, min_w=600, min_bytes=60*1024, avoid_terms=None):
    """複数検索クエリを順に試し、実写らしき画像の (url, data) を返す。"""
    avoid = avoid_terms or ['logo','poster','svg','map','diagram','plan','sign','postcard','ticket','emblem']
    for q in queries:
        try:
            filenames = commons_search_filenames(q)
        except Exception as e:
            print(f'    search err: {e}')
            continue
        for fn in filenames:
            low = fn.lower()
            if any(a in low for a in avoid): continue
            if low.endswith('.svg') or low.endswith('.png') and 'logo' in low: continue
            try:
                url = commons_thumburl(fn)
                if not url: continue
                d = fetch(url)
                if not is_img(d): continue
                im = Image.open(io.BytesIO(d))
                if im.size[0] < min_w: continue
                if len(d) < min_bytes: continue
                return (url, d, fn)
            except Exception as e:
                continue
    return None

# 各画像 → 検索クエリ候補（Commons で検索）
JOBS = [
    ('pixar-pier.jpg',        ['Pixar Pier Disneyland ferris wheel','Paradise Pier Disneyland','Disney California Adventure pier']),
    ('indy-adventure.jpg',    ['Indiana Jones Adventure Disneyland entrance','Indiana Jones Adventure queue','Disneyland Adventureland entrance']),
    ('rise-resistance.jpg',   ["Star Wars Galaxy's Edge Disneyland","Batuu Disneyland","Millennium Falcon Galaxy's Edge"]),
    ('tianas-bayou.jpg',      ['Splash Mountain Disneyland','Tiana Bayou Adventure','Disneyland Critter Country']),
    ('cars-land.jpg',         ['Cars Land Disney California Adventure','Cars Land Radiator Springs','Cars Land night']),
    ('small-world.jpg',       ["it's a small world Disneyland exterior","Small World Disneyland facade","Fantasyland Disneyland small world"]),
    ('mickey-mouse.jpg',      ['Mickey Mouse character parade','Disneyland Mickey character meet','Mickey Minnie Disneyland']),
    ('fireworks.jpg',         ['Disneyland fireworks castle','Disneyland Forever fireworks','Sleeping Beauty Castle fireworks']),
    ('haunted-mansion.jpg',   ['Haunted Mansion Disneyland exterior','Haunted Mansion Disneyland','Haunted Mansion Holiday Exterior']),
    ('pirates-caribbean.jpg', ['New Orleans Square Disneyland','Pirates Caribbean Disneyland ride','Blue Bayou Disneyland']),
]

ok = fail = 0
for outname, queries in JOBS:
    print(f'\n🔄 {outname:<22}')
    result = try_search(queries)
    if not result:
        print(f'  !! 失敗')
        fail += 1
        time.sleep(1)
        continue
    url, data, fname = result
    fp = os.path.join(BASE, outname)
    sz = save_jpeg(data, fp)
    print(f'  OK {sz:>7,}B  <- {fname[:60]}')
    ok += 1
    time.sleep(1)

print(f'\n=== 成功 {ok}/{len(JOBS)} ===')
