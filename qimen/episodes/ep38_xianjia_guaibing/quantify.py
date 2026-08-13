#!/usr/bin/env python3
"""
EP38 量化腳本：仙家怪病 — 螣蛇落宮鎖定五位仙家
===================================================================

本集新知識點：
1. 五位仙家定義與五行對應
2. 螣蛇落宮診斷法
3. 五行-宮位-仙家完整映射

自帶常數，不依賴 engine_v2.py。
"""

print('=' * 70)
print('EP38 量化驗證：仙家怪病')
print('=' * 70)

# ============================================================
# 常數
# ============================================================
PALACE_WX = {1:'水',2:'土',3:'木',4:'木',6:'金',7:'金',8:'土',9:'火'}

XIANGJIA = {
    '胡仙': {'animal':'狐狸','title':'胡三爺','wuxing':'火','color':'紅色','trait':'法力高、恩怨分明'},
    '黃仙': {'animal':'黃鼠狼','title':'黃二爺','wuxing':'土','color':'黃色','trait':'附身能力極強、特別記仇'},
    '白仙': {'animal':'白色刺猬','title':'白老太','wuxing':'金','color':'白色','trait':'心性定力最強、善良好醫術'},
    '柳仙': {'animal':'蛇','title':'柳先生','wuxing':'木','color':'植物','trait':'靈氣高、千里攝魂'},
    '灰仙': {'animal':'老鼠','title':'灰四爺','wuxing':'水','color':'灰色/玄色','trait':'智慧高、倉神/財神'},
}

# 宮位→仙家映射
GONG_XIANJIA = {
    9: '胡仙',
    2: '黃仙', 8: '黃仙',
    6: '白仙', 7: '白仙',
    3: '柳仙', 4: '柳仙',
    1: '灰仙',
}

# ============================================================
# Section 1: 五位仙家總表
# ============================================================
print('\n' + '=' * 70)
print('Section 1: 五位仙家總表')
print('=' * 70)

print(f'\n  {"仙家":6s}  {"動物":8s}  {"尊稱":8s}  {"五行":4s}  {"顏色":8s}  {"特徵"}')
for name, info in XIANGJIA.items():
    print(f'  {name:6s}  {info["animal"]:8s}  {info["title"]:8s}  {info["wuxing"]:4s}  {info["color"]:8s}  {info["trait"]}')

# ============================================================
# Section 2: 螣蛇落宮診斷法
# ============================================================
print('\n' + '=' * 70)
print('Section 2: 螣蛇落宮→仙家診斷')
print('=' * 70)

print(f'\n  {"螣蛇落宮":10s}  {"宮位五行":8s}  {"對應仙家":8s}  {"動物"}')
for gong in [1,2,3,4,6,7,8,9]:
    wx = PALACE_WX[gong]
    xj = GONG_XIANJIA.get(gong, '?')
    animal = XIANGJIA[xj]['animal'] if xj in XIANGJIA else '?'
    print(f'  {gong:>2d}宮        {wx:8s}  {xj:8s}  {animal}')

# ============================================================
# Section 3: 診斷函數
# ============================================================
print('\n' + '=' * 70)
print('Section 3: 仙家診斷函數驗證')
print('=' * 70)

def xianjia_diagnose(tengshe_gong):
    """根據螣蛇落宮診斷仙家"""
    xj_name = GONG_XIANJIA.get(tengshe_gong)
    if xj_name is None:
        return None
    info = XIANGJIA[xj_name]
    return {
        'gong': tengshe_gong,
        'wuxing': PALACE_WX[tengshe_gong],
        'xianjia': xj_name,
        'animal': info['animal'],
        'title': info['title'],
    }

# 測試所有宮位
for gong in [1,3,5,7,9]:
    result = xianjia_diagnose(gong)
    if result:
        print(f'  螣蛇落{result["gong"]}宮({result["wuxing"]}) -> {result["xianjia"]}({result["title"]}) = {result["animal"]}')
    else:
        print(f'  螣蛇落{gong}宮 -> 無對應仙家 (中五宮)')

# ============================================================
# Section 4: EP38 新增 G-ID
# ============================================================
print('\n' + '=' * 70)
print('Section 4: EP38 新增 G-ID')
print('=' * 70)

gaps = [
    ('G166', '螣蛇落宮→仙家診斷函數未建立'),
    ('G167', '螣蛇多重角色映射未系統化'),
    ('G168', '五位仙家五行對應常數表未建立'),
]

for gid, desc in gaps:
    print(f'  {gid}: {desc}')
print(f'\n  EP38 總計新增 {len(gaps)} 個 G-ID')
print(f'  累計 G-ID: G001-G168 (共168個)')

print('\n' + '=' * 70)
print('EP38 量化完成')
print('=' * 70)
