"""残り4枚の差し替え + 全画像を 1600px幅 / JPEG Q85 に縮小。"""
import urllib.request, os, time
from PIL import Image
import io

BASE = r'C:/Users/kyosu/worldカップ旅行/images'

HDRS = {
    'User-Agent': 'Mozilla/5.0 (Windows; rv:120) Gecko/20100101 Firefox/120.0',
    'Accept': 'image/*,*/*;q=0.8',
}

# Pexels（公開配布・商用OK）の安定URL。以前の download_images.py でも同ソース利用。
REPLACEMENTS = {
    'nyc-skyline.jpg':    'https://images.pexels.com/photos/290386/pexels-photo-290386.jpeg?auto=compress&cs=tinysrgb&w=1600',
    'griffith.jpg':       'https://images.pexels.com/photos/2404370/pexels-photo-2404370.jpeg?auto=compress&cs=tinysrgb&w=1600',
    'roller-coaster.jpg': 'https://images.pexels.com/photos/207305/pexels-photo-207305.jpeg?auto=compress&cs=tinysrgb&w=1600',
    'la-palms.jpg':       'https://images.pexels.com/photos/1619317/pexels-photo-1619317.jpeg?auto=compress&cs=tinysrgb&w=1600',
}

def is_image(data):
    if len(data) < 12: return False
    if data[:3] == b'\xff\xd8\xff': return True
    if data[:8].startswith(b'\x89PNG'): return True
    if data[:4] == b'RIFF' and data[8:12] == b'WEBP': return True
    return False

print('--- Step 1: 差し替え取得 ---')
for name, url in REPLACEMENTS.items():
    fp = os.path.join(BASE, name)
    try:
        req = urllib.request.Request(url, headers=HDRS)
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
            ct = r.headers.get('Content-Type', '')
        if not is_image(data):
            print(f'  !! {name}: non-image ct={ct}')
            continue
        with open(fp, 'wb') as f:
            f.write(data)
        print(f'  OK {name}: {len(data):,}B ({ct})')
        time.sleep(0.5)
    except Exception as e:
        print(f'  !! {name}: {e}')

print('\n--- Step 2: 1600px 幅 / Q85 にリサイズ ---')
MAX_W = 1600
files = sorted(f for f in os.listdir(BASE) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')))
for fn in files:
    fp = os.path.join(BASE, fn)
    before = os.path.getsize(fp)
    try:
        with Image.open(fp) as im:
            im = im.convert('RGB')
            w, h = im.size
            if w > MAX_W:
                new_h = int(h * MAX_W / w)
                im = im.resize((MAX_W, new_h), Image.LANCZOS)
            buf = io.BytesIO()
            im.save(buf, format='JPEG', quality=85, optimize=True, progressive=True)
            data = buf.getvalue()
        # 既存より小さくなった場合のみ上書き（無劣化最適化を意識）
        if len(data) < before:
            new_name = fn.rsplit('.', 1)[0] + '.jpg'
            new_fp = os.path.join(BASE, new_name)
            with open(new_fp, 'wb') as f:
                f.write(data)
            if new_fp != fp and os.path.exists(fp):
                os.remove(fp)
            after = len(data)
            print(f'  OK {fn:<24} {before:>10,}B -> {after:>10,}B  ({100*after/before:.1f}%)')
        else:
            print(f'  -- {fn:<24} {before:>10,}B  (skip, size OK)')
    except Exception as e:
        print(f'  !! {fn}: {e}')

print('\n=== Done ===')
