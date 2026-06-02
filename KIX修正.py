"""伊丹/ITM → 関空/KIX に全置換。"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path

PATH = Path(r'C:/Users/kyosu/worldカップ旅行/travel-guide-v7.html')
html = PATH.read_text(encoding='utf-8')

REPLACEMENTS = [
    # 日本語：伊丹 → 関空
    ('18:25 NH095 で伊丹へ',        '18:25 NH095 で関空へ'),
    ('18:25 NH095 で伊丹空港へ',    '18:25 NH095 で関西空港へ'),
    ('羽田 → 伊丹',                 '羽田 → 関空'),
    ('6/20 (土) 19:50 ITM',         '6/20 (土) 19:50 KIX'),
    ('HND → ITM (6/20 18:25)',      'HND → KIX (6/20 18:25)'),
    ('HND → ITM',                   'HND → KIX'),
    ('🛬 伊丹到着',                  '🛬 関空到着'),
    ('→ 19:50 ITM',                 '→ 19:50 KIX'),
    ('19:50 伊丹',                   '19:50 関空'),
    # Leaflet data d19 の名称
    ('name:\'羽田 HND（機中泊）',    "name:'羽田 HND（機中泊）"),  # 変更なし(羽田は合ってる)
    # 関空の緯度経度も修正（d19最終到着の国内線レッグがあれば）
]

applied = 0
for old, new in REPLACEMENTS:
    if old == new:
        continue
    count = html.count(old)
    if count > 0:
        html = html.replace(old, new)
        print(f'  ✅ "{old[:50]}" × {count}')
        applied += count

# 念のため：もし "伊丹" が残っていたら全部 "関空" に
remain_itami = html.count('伊丹')
if remain_itami:
    html = html.replace('伊丹', '関空')
    print(f'  ✅ 残り"伊丹" × {remain_itami}件も関空に')
    applied += remain_itami

remain_itm = html.count(' ITM')  # 空白付きで検出
if remain_itm:
    html = html.replace(' ITM', ' KIX')
    print(f'  ✅ 残り" ITM" × {remain_itm}件も KIX に')
    applied += remain_itm

PATH.write_text(html, encoding='utf-8')
print(f'\n=== {applied}件置換 size={len(html):,}B ===')
