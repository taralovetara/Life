#!/usr/bin/env python3
"""
EP27 量化腳本：犯太歲 — 傳統五種 + 奇門遁甲犯太歲
===================================================================

本集新知識點：
1. 太歲基礎：60位太歲神、值年太歲
2. 五種傳統犯太歲：值、刑、衝、害、破
3. 奇門犯太歲：用神剋年干 + 用神衝年干
4. 奇門 vs 傳統比較

自帶常數，不依賴 engine_v2.py。
"""
from datetime import datetime

print('=' * 70)
print('EP27 量化驗證：犯太歲')
print('=' * 70)

# ============================================================
# 常數定義
# ============================================================
GONG_BAGUA = {
    1: '坎', 2: '坤', 3: '震', 4: '巽',
    5: '中', 6: '乾', 7: '兌', 8: '艮', 9: '離',
}

WUXING_TG = {
    '甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土',
    '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水',
}

WUXING_KE = {
    '木': '土', '土': '水', '水': '火', '火': '金', '金': '木',
}

DIZHI = ['子','丑','寅','卯','辰','巳','午','未','申','酉','戌','亥']
SHENGXIAO = ['鼠','牛','虎','兔','龍','蛇','馬','羊','猴','雞','狗','豬']
DZ2SX = dict(zip(DIZHI, SHENGXIAO))

# 宮位相衝
GONG_CHONG = {1:9, 9:1, 2:8, 8:2, 3:7, 7:3, 4:6, 6:4}

# 地支相衝
DZ_CHONG = {d: DIZHI[(i+6)%12] for i, d in enumerate(DIZHI)}

# 地支相刑
DZ_XING = {
    '子': ['卯'], '卯': ['子'],
    '寅': ['巳','申'], '巳': ['寅','申'], '申': ['寅','巳'],
    '丑': ['戌','未'], '戌': ['丑','未'], '未': ['丑','戌'],
    '辰': ['辰'], '午': ['午'], '酉': ['酉'], '亥': ['亥'],
}

# 地支相害
DZ_HAI = {
    '子': ['未'], '未': ['子'],
    '丑': ['午'], '午': ['丑'],
    '寅': ['巳'], '巳': ['寅'],
    '卯': ['辰'], '辰': ['卯'],
    '申': ['亥'], '亥': ['申'],
    '酉': ['戌'], '戌': ['酉'],
}

# 地支相破（EP27 新增 G117）
DZ_PO = {
    '子': ['酉'], '酉': ['子'],
    '丑': ['辰'], '辰': ['丑'],
    '寅': ['亥'], '亥': ['寅'],
    '卯': ['午'], '午': ['卯'],
    '巳': ['申'], '申': ['巳'],
    '未': ['戌'], '戌': ['未'],
}

# 60位太歲神
TAISUI_SHEN_60 = {
    '甲子': '金辯', '乙丑': '陳材', '丙寅': '耿章', '丁卯': '沈興',
    '戊辰': '趙達', '己巳': '郭燦', '庚午': '王清', '辛未': '李素',
    '壬申': '洪旺', '癸酉': '康志', '甲戌': '施廣', '乙亥': '任保',
    '丙子': '郭嘉', '丁丑': '汪文', '戊寅': '魯先', '己卯': '方仲',
    '庚辰': '董德', '辛巳': '鄭但', '壬午': '陸明', '癸未': '魏仁',
    '甲申': '方傑', '乙酉': '蔣崇', '丙戌': '白敏', '丁亥': '封濟',
    '戊子': '鄒鐺', '己丑': '潘佐', '庚寅': '鄔桓', '辛卯': '范寧',
    '壬辰': '彭泰', '癸巳': '徐單', '甲午': '章詞', '乙未': '楊仙',
    '丙申': '管仲', '丁酉': '康傑', '戊戌': '姜武', '己亥': '謝太',
    '庚子': '盧秘', '辛丑': '楊信', '壬寅': '賀諤', '癸卯': '皮時',
    '甲辰': '李誠', '乙巳': '吳遂', '丙午': '文哲', '丁未': '繆丙',
    '戊申': '俞志', '己酉': '程寶', '庚戌': '倪秘', '辛亥': '葉堅',
    '壬子': '丘德', '癸丑': '朱得', '甲寅': '張朝', '乙卯': '萬清',
    '丙辰': '辛亞', '丁巳': '楊彥', '戊午': '黎卿', '己未': '傅黨',
    '庚申': '毛梓', '辛酉': '文政', '壬戌': '洪計', '癸亥': '虞程',
}

