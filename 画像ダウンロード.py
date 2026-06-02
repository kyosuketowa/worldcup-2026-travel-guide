"""Download images for travel guide from Pexels (free/public)."""
import urllib.request
import os
import sys

BASE = r'C:/Users/kyosu/worldカップ旅行/images'
os.makedirs(BASE, exist_ok=True)

HDRS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}

# Pexels direct photo URLs (free, no auth needed)
# ?auto=compress&cs=tinysrgb&w=1200 gives optimized 1200px width
IMG = {
    'nyc-skyline.jpg':       'https://images.pexels.com/photos/374870/pexels-photo-374870.jpeg?auto=compress&cs=tinysrgb&w=1600',
    'statue-of-liberty.jpg': 'https://images.pexels.com/photos/356830/pexels-photo-356830.jpeg?auto=compress&cs=tinysrgb&w=1200',
    'times-square.jpg':      'https://images.pexels.com/photos/2404046/pexels-photo-2404046.jpeg?auto=compress&cs=tinysrgb&w=1200',
    'brooklyn-bridge.jpg':   'https://images.pexels.com/photos/3586966/pexels-photo-3586966.jpeg?auto=compress&cs=tinysrgb&w=1200',
    'dumbo-manhattan.jpg':   'https://images.pexels.com/photos/2224861/pexels-photo-2224861.jpeg?auto=compress&cs=tinysrgb&w=1200',
    'central-park.jpg':      'https://images.pexels.com/photos/1486577/pexels-photo-1486577.jpeg?auto=compress&cs=tinysrgb&w=1200',
    'italian-food.jpg':      'https://images.pexels.com/photos/1279330/pexels-photo-1279330.jpeg?auto=compress&cs=tinysrgb&w=1200',
    'bagel.jpg':             'https://images.pexels.com/photos/2228405/pexels-photo-2228405.jpeg?auto=compress&cs=tinysrgb&w=1200',
    'ramen.jpg':             'https://images.pexels.com/photos/884600/pexels-photo-884600.jpeg?auto=compress&cs=tinysrgb&w=1200',
    'roller-coaster.jpg':    'https://images.pexels.com/photos/2220336/pexels-photo-2220336.jpeg?auto=compress&cs=tinysrgb&w=1200',
    'water-park.jpg':        'https://images.pexels.com/photos/261101/pexels-photo-261101.jpeg?auto=compress&cs=tinysrgb&w=1200',
    'stadium.jpg':           'https://images.pexels.com/photos/46798/the-ball-stadion-football-the-pitch-46798.jpeg?auto=compress&cs=tinysrgb&w=1200',
    'seafood.jpg':           'https://images.pexels.com/photos/725992/pexels-photo-725992.jpeg?auto=compress&cs=tinysrgb&w=1200',
    'disneyland-castle.jpg': 'https://images.pexels.com/photos/2403211/pexels-photo-2403211.jpeg?auto=compress&cs=tinysrgb&w=1200',
    'airplane.jpg':          'https://images.pexels.com/photos/2026324/pexels-photo-2026324.jpeg?auto=compress&cs=tinysrgb&w=1200',
    'dallas-skyline.jpg':    'https://images.pexels.com/photos/2389349/pexels-photo-2389349.jpeg?auto=compress&cs=tinysrgb&w=1200',
    'marina-sunset.jpg':     'https://images.pexels.com/photos/1007657/pexels-photo-1007657.jpeg?auto=compress&cs=tinysrgb&w=1200',
    'hollywood-sign.jpg':    'https://images.pexels.com/photos/2563611/pexels-photo-2563611.jpeg?auto=compress&cs=tinysrgb&w=1200',
    'griffith.jpg':          'https://images.pexels.com/photos/1136575/pexels-photo-1136575.jpeg?auto=compress&cs=tinysrgb&w=1200',
    'range-rover.jpg':       'https://images.pexels.com/photos/919073/pexels-photo-919073.jpeg?auto=compress&cs=tinysrgb&w=1200',
}

ok, fail = 0, 0
for name, url in IMG.items():
    fp = os.path.join(BASE, name)
    try:
        req = urllib.request.Request(url, headers=HDRS)
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
            ct = r.headers.get('Content-Type', '')
        # sanity check
        if not data[:3] in (b'\xff\xd8\xff', b'\x89PN'):
            print(f'  !! {name}: non-image response (ct={ct}, {len(data)}B)')
            fail += 1
            continue
        with open(fp, 'wb') as f:
            f.write(data)
        print(f'  OK {name}: {len(data):,}B  ct={ct}')
        ok += 1
    except Exception as e:
        print(f'  !! {name}: {e}')
        fail += 1

print(f'\n=== Done: {ok} ok / {fail} failed ===')
sys.exit(0 if ok > 0 else 1)
