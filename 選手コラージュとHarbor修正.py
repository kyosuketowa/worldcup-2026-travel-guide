"""Hurricane Harbor 修正 + 日本×オランダ代表選手コラージュ生成。"""
import sys, io, urllib.request, os, json, time
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = r'C:/Users/kyosu/worldカップ旅行/images'
HDRS = {
    'User-Agent': 'MorishitaTravelGuide/1.0 (contact: beat.kyosuke.0226@gmail.com)',
    'Accept': 'application/json,image/*',
}

def fetch(url):
    r = urllib.request.urlopen(urllib.request.Request(url, headers=HDRS), timeout=30)
    return r.read(), r.headers.get('Content-Type','')

def fetch_json(url):
    return json.loads(fetch(url)[0].decode('utf-8'))

def is_img(data):
    if len(data) < 12: return False
    if data[:3] == b'\xff\xd8\xff': return True
    if data[:8].startswith(b'\x89PNG'): return True
    if data[:4] == b'RIFF' and data[8:12] == b'WEBP': return True
    return False

# =========================================================
# ① Hurricane Harbor 画像差し替え（Pexelsのウォータースライド）
# =========================================================
print('--- Hurricane Harbor 再取得 ---')
HH_URL = 'https://images.pexels.com/photos/1769356/pexels-photo-1769356.jpeg?auto=compress&cs=tinysrgb&w=1600'
try:
    data, _ = fetch(HH_URL)
    if is_img(data):
        im = Image.open(io.BytesIO(data)).convert('RGB')
        if im.size[0] > 1600:
            im = im.resize((1600, int(im.size[1]*1600/im.size[0])), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, format='JPEG', quality=85, optimize=True)
        with open(os.path.join(BASE, 'water-park.jpg'), 'wb') as f:
            f.write(buf.getvalue())
        print(f'  OK water-park.jpg  {len(buf.getvalue()):,}B (ウォータースライド)')
except Exception as e:
    print(f'  !! water-park: {e}')

# =========================================================
# ② 選手写真ダウンロード（Wikipedia）
# =========================================================
print('\n--- 代表選手写真取得 ---')
PLAYERS = [
    # Japan
    ('Takefusa_Kubo',           'p-kubo.jpg',     'JP', '久保建英'),
    ('Ritsu_Doan',              'p-doan.jpg',     'JP', '堂安律'),
    ('Kaoru_Mitoma',            'p-mitoma.jpg',   'JP', '三苫薫'),
    # Netherlands
    ('Virgil_van_Dijk',         'p-vandijk.jpg',  'NL', 'ファン・ダイク'),
    ('Frenkie_de_Jong',         'p-dejong.jpg',   'NL', 'デ・ヨング'),
    ('Cody_Gakpo',              'p-gakpo.jpg',    'NL', 'ハクポ'),
]

def wiki_image(title):
    """summary API のサムネ/原画URL を返す。"""
    try:
        s = fetch_json(f'https://en.wikipedia.org/api/rest_v1/page/summary/{title}')
        if 'originalimage' in s:
            return s['originalimage']['source']
        if 'thumbnail' in s:
            return s['thumbnail']['source']
    except Exception:
        pass
    return None

player_paths = {}
for title, outname, side, jp_name in PLAYERS:
    try:
        url = wiki_image(title)
        if not url:
            print(f'  !! {outname}: no url'); continue
        data, _ = fetch(url)
        if not is_img(data):
            print(f'  !! {outname}: non-image'); continue
        im = Image.open(io.BytesIO(data)).convert('RGB')
        fp = os.path.join(BASE, outname)
        im.save(fp, format='JPEG', quality=88)
        player_paths[outname] = (fp, side, jp_name)
        print(f'  OK {outname:<16} ({jp_name})')
        time.sleep(1.2)
    except Exception as e:
        print(f'  !! {outname}: {e}')

# =========================================================
# ③ コラージュ画像生成（1600×900）
# =========================================================
print('\n--- コラージュ生成 ---')
CANVAS_W, CANVAS_H = 1600, 900
CELL_W, CELL_H = 400, 500  # 6セル (3×2)
BG_JP = (186, 12, 47)    # 日本赤
BG_NL = (255, 102, 0)    # オランダオレンジ
GAP = 4

