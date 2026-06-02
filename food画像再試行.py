"""残り7枚を別クエリで再取得"""
import sys, io, urllib.request, urllib.parse, os, json, time
from PIL import Image
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)

BASE = r'C:/Users/kyosu/worldカップ旅行/images'
HDRS = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36','Accept':'image/*','Referer':'https://commons.wikimedia.org/'}

def fetch(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers=HDRS), timeout=40).read()
def is_img(d):
    if len(d) < 12: return False
    return d[:3]==b'\xff\xd8\xff' or d[:8].startswith(b'\x89PNG')
def save_jpeg(data, path, max_w=1200):
    im = Image.open(io.BytesIO(data)).convert('RGB')
    if im.size[0] > max_w:
        im = im.resize((max_w, int(im.size[1]*max_w/im.size[0])), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format='JPEG', quality=85, optimize=True, progressive=True)
    with open(path,'wb') as f: f.write(buf.getvalue())
    return len(buf.getvalue())
def search(q, limit=20):
    qe = urllib.parse.quote(q)
    url = f'https://commons.wikimedia.org/w/api.php?action=query&format=json&list=search&srsearch={qe}&srnamespace=6&srlimit={limit}'
    return [it.get('title','') for it in json.loads(fetch(url).decode('utf-8')).get('query',{}).get('search',[])]
def thumb(fn):
    q = urllib.parse.quote(fn)
    url = f'https://commons.wikimedia.org/w/api.php?action=query&format=json&titles={q}&prop=imageinfo&iiprop=url|mime&iiurlwidth=1200'
    d = fetch(url).decode('utf-8')
    for _, p in json.loads(d).get('query',{}).get('pages',{}).items():
        ii = p.get('imageinfo', [])
        if ii and ii[0].get('mime','').startswith('image/'):
            return ii[0].get('thumburl') or ii[0].get('url')
    return None
def is_image_file(name):
    return name.lower().endswith(('.jpg','.jpeg','.png'))
AVOID = ['logo','poster','svg','diagram','chart','plan','sign','map']

JOBS = [
    ('food-jalapeno-popper.jpg', ['Jalapeño poppers appetizer','Stuffed jalapeno peppers','Pimiento cheese jalapeno']),
    ('food-tres-leches.jpg',     ['Pastel de tres leches','Cake dessert Latin','Three milk cake']),
    ('food-fried-chicken.jpg',   ['Fried chicken dinner','Chicken and waffles','American fried chicken']),
    ('food-monte-cristo.jpg',    ['Monte Cristo sandwich food','Ham cheese fried sandwich','Fried sandwich']),
    ('food-pretzel.jpg',         ['Pretzel bread snack','Pretzel soft','Salted pretzel']),
    ('food-burrito.jpg',         ['Burrito Mexican','Chicken burrito','Burrito food']),
    ('food-pastry.jpg',          ['Croissant bakery','French pastry','Danish bakery breakfast']),
]

ok = fail = 0
for outname, queries in JOBS:
    fp = os.path.join(BASE, outname)
    if os.path.exists(fp) and os.path.getsize(fp) > 50000:
        print(f'  -- {outname}: exists')
        ok += 1
        continue
    print(f'\n[[{outname}]]', flush=True)
    found = None
    for q in queries:
        time.sleep(1.2)
        try:
            names = search(q)
        except: continue
        img_names = [n for n in names if is_image_file(n) and not any(a in n.lower() for a in AVOID)]
        for fn in img_names[:10]:
            time.sleep(0.5)
            try:
                u = thumb(fn)
                if not u: continue
                d = fetch(u)
                if not is_img(d): continue
                im = Image.open(io.BytesIO(d))
                if max(im.size) < 600 or len(d) < 40*1024: continue
                found = (u, d, fn)
                print(f'    ✅ {fn[:60]}', flush=True)
                break
            except Exception:
                continue
        if found: break
    if not found:
        print(f'  ❌', flush=True)
        fail += 1
        continue
    u, d, fn = found
    sz = save_jpeg(d, fp)
    print(f'  💾 {sz:,}B', flush=True)
    ok += 1
    time.sleep(0.8)

print(f'\n=== {ok}/{len(JOBS)} ===', flush=True)
