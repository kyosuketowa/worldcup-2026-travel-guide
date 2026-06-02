"""Wikimedia Commons/公式CC画像を使って、内容と名前がズレたJPGを上書き取得する。"""
import urllib.request, os

BASE = r'C:/Users/kyosu/worldカップ旅行/images'
os.makedirs(BASE, exist_ok=True)

HDRS = {
    'User-Agent': 'Mozilla/5.0 (compatible; MorishitaTravelGuide/1.0; +https://example.com/)',
    'Accept': 'image/*,*/*;q=0.8',
}

# すべて Wikimedia Commons の直リンク（著作権CC BY/SA もしくは PD）
FIX = {
    # NG判定済み13枚
    'nyc-skyline.jpg':       'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/View_of_Empire_State_Building_from_Rockefeller_Center_New_York_City_dllu.jpg/1280px-View_of_Empire_State_Building_from_Rockefeller_Center_New_York_City_dllu.jpg',
    'statue-of-liberty.jpg': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Statue_of_Liberty%2C_NY.jpg/1024px-Statue_of_Liberty%2C_NY.jpg',
    'times-square.jpg':      'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Times_Square_1-2.JPG/1280px-Times_Square_1-2.JPG',
    'central-park.jpg':      'https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/The_Dakota.jpg/1280px-The_Dakota.jpg',  # ダコタハウス実物
    'bagel.jpg':             'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Bagels-Montr%C3%A9al-Canada.jpg/1280px-Bagels-Montr%C3%A9al-Canada.jpg',
    'roller-coaster.jpg':    'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/El_Toro_%28Six_Flags_Great_Adventure%29_02.jpg/1280px-El_Toro_%28Six_Flags_Great_Adventure%29_02.jpg',
    'dallas-skyline.jpg':    'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Dallas_skyline_daytime.jpg/1280px-Dallas_skyline_daytime.jpg',
    'disneyland-castle.jpg': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Disneyland_Sleeping_Beauty_Castle_DSC_6837.jpg/1280px-Disneyland_Sleeping_Beauty_Castle_DSC_6837.jpg',
    'griffith.jpg':          'https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Griffith_Observatory_at_night_2006.jpg/1280px-Griffith_Observatory_at_night_2006.jpg',
    'hollywood-sign.jpg':    'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Hollywood_Sign_%28Zuschnitt%29.jpg/1280px-Hollywood_Sign_%28Zuschnitt%29.jpg',
    'la-palms.jpg':          'https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Palm_trees_along_Hollywood_Boulevard_-_panoramio.jpg/1280px-Palm_trees_along_Hollywood_Boulevard_-_panoramio.jpg',
    'marina-sunset.jpg':     'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Marina_del_Rey_Marina_North_Jetty.jpg/1280px-Marina_del_Rey_Marina_North_Jetty.jpg',
    'range-rover.jpg':       'https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/2018_Range_Rover_Vogue_SE_SDV8_Automatic_4.4_Front.jpg/1280px-2018_Range_Rover_Vogue_SE_SDV8_Automatic_4.4_Front.jpg',
    # 追加で欲しい画像
    'stadium-at-t.jpg':      'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/AT%26T_Stadium_Arlington_%28cropped%29.jpg/1280px-AT%26T_Stadium_Arlington_%28cropped%29.jpg',
    'dumbo-real.jpg':        'https://upload.wikimedia.org/wikipedia/commons/thumb/7/79/Manhattan_Bridge_View_from_DUMBO.jpg/1280px-Manhattan_Bridge_View_from_DUMBO.jpg',
    'mott-street.jpg':       'https://upload.wikimedia.org/wikipedia/commons/thumb/1/19/Mott_Street_from_Canal.jpg/1280px-Mott_Street_from_Canal.jpg',
}

def is_image(data: bytes) -> bool:
    if len(data) < 12: return False
    if data[:3] == b'\xff\xd8\xff': return True        # JPEG
    if data[:8].startswith(b'\x89PNG'): return True    # PNG
    if data[:4] == b'RIFF' and data[8:12] == b'WEBP': return True
    return False

ok = fail = 0
for name, url in FIX.items():
    fp = os.path.join(BASE, name)
    try:
        req = urllib.request.Request(url, headers=HDRS)
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
            ct = r.headers.get('Content-Type', '')
        if not is_image(data):
            print(f'  !! {name}: non-image ct={ct} len={len(data)}')
            fail += 1
            continue
        with open(fp, 'wb') as f:
            f.write(data)
        print(f'  OK {name}: {len(data):,}B ({ct})')
        ok += 1
    except Exception as e:
        print(f'  !! {name}: {e}')
        fail += 1

print(f'\n=== Done: {ok} ok / {fail} failed ===')
