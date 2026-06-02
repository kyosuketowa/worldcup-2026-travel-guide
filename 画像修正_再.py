"""In-N-Out バーガー + Walk of Fame star の再取得。"""
import sys, io, urllib.request, os
from PIL import Image
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = r'C:/Users/kyosu/worldカップ旅行/images'
HDRS = {'User-Agent': 'Mozilla/5.0 (Windows; rv:120) Gecko/20100101 Firefox/120.0', 'Accept':'image/*'}

URLS = {
    # バーガー写真（Pexels）
    'in-n-out.jpg':     'https://images.pexels.com/photos/1639557/pexels-photo-1639557.jpeg?auto=compress&cs=tinysrgb&w=1600',
    # Walk of Fame star（Pexels）
    'walk-of-fame.jpg': 'https://images.pexels.com/photos/208984/pexels-photo-208984.jpeg?auto=compress&cs=tinysrgb&w=1600',
}

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

for name, url in URLS.items():
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers=HDRS), timeout=30)
        data = r.read()
        sz = resize_save(data, os.path.join(BASE, name))
        print(f'  OK {name:<24} {sz:>7,}B')
    except Exception as e:
        print(f'  !! {name}: {e}')
