#!/usr/bin/env python3
"""
EP22 量化腳本：轉盤四盤完整排布 + 驛馬計算 + 空亡整合
===================================================================

本集新知識點：
1. 後天八卦順/逆時針8宮序（轉盤核心）
2. 天盤排布：值符確定 → 位移計算 → 九星+天干旋轉
3. 人盤排布：值使確定 → 時宮飛布 → 八門反向排列
4. 神盤排布：小值符跟大值符，其餘順/逆排
5. 驛馬口訣計算（G32 解決）
6. 空亡計算（G27 解決）
7. 九星本宮映射
"""
import sys
sys.path.insert(0, '../../')
from engine_v2 import (
    JIUXING_HOME, JIUXING_HOME_R,
    BAGUA_CW_8, BAGUA_CCW_8,
    LUOSHU_9_YANG, LUOSHU_9_YIN,
    LUOSHU_8_YANG, LUOSHU_8_YIN,
    YIMA_MAP, XUNKONG_MAP,
    DZ2GONG, DZ_CHONG, GONG_BAGUA,
    STAR_DOOR, XUNSHOU_DUNYI, LIUJIAZI, XUNSHOU_IDX,
    calc_yima, get_xunkong,
    qiju_v2, print_chart_v2,
)
from datetime import datetime

print('=' * 70)
print('EP22 量化驗證：轉盤四盤排布 + 驛馬 + 空亡')
print('=' * 70)

# ============================================================
# Section 1: 後天八卦8宮序驗證
# ============================================================
print('\n' + '=' * 70)
print('Section 1: 後天八卦8宮序')
print('=' * 70)

print(f'  陽遁順時針: {BAGUA_CW_8}')
print(f'  陰遁逆時針: {BAGUA_CCW_8}')

# 驗證：相鄰宮位確實是後天八卦相鄰方位
bagua_names = {1:'坎(北)',8:'艮(東北)',3:'震(東)',4:'巽(東南)',
              9:'離(南)',2:'坤(西南)',7:'兌(西)',6:'乾(西北)'}
print('\n  陽遁方位序列:')
for i, p in enumerate(BAGUA_CW_8):
    arrow = ' → ' if i < len(BAGUA_CW_8)-1 else ''
    print(f'    {bagua_names[p]}{arrow}', end='')
print()

# 驗證陰遁係陽遁嘅反轉
print(f'\n  陰遁=陽遁反轉: {BAGUA_CCW_8 == list(reversed(BAGUA_CW_8))}')

# ============================================================
# Section 2: 洛書飛布序
# ============================================================
print('\n' + '=' * 70)
print('Section 2: 洛書飛布序')
print('=' * 70)

print(f'  9宮陽遁(含中5): {LUOSHU_9_YANG}')
print(f'  9宮陰遁(含中5): {LUOSHU_9_YIN}')
print(f'  8宮陽遁(不含中5): {LUOSHU_8_YANG}')
print(f'  8宮陰遁(不含中5): {LUOSHU_8_YIN}')

# 驗證9宮陽遁=1-9順序
print(f'\n  9宮陽遁=1到9: {LUOSHU_9_YANG == list(range(1,10))}')
print(f'  9宮陰遁=9到1: {LUOSHU_9_YIN == list(range(9,0,-1))}')

# ============================================================
# Section 3: 九星本宮映射
# ============================================================
print('\n' + '=' * 70)
print('Section 3: 九星本宮映射')
print('=' * 70)

print('\n  宮位 → 原始天星 (JIUXING_HOME):')
for p in range(1, 10):
    star = JIUXING_HOME[p]
    print(f'    {GONG_BAGUA[p]}{p}宮 → {star}')

print('\n  反向映射 (星名 → 本宮 JIUXING_HOME_R):')
for star, home in sorted(JIUXING_HOME_R.items()):
    print(f'    {star} → {GONG_BAGUA[home]}{home}宮')

# ============================================================
# Section 4: 值符值使對應關係
# ============================================================
print('\n' + '=' * 70)
print('Section 4: 值符值使固定對應')
print('=' * 70)

