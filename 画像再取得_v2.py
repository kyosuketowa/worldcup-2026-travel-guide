"""Wikipedia REST API経由で記事のメイン画像を取得し、正しい画像をimages/に配置する。"""
import urllib.request, os, json, time

BASE = r'C:/Users/kyosu/worldカップ旅行/images'
os.makedirs(BASE, exist_ok=True)

HDRS = {
    'User-Agent': 'MorishitaTravelGuide/1.0 (contact: beat.kyosuke.0226@gmail.com)',
    'Accept': 'application/json,image/*',
}

# Wikipedia記事タイトル -> 保存ファイル名
ARTICLES = [
    ('Statue_of_Liberty',          'statue-of-liberty.jpg'),
    ('Times_Square',               'times-square.jpg'),
    ('The_Dakota',                 'central-park.jpg'),      # ダコタハウスで代用
    ('Bagel',                      'bagel.jpg'),
    ('AT%26T_Stadium',             'stadium.jpg'),           # W杯会場・上書き
    ('Six_Flags_Over_Texas',       'roller-coaster.jpg'),
    ('Dallas',                     'dallas-skyline.jpg'),
    ('Sleeping_Beauty_Castle',     'disneyland-castle.jpg'),
    ('Griffith_Observatory',       'griffith.jpg'),
    ('Hollywood_Sign',             'hollywood-sign.jpg'),
    ('Marina_del_Rey,_California', 'marina-sunset.jpg'),
    ('Range_Rover_(L405)',         'range-rover.jpg'),
    ('Manhattan_Bridge',           'dumbo-manhattan.jpg'),   # DUMBOから見る橋
    ('Empire_State_Building',      'nyc-skyline.jpg'),
    ('Hollywood_Boulevard',        'la-palms.jpg'),
]

def fetch_json(url):
    req = urllib.request.Request(url, headers=HDRS)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode('utf-8'))

def fetch_binary(url):
    req = urllib.request.Request(url, headers=HDRS)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read(), r.headers.get('Content-Type', '')

def is_image(data):
    if len(data) < 12: return False
    if data[:3] == b'\xff\xd8\xff': return True
    if data[:8].startswith(b'\x89PNG'): return True
    if data[:4] == b'RIFF' and data[8:12] == b'WEBP': return True
    return False

ok = fail = 0
for title, outname in ARTICLES:
    fp = os.path.join(BASE, outname)
    try:
        summary = fetch_json(f'https://en.wikipedia.org/api/rest_v1/page/summary/{title}')
        img_url = None
        if 'originalimage' in summary:
            img_url = summary['originalimage']['source']
        elif 'thumbnail' in summary:
            img_url = summary['thumbnail']['source']
        if not img_url:
            print(f'  !! {title}: no image in summary')
            fail += 1
            time.sleep(1.5)
            continue
        # Avoid very narrow thumbnails: request larger by replacing size segment
        if '/thumb/' in img_url and img_url.endswith('.jpg'):
            # keep as-is; summary thumbnail URLs are usually 1024+
            pass
        data, ct = fetch_binary(img_url)
        if not is_image(data):
            print(f'  !! {outname}: non-image ct={ct}')
            fail += 1
            time.sleep(1.5)
            continue
        with open(fp, 'wb') as f:
            f.write(data)
        print(f'  OK {outname:<24} <- {title:<30} {len(data):>10,}B')
        ok += 1
        time.sleep(1.5)  # rate limit friendly
    except Exception as e:
        print(f'  !! {outname} ({title}): {e}')
        fail += 1
        time.sleep(1.5)

print(f'\n=== Done: {ok} ok / {fail} failed ===')