# ============================================================
# Section 1: 60位太歲神驗證
# ============================================================
print('\n' + '=' * 70)
print('Section 1: 60位太歲神')
print('=' * 70)

print(f'\n  太歲神總數: {len(TAISUI_SHEN_60)}')
print(f'  完整性: {"PASS" if len(TAISUI_SHEN_60) == 60 else "FAIL"}')
print(f'  2022 壬寅年太歲神: {TAISUI_SHEN_60.get("壬寅", "未知")} (應為賀諤)')

# ============================================================
# Section 2: 五種傳統犯太歲
# ============================================================
print('\n' + '=' * 70)
print('Section 2: 五種傳統犯太歲')
print('=' * 70)

def check_traditional_fan_taisui(year_dz):
    results = {'zhi': [], 'xing': [], 'chong': [], 'hai': [], 'po': []}
    for dz in DIZHI:
        sx = DZ2SX[dz]
        if dz == year_dz:
            results['zhi'].append(sx)
        if year_dz in DZ_XING.get(dz, []) or dz in DZ_XING.get(year_dz, []):
            results['xing'].append(sx)
        if DZ_CHONG.get(dz) == year_dz:
            results['chong'].append(sx)
        if year_dz in DZ_HAI.get(dz, []) or dz in DZ_HAI.get(year_dz, []):
            results['hai'].append(sx)
        if year_dz in DZ_PO.get(dz, []) or dz in DZ_PO.get(year_dz, []):
            results['po'].append(sx)
    return results

# 以幾個年份為例
for year_gz, year_dz in [('壬寅','寅'), ('癸卯','卯'), ('丙午','午')]:
    r = check_traditional_fan_taisui(year_dz)
    all_fan = set()
    for v in r.values():
        all_fan.update(v)
    print(f'\n  {year_gz}年 ({DZ2SX[year_dz]}年) 太歲神 {TAISUI_SHEN_60[year_gz]}:')
    print(f'    值太歲: {r["zhi"]}')
    print(f'    刑太歲: {r["xing"]}')
    print(f'    衝太歲: {r["chong"]}')
    print(f'    害太歲: {r["hai"]}')
    print(f'    破太歲: {r["po"]}')
    print(f'    犯太歲生肖: {sorted(all_fan)}')

# 驗證每個生肖都遇到五種
print(f'\n  驗證: 每個生肖都會遇到五種犯太歲?')
all_ok = True
for dz in DIZHI:
    r = check_traditional_fan_taisui(dz)
    for k in ['zhi','xing','chong','hai','po']:
        if not r[k]:
            all_ok = False
            print(f'    {DZ2SX[dz]}年: {k}為空!')
if all_ok:
    print(f'    PASS')

# ============================================================
# Section 3: 地支相破表（EP27 新增）
# ============================================================
print('\n' + '=' * 70)
print('Section 3: 地支相破表 DZ_PO (EP27 新增 G117)')
print('=' * 70)

po_pairs = set()
for dz, targets in sorted(DZ_PO.items()):
    for t in targets:
        pair = tuple(sorted([dz, t]))
        if pair not in po_pairs:
            po_pairs.add(pair)
            print(f'    {DZ2SX[pair[0]]}({pair[0]}) - {DZ2SX[pair[1]]}({pair[1]})')
print(f'\n  相破對總數: {len(po_pairs)} (應為6)')

# ============================================================
# Section 4: 奇門犯太歲邏輯
# ============================================================
print('\n' + '=' * 70)
print('Section 4: 奇門犯太歲邏輯')
print('=' * 70)

