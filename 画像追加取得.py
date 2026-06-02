"""各目的地の専用画像を Wikipedia API から追加取得。既存 images/ 配下に保存。"""
import sys, io, urllib.request, os, json, time
from PIL import Image

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = r'C:/Users/kyosu/worldカップ旅行/images'
HDRS = {
    'User-Agent': 'MorishitaTravelGuide/1.0 (contact: beat.kyosuke.0226@gmail.com)',
    'Accept': 'application/json,image/*',
}

# (Wikipedia英語記事タイトル, 保存ファイル名, 説明)
ARTICLES = [
    # NYC
    ('Strawberry_Fields_(memorial)',        'strawberry-fields.jpg',  'IMAGINEモザイク'),
    ('Ellis_Island',                         'ellis-island.jpg',       'エリス島移民博物館'),
    ("Basilica_of_St._Patrick's_Old_Cathedral", 'old-st-patricks.jpg', 'Mean Streetsロケ地'),
    ('Little_Italy,_Manhattan',              'little-italy.jpg',       'ゴッドファーザー巡礼'),
    ('30_Rockefeller_Plaza',                 'top-of-rock.jpg',        '展望台'),
    ('Brooklyn_Bridge',                      'brooklyn-bridge2.jpg',   'ブルックリン橋'),
    # LA
    ("TCL_Chinese_Theatre",                  'tcl-chinese.jpg',        'ハリウッド手形・足型'),
    ('The_Grove_(Los_Angeles)',              'the-grove.jpg',          'ショッピング複合施設'),
    ('In-N-Out_Burger',                      'in-n-out.jpg',           'アメリカン・バーガー'),
    ('Hollywood_Walk_of_Fame',               'walk-of-fame.jpg',       '星型プレート'),
    # Dallas / Arlington
    ('Globe_Life_Field',                     'globe-life-field.jpg',   'MLBレンジャーズ球場'),
    # NYC restaurant（Locanda Verdeは記事なし・代替としてThe Greenwich Hotel）
    ('Robert_De_Niro',                       'de-niro.jpg',            'デ・ニーロ'),
]

def fetch_json(url):
    r = urllib.request.urlopen(urllib.request.Request(url, headers=HDRS), timeout=30)
    return json.loads(r.read().decode('utf-8'))

def fetch_bytes(url):
    r = urllib.request.urlopen(urllib.request.Request(url, headers=HDRS), timeout=30)
    return r.read(), r.headers.get('Content-Type','')

def is_img(data):
    if len(data) < 12: return False
    if data[:3] == b'\xff\xd8\xff': return True
    if data[:8].startswith(b'\x89PNG'): return True
    if data[:4] == b'RIFF' and data[8:12] == b'WEBP': return True
    return False

def resize_save(data, out_path, max_w=1600):
    im = Image.open(io.BytesIO(data)).convert('RGB')
    if im.size[0] > max_w:
        h = int(im.size[1] * max_w / im.size[0])
        im = im.resize((max_w, h), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format='JPEG', quality=85, optimize=True, progressive=True)
    with open(out_path, 'wb') as f:
        f.write(buf.getvalue())
    return len(buf.getvalue())

ok = fail = 0
for title, outname, desc in ARTICLES:
    fp = os.path.join(BASE, outname)
    if os.path.exists(fp):
        print(f'  -- {outname}: already exists')
        continue
    try:
        # まず summary API
        img_url = None
        try:
            s = fetch_json(f'https://en.wikipedia.org/api/rest_v1/page/summary/{title}')
            if 'originalimage' in s:
                img_url = s['originalimage']['source']
            elif 'thumbnail' in s:
                img_url = s['thumbnail']['source']
        except Exception as e:
            pass

        # フォールバック: media-list から最初の画像ファイルを取得
        if not img_url:
            ml = fetch_json(f'https://en.wikipedia.org/api/rest_v1/page/media-list/{title}')
            for item in ml.get('items', []):
                if item.get('type') != 'image':
                    continue
                name = item.get('title','').lower()
                if any(b in name for b in ['logo','svg','icon','seal','map','diagram']):
                    continue
                srcs = item.get('srcset') or []
                if srcs:
                    s2 = srcs[-1]['src']
                    img_url = ('https:' + s2) if s2.startswith('//') else s2
                    break

        if not img_url:
            print(f'  !! {outname}: no image url')
            fail += 1
            time.sleep(1.2)
            continue

        data, ct = fetch_bytes(img_url)
        if not is_img(data):
            print(f'  !! {outname}: non-image ct={ct}')
            fail += 1
            time.sleep(1.2)
            continue

        sz = resize_save(data, fp)
        print(f'  OK {outname:<24} {sz:>7,}B  ({desc})')
        ok += 1
        time.sleep(1.2)
    except Exception as e:
        print(f'  !! {outname}: {e}')
        fail += 1
        time.sleep(1.2)

print(f'\n=== {ok} ok / {fail} fail ===')