def square_crop_from_top(im, size):
    """顔中心になるよう上寄りで正方形クロップ→リサイズ。"""
    w, h = im.size
    side = min(w, h)
    # 人物写真なら上の方に顔がある前提で、上寄りにクロップ
    left = (w - side) // 2
    top = max(0, (h - side) // 3)  # 顔中心狙い
    im2 = im.crop((left, top, left + side, top + side))
    return im2.resize((size, size), Image.LANCZOS)

def portrait_crop(im, tw, th):
    """縦長のセルに合わせてクロップ。"""
    w, h = im.size
    target_ratio = tw / th
    src_ratio = w / h
    if src_ratio > target_ratio:
        # 横長過ぎ → 左右をトリミング
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        im = im.crop((left, 0, left + new_w, h))
    else:
        # 縦長 → 上を残して下をトリミング
        new_h = int(w / target_ratio)
        top = 0  # 顔は通常上
        im = im.crop((0, top, w, top + new_h))
    return im.resize((tw, th), Image.LANCZOS)

# ベース背景（グラデーション）
base = Image.new('RGB', (CANVAS_W, CANVAS_H), (20, 20, 30))
# 左半分を日本赤グラデ、右半分をオランダオレンジグラデ
for y in range(CANVAS_H):
    # 日本側: 上端より下端の方が濃く
    jp = tuple(int(c * (0.7 + 0.3 * y / CANVAS_H)) for c in BG_JP)
    nl = tuple(int(c * (0.7 + 0.3 * y / CANVAS_H)) for c in BG_NL)
    for x in range(CANVAS_W // 2):
        base.putpixel((x, y), jp)
    for x in range(CANVAS_W // 2, CANVAS_W):
        base.putpixel((x, y), nl)

# 選手を配置
# 日本 3名（左）: 3列に並べる（各枠 260×400）
# オランダ 3名（右）: 同様
positions = {
    # (col_idx, side) → (left_x, top_y, w, h)
    ('JP', 0): (40, 180, 236, 340),
    ('JP', 1): (292, 180, 236, 340),
    ('JP', 2): (544, 180, 236, 340),
    ('NL', 0): (816, 180, 236, 340),
    ('NL', 1): (1068, 180, 236, 340),
    ('NL', 2): (1320, 180, 236, 340),
}

jp_idx = nl_idx = 0
for outname, (fp, side, jp_name) in player_paths.items():
    if side == 'JP':
        pos = positions[('JP', jp_idx)]; jp_idx += 1
    else:
        pos = positions[('NL', nl_idx)]; nl_idx += 1
    x, y, w, h = pos
    try:
        with Image.open(fp) as im:
            im = im.convert('RGB')
            im_crop = portrait_crop(im, w, h)
            # 枠白
            frame = Image.new('RGB', (w+8, h+8), 'white')
            frame.paste(im_crop, (4, 4))
            base.paste(frame, (x-4, y-4))
    except Exception as e:
        print(f'  !! {outname}: {e}')

# タイトルとテキスト
draw = ImageDraw.Draw(base)
# フォント探索
def load_font(size):
    # Windowsの日本語対応フォント
    candidates = [
        r'C:\Windows\Fonts\YuGothB.ttc',
        r'C:\Windows\Fonts\meiryob.ttc',
        r'C:\Windows\Fonts\msgothic.ttc',
        r'C:\Windows\Fonts\arial.ttf',
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()

font_title_big = load_font(84)
font_sub = load_font(42)
font_label = load_font(26)
font_name = load_font(22)

# 中央の VS バッジ（円）
vs_cx, vs_cy, vs_r = CANVAS_W // 2, 90, 60
draw.ellipse((vs_cx-vs_r, vs_cy-vs_r, vs_cx+vs_r, vs_cy+vs_r), fill=(20,20,30), outline='white', width=4)
try:
    bbox = draw.textbbox((0,0), 'VS', font=font_title_big)
    tw = bbox[2]-bbox[0]; th = bbox[3]-bbox[1]
    draw.text((vs_cx - tw//2, vs_cy - th//2 - 8), 'VS', font=font_title_big, fill='white')
except Exception:
    draw.text((vs_cx-50, vs_cy-40), 'VS', font=font_title_big, fill='white')

# 日本サイドの見出し
draw.text((40, 30), '🇯🇵 日本代表', font=font_sub, fill='white')
draw.text((40, 90), 'JAPAN', font=font_label, fill=(255, 255, 255, 180))

# オランダサイド
try:
    bbox = draw.textbbox((0,0), '🇳🇱 オランダ代表', font=font_sub)
    w_jp = bbox[2]-bbox[0]
    draw.text((CANVAS_W - 40 - w_jp, 30), '🇳🇱 オランダ代表', font=font_sub, fill='white')
    bbox = draw.textbbox((0,0), 'NETHERLANDS', font=font_label)
    w_nl = bbox[2]-bbox[0]
    draw.text((CANVAS_W - 40 - w_nl, 90), 'NETHERLANDS', font=font_label, fill='white')
except Exception:
    pass

# 選手名ラベル（写真下）
jp_names = ['久保建英', '堂安律', '三苫薫']
nl_names = ['ファン・ダイク', 'デ・ヨング', 'ハクポ']
for i, name in enumerate(jp_names):
    pos = positions[('JP', i)]
    try:
        bbox = draw.textbbox((0,0), name, font=font_name)
        tw = bbox[2]-bbox[0]
        draw.text((pos[0] + pos[2]//2 - tw//2, pos[1] + pos[3] + 14), name, font=font_name, fill='white')
    except Exception:
        pass
for i, name in enumerate(nl_names):
    pos = positions[('NL', i)]
    try:
        bbox = draw.textbbox((0,0), name, font=font_name)
        tw = bbox[2]-bbox[0]
        draw.text((pos[0] + pos[2]//2 - tw//2, pos[1] + pos[3] + 14), name, font=font_name, fill='white')
    except Exception:
        pass

# 試合情報（下）
draw.rectangle((0, CANVAS_H-90, CANVAS_W, CANVAS_H), fill=(10, 10, 20))
match_info = 'FIFA World Cup 2026 · Match 11 · Group F'
date_info = '2026.6.14 (日) 15:00 CDT @ AT&T Stadium, Arlington'
try:
    bbox = draw.textbbox((0,0), match_info, font=font_sub)
    tw = bbox[2]-bbox[0]
    draw.text((CANVAS_W//2 - tw//2, CANVAS_H - 78), match_info, font=font_sub, fill=(255, 217, 127))
    bbox = draw.textbbox((0,0), date_info, font=font_label)
    tw = bbox[2]-bbox[0]
    draw.text((CANVAS_W//2 - tw//2, CANVAS_H - 32), date_info, font=font_label, fill='white')
except Exception:
    pass

# 保存
out_fp = os.path.join(BASE, 'wc-match-collage.jpg')
buf = io.BytesIO()
base.save(buf, format='JPEG', quality=88, optimize=True, progressive=True)
with open(out_fp, 'wb') as f:
    f.write(buf.getvalue())
print(f'  OK wc-match-collage.jpg {len(buf.getvalue()):,}B')