def wuxing_ke(wx_a, wx_b):
    return WUXING_KE.get(wx_a) == wx_b

print(f'\n  核心規則:')
print(f'    用神宮剋年干宮 -> 犯太歲（以下犯上）')
print(f'    用神宮衝年干宮 -> 犯太歲（宮位對衝）')
print(f'    年干宮剋用神宮 -> 不算（上管下正常）')

# 模擬: 年干壬(水)落坎1宮
niangan_wx = '水'
niangan_palace = 1

scenarios = [
    ('戊(土)', '土', 9, '離9宮'),
    ('甲(木)', '木', 3, '震3宮'),
    ('丙(火)', '火', 9, '離9宮'),
    ('庚(金)', '金', 3, '震3宮'),
    ('宮位衝', None, 9, '離9宮(衝坎1)'),
]

print(f'\n  模擬: 年干壬(水)落坎1宮')
print(f'  {"用神":10s} {"落宮":12s} {"剋?":4s} {"衝?":4s} {"犯太歲"}')
for name, wx, palace, desc in scenarios:
    ke = wuxing_ke(wx, niangan_wx) if wx else False
    chong = GONG_CHONG.get(palace) == niangan_palace
    fan = 'YES' if (ke or chong) else 'NO'
    reason = []
    if ke: reason.append('剋')
    if chong: reason.append('衝')
    reason_str = '+'.join(reason) if reason else '-'
    print(f'  {name:10s} {desc:12s} {"YES" if ke else "NO":4s} {"YES" if chong else "NO":4s} {fan} ({reason_str})')

# ============================================================
# Section 5: 年干剋用神 vs 用神剋年干
# ============================================================
print('\n' + '=' * 70)
print('Section 5: 方向性區分（關鍵）')
print('=' * 70)

print(f'\n  案例1: 年干壬(水)坎1 vs 用神戊(土)離9')
print(f'    戊土剋壬水? -> YES -> 犯太歲!')
print(f'    壬水剋戊土? -> NO')

print(f'\n  案例2: 年干庚(金)乾6 vs 用神甲(木)巽4')
print(f'    甲木剋庚金? -> NO')
print(f'    巽4衝乾6? -> YES -> 犯太歲!')
print(f'    庚金剋甲木? -> YES -> 不算(上管下)')

# ============================================================
# Section 6: 奇門 vs 傳統比較
# ============================================================
print('\n' + '=' * 70)
print('Section 6: 奇門 vs 傳統犯太歲')
print('=' * 70)

comparisons = [
    ('精準度', '高（針對個人盤面）', '低（1/12人口）'),
    ('對象', '求測人本人（唯一性）', '整個生肖'),
    ('方法', '用神宮 vs 年干宮', '生肖 vs 年份地支'),
    ('實用性', '可查任何年份', '僅當年'),
    ('層次', '高', '低'),
]

print(f'\n  {"維度":8s} {"奇門遁甲":20s} {"傳統生肖":20s}')
for dim, qm, trad in comparisons:
    print(f'  {dim:8s} {qm:20s} {trad:20s}')

# ============================================================
# Section 7: G-ID 總結
# ============================================================
print('\n' + '=' * 70)
print('Section 7: EP27 新增 G-ID')
print('=' * 70)

gaps = [
    ('G112', '奇門犯太歲函數未實現 detect_fan_taisui()'),
    ('G113', '年干落宮查找函數未建立 find_niangan_palace()'),
    ('G114', '年支宮對犯太歲的補充影響未量化'),
    ('G115', '其他年份太歲查詢函數未建立'),
    ('G116', '60位太歲神名錄表未建立'),
    ('G117', '十二地支相破表 DZ_PO 未在引擎中定義'),
]

for gid, desc in gaps:
    print(f'  {gid}: {desc}')
print(f'\n  EP27 總計新增 {len(gaps)} 個 G-ID')

print('\n' + '=' * 70)
print('EP27 量化完成')
print('=' * 70)
