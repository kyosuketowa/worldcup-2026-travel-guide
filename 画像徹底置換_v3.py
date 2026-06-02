"""Commons 直接置換 v3 - verbose error"""
import sys, io, urllib.request, urllib.parse, os, json, time, traceback
from PIL import Image
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)

BASE = r'C:/Users/kyosu/worldカップ旅行/images'
HDRS = {'User-Agent':'MorishitaTravelGuide/1.0','Accept':'application/json,image/*,*/*;q=0.8'}

def fetch(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers=HDRS), timeout=40).read()

def is_img(d):
    if len(d) < 12: return False
    return d[:3]==b'\xff\xd8\xff' or d[:8].startswith(b'\x89PNG')

def save_jpeg(data, path, max_w=1400):
    im = Image.open(io.BytesIO(data)).convert('RGB')
    if im.size[0] > max_w:
        im = im.resize((max_w, int(im.size[1]*max_w/im.size[0])), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format='JPEG', quality=85, optimize=True, progressive=True)
    with open(path,'wb') as f: f.write(buf.getvalue())
    return len(buf.getvalue())

def search(query, limit=30):
    q = urllib.parse.quote(query)
    url = f'https://commons.wikimedia.org/w/api.php?action=query&format=json&list=search&srsearch={q}&srnamespace=6&srlimit={limit}'
    d = fetch(url).decode('utf-8')
    return [it.get('title','') for it in json.loads(d).get('query',{}).get('search',[])]

def thumb(file_title, width=1400):
    q = urllib.parse.quote(file_title)
    url = f'https://commons.wikimedia.org/w/api.php?action=query&format=json&titles={q}&prop=imageinfo&iiprop=url|size&iiurlwidth={width}'
    d = fetch(url).decode('utf-8')
    for _, p in json.loads(d).get('query',{}).get('pages',{}).items():
        ii = p.get('imageinfo', [])
        if ii:
            return ii[0].get('thumburl') or ii[0].get('url')
    return None

AVOID = ['logo','poster','svg','diagram','plan','postcard','ticket','emblem','coat_of_arms']

JOBS = [
    ('haunted-mansion.jpg',   ['Haunted Mansion Disneyland exterior','Haunted Mansion Disneyland']),
    ('pirates-caribbean.jpg', ['Pirates Caribbean Disneyland attraction','New Orleans Square Disneyland']),
    ('cars-land.jpg',         ['Cars Land Disneyland night','Radiator Springs Racers']),
    ('pixar-pier.jpg',        ['Paradise Pier Disneyland','Pixar Pier Disneyland']),
    ('small-world.jpg',       ["small world Disneyland facade",'small world Disneyland exterior']),
    ('indy-adventure.jpg',    ['Indiana Jones Adventure Disneyland entrance','Indiana Jones Adventure queue']),
    ('rise-resistance.jpg',   ["Galaxy's Edge Disneyland Millennium Falcon","Galaxy's Edge Disneyland Batuu"]),
    ('tianas-bayou.jpg',      ['Splash Mountain Disneyland','Tiana Bayou Adventure attraction']),
    ('mickey-mouse.jpg',      ['Mickey Mouse parade Disneyland','Mickey Mouse character Disneyland']),
    ('fireworks.jpg',         ['Sleeping Beauty Castle fireworks','Disneyland fireworks night']),
]

ok = fail = 0
for outname, queries in JOBS:
    print(f'[[{outname}]]', flush=True)
    found = None
    for q in queries:
        print(f'   query: "{q}"', flush=True)
        try:
            names = search(q)
            print(f'     -> {len(names)} hits', flush=True)
        except Exception as e:
            print(f'     search err: {e}', flush=True)
            time.sleep(1.0)
            continue

        for fn in names[:15]:
            low = fn.lower()
            if any(a in low for a in AVOID):
                continue
            if low.endswith('.svg'):
                continue
            try:
                u = thumb(fn)
                if not u: continue
                d = fetch(u)
                if not is_img(d): continue
                im = Image.open(io.BytesIO(d))
                if im.size[0] < 600 or len(d) < 80*1024:
                    continue
                found = (u, d, fn)
                print(f'     ✅ use: {fn}', flush=True)
                break
            except Exception as e:
                print(f'     skip {fn[:50]}: {type(e).__name__}', flush=True)
                continue
        if found: break
        time.sleep(0.8)

    if not found:
        print(f'   ❌ 失敗', flush=True)
        fail += 1
        continue
    u, d, fn = found
    sz = save_jpeg(d, os.path.join(BASE, outname))
    print(f'   💾 {sz:,}B', flush=True)
    ok += 1
    time.sleep(0.8)

print(f'\n=== {ok}/{len(JOBS)} ===', flush=True)