print('\n  大值符(星) ↔ 值使(門):')
for star, door in STAR_DOOR.items():
    home = JIUXING_HOME_R.get(star, '?')
    print(f'    {star}({GONG_BAGUA.get(home,"?")}{home}宮) ↔ {door}')

# ============================================================
# Section 5: 驛馬口訣驗證（G32 解決）
# ============================================================
print('\n' + '=' * 70)
print('Section 5: 驛馬口訣 (G32 解決)')
print('=' * 70)

yima_groups = [
    ('申子辰在寅', ['申','子','辰'], '寅'),
    ('寅午戌在申', ['寅','午','戌'], '申'),
    ('巳酉丑在亥', ['巳','酉','丑'], '亥'),
    ('亥卯未在巳', ['亥','卯','未'], '巳'),
]

print('\n  口訣驗證:')
for motto, dzs, ym in yima_groups:
    results = []
    for dz in dzs:
        actual = YIMA_MAP.get(dz, '?')
        ok = '✓' if actual == ym else '✗'
        results.append(f'{dz}→{actual}{ok}')
    print(f'    {motto}: {" | ".join(results)}')

# 完整12地支驛馬表
print('\n  完整12地支驛馬表:')
for dz in ['子','丑','寅','卯','辰','巳','午','未','申','酉','戌','亥']:
    ym = YIMA_MAP.get(dz, '?')
    palace = DZ2GONG.get(ym, 0)
    print(f'    {dz} → 驛馬{ym} ({GONG_BAGUA.get(palace,'?')}{palace}宮)')

# ============================================================
# Section 6: 空亡計算驗證（G27 解決）
# ============================================================
print('\n' + '=' * 70)
print('Section 6: 空亡計算 (G27 解決)')
print('=' * 70)

print('\n  每旬空亡地支 (XUNKONG_MAP):')
for xs_name in ['甲子','甲戌','甲申','甲午','甲辰','甲寅']:
    kong = XUNKONG_MAP[xs_name]
    print(f'    {xs_name}旬 → 空亡: {kong[0]}、{kong[1]}')

# 驗證：空亡地支確實唔在該旬60甲子中
print('\n  驗證空亡地支唔在該旬:')
for xs_idx in XUNSHOU_IDX:
    xs_name = LIUJIAZI[xs_idx]
    kong = XUNKONG_MAP[xs_name]
    # 該旬的10個干支
    xs_jz = [LIUJIAZI[xs_idx+i] for i in range(10)]
    xs_dz = set(jz[1] for jz in xs_jz)
    for k in kong:
        ok = '✓' if k not in xs_dz else '✗'
        print(f'    {xs_name}旬: {k} 不在該旬{ok}')

# ============================================================
# Section 7: 實際起局驗證
# ============================================================
print('\n' + '=' * 70)
print('Section 7: 實際起局驗證（轉盤 V2）')
print('=' * 70)

test_time = datetime(2026, 8, 8, 9, 30)  # 巳時
r = qiju_v2(test_time)
print_chart_v2(r, 'EP22 轉盤起局測試')

# 空亡 + 驛馬 輸出
kw = r.get('kongwang', {})
ym = r.get('yima', {})
print(f'\n  空亡地支: {kw.get("dz", [])}')
print(f'  空亡宮位: {[GONG_BAGUA.get(p,p) for p in kw.get("palaces", [])]}')
print(f'  驛馬: {ym.get("dz", "?")} ({GONG_BAGUA.get(ym.get("palace",0), "?")}{ym.get("palace",0)}宮)')

# 驗證四盤完整性
print('\n  四盤完整性檢查:')
for layer_name, layer_data in [('地盤dp', r['dp']), ('天盤tg', r['tg']), ('人盤rp', r['rp']), ('神盤sp', r['sp'])]:
    count = len(layer_data)
    print(f'    {layer_name}: {count}宮 {"✓" if count == 8 or (count == 9 and 5 in layer_data) else "✗"}')

print('\n' + '=' * 70)
print('EP22 量化完成')
print('=' * 70)