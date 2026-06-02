"""Retry failed images + accept WebP."""
import urllib.request, os

BASE = r'C:/Users/kyosu/worldカップ旅行/images'
os.makedirs(BASE, exist_ok=True)

HDRS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'image/*',
    'Accept-Language': 'en-US,en;q=0.9',
}

RETRY = {
    'dumbo-manhattan.jpg':   'https://images.pexels.com/photos/1486222/pexels-photo-1486222.jpeg?auto=compress&cs=tinysrgb&w=1200',
    'italian-food.jpg':      'https://images.pexels.com/photos/1279330/pexels-photo-1279330.jpeg?auto=compress&cs=tinysrgb&w=1200',
    'ramen.jpg':             'https://images.pexels.com/photos/884600/pexels-photo-884600.jpeg?auto=compress&cs=tinysrgb&w=1200',
    'marina-sunset.jpg':     'https://images.pexels.com/photos/1007657/pexels-photo-1007657.jpeg?auto=compress&cs=tinysrgb&w=1200',
    'hollywood-sign.jpg':    'https://images.pexels.com/photos/1796730/pexels-photo-1796730.jpeg?auto=compress&cs=tinysrgb&w=1200',
    'range-rover.jpg':       'https://images.pexels.com/photos/919073/pexels-photo-919073.jpeg?auto=compress&cs=tinysrgb&w=1200',
    'la-palms.jpg':          'https://images.pexels.com/photos/1562058/pexels-photo-1562058.jpeg?auto=compress&cs=tinysrgb&w=1200',
    'pizza.jpg':             'https://images.pexels.com/photos/708587/pexels-photo-708587.jpeg?auto=compress&cs=tinysrgb&w=1200',
}

def is_image(data):
    if len(data) < 12: return False
    if data[:3] == b'\xff\xd8\xff': return True       # JPEG
    if data[:8].startswith(b'\x89PNG'): return True   # PNG
    if data[:4] == b'RIFF' and data[8:12] == b'WEBP': return True  # WebP
    return False

ok = 0
for name, url in RETRY.items():
    fp = os.path.join(BASE, name)
    try:
        req = urllib.request.Request(url, headers=HDRS)
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
            ct = r.headers.get('Content-Type', '')
        if not is_image(data):
            print(f'  !! {name}: non-image (ct={ct}, {len(data)}B)')
            continue
        # If webp, save as .webp - but keep requested name (browsers accept any ext)
        with open(fp, 'wb') as f:
            f.write(data)
        print(f'  OK {name}: {len(data):,}B  ct={ct}')
        ok += 1
    except Exception as e:
        print(f'  !! {name}: {e}')

print(f'Retrieved: {ok}')
