#!/usr/bin/env python3
"""
EP07 量化腳本：留任vs跳槽 + 地支刑衝害合 + 天干組合格局
===================================================================
"""

print('=' * 70)
print('Section 1: 地支相刑 — 4種')
print('=' * 70)

DIZHI_XING = {
    '無禮之刑': [('子','卯')],
    '無恩之刑': [('寅','巳'), ('巳','申'), ('寅','申')],
    '持勢之刑': [('丑','未'), ('未','戌'), ('丑','戌')],
    '自刑': [('辰','辰'), ('午','午'), ('酉','酉'), ('亥','亥')],
}

for name, pairs in DIZHI_XING.items():
    ps = '、'.join([f'{a}{b}' for a,b in pairs])
    print(f'  {name}: {ps}')
print()
print('含義：挫折、不順利')
print('測事 → 觸犯法律  測人 → 疾病/受傷痛苦')
print()

print('=' * 70)
print('Section 2: 地支相衝 — 6對')
print('=' * 70)

DIZHI_CHONG = {
    '子':'午','午':'子','丑':'未','未':'丑',
    '寅':'申','申':'寅','卯':'酉','酉':'卯',
    '辰':'戌','戌':'辰','巳':'亥','亥':'巳',
}

pairs = set()
for k,v in DIZHI_CHONG.items():
    pair = tuple(sorted([k,v]))
    if pair not in pairs:
        pairs.add(pair)
        print(f'  {k} vs {v} → 相衝')
print()
print('含義：對抗衝突 + 動 + 變化 → 逢衝必動')
print('力量大於天干相衝')
print()

print('=' * 70)
print('Section 3: 地支相害 — 6對')
print('=' * 70)

DIZHI_HAI = {
    '子':'未','未':'子','丑':'午','午':'丑',
    '寅':'巳','巳':'寅','卯':'辰','辰':'卯',
    '申':'亥','亥':'申','酉':'戌','戌':'酉',
}

pairs = set()
for k,v in DIZHI_HAI.items():
    pair = tuple(sorted([k,v]))
    if pair not in pairs:
        pairs.add(pair)
        print(f'  {k} vs {v} → 相害')
print()
print('含義：互相殘害傷害 → 兩敗俱傷')
print()

print('=' * 70)
print('Section 4: 地支相合 — 三合+六合')
print('=' * 70)

DIZHI_SANHE = [('申','子','辰'),('亥','卯','未'),('寅','午','戌'),('丑','巳','酉')]
DIZHI_LIUHE = {'子':'丑','丑':'子','寅':'亥','亥':'寅','卯':'戌','戌':'卯','辰':'酉','酉':'辰','巳':'申','申':'巳','午':'未','未':'午'}

print('三合（4組）：')
for a,b,c in DIZHI_SANHE:
    print(f'  {a}+{b}+{c} → 三合')
print()
print('六合（6對）：')
shown = set()
for k,v in DIZHI_LIUHE.items():
    p = tuple(sorted([k,v]))
    if p not in shown:
        shown.add(p)
        print(f'  {k}+{v} → 六合（和諧穩定）')
print()

print('=' * 70)
print('Section 5: 天干組合相衝 — 暗含地支邏輯')
print('=' * 70)

TIANGAN_HIDDEN_DZ = {'戊':'子','己':'戌','庚':'申','辛':'午','壬':'辰','癸':'寅'}

print('六儀遁甲：甲子戊、甲戌己、甲申庚、甲午辛、甲辰壬、甲寅癸')
print('→ 戊己庚辛壬癸 各自暗含一個地支')
print()
print('天干組合相衝的完整邏輯：')
for a, b, expected in [('戊','辛','子午衝'),('己','壬','戌辰衝'),('庚','癸','申寅衝')]:
    ha, hb = TIANGAN_HIDDEN_DZ[a], TIANGAN_HIDDEN_DZ[b]
    actual = DIZHI_CHONG.get(ha,'?')
    ok = '✅' if actual == hb else '❌'
    print(f'  {a}({ha}) + {b}({hb}) → {ha}{actual} = {expected} {ok}')
print()
print('⚠️ 這解釋了EP06的癸+庚衝格：癸(寅) + 庚(申) → 寅申衝')
print('   也解釋了辛+乙衝格：辛(午) + 乙(?) → 需要確認乙的暗含地支')
print('   但乙不屬於六儀，所以辛+乙的衝格邏輯可能不同（待確認）')
print()

print('=' * 70)
print('Section 6: 天干組合格局庫')
print('=' * 70)

TIANGAN_ZUHE = {
    ('庚','丙'): {'type':'衝格','meaning':'強烈動的信息','score':-1.5},
    ('丙','庚'): {'type':'衝格','meaning':'強烈動的信息','score':-1.5},
    ('癸','庚'): {'type':'衝格','meaning':'逢衝必動','score':-1.5},
    ('辛','乙'): {'type':'衝格','meaning':'逢衝必動','score':-1.5},
    ('乙','辛'): {'type':'衝格','meaning':'逢衝必動','score':-1.5},
    ('戊','辛'): {'type':'衝格','meaning':'子午衝(暗含)','score':-1.5},
    ('辛','戊'): {'type':'衝格','meaning':'子午衝(暗含)','score':-1.5},
    ('己','壬'): {'type':'衝格','meaning':'戌辰衝(暗含)','score':-1.5},
    ('壬','己'): {'type':'衝格','meaning':'戌辰衝(暗含)','score':-1.5},
    ('庚','癸'): {'type':'衝格','meaning':'申寅衝(暗含)','score':-1.5},
    ('癸','庚'): {'type':'衝格','meaning':'申寅衝(暗含)','score':-1.5},
    ('丁','戊'): {'type':'合格','meaning':'穩定、塵埃落定','score':1.5},
    ('戊','丁'): {'type':'合格','meaning':'穩定、塵埃落定','score':1.5},
    ('壬','丁'): {'type':'合格','meaning':'穩定','score':1.5},
    ('丁','壬'): {'type':'合格','meaning':'穩定','score':1.5},
}

chong_ge = [(k,v) for k,v in TIANGAN_ZUHE.items() if v['type']=='衝格']
he_ge = [(k,v) for k,v in TIANGAN_ZUHE.items() if v['type']=='合格']
print(f'衝格: {len(chong_ge)//2} 組（含暗含地支3組）')
for (a,b), info in chong_ge:
    if a < b: print(f'  {a}+{b}: {info["meaning"]}')
print(f'\n合格: {len(he_ge)//2} 組')
for (a,b), info in he_ge:
    if a < b: print(f'  {a}+{b}: {info["meaning"]}')
print()

print('=' * 70)
print('Section 7: 留任vs跳槽分析框架')
print('=' * 70)

print('用神：')
print('  開門 = 目前的工作/公司')
print('  日干 = 求測人自己')
print('  時干 = 新的工作/新公司')
print()
print('分析邏輯：')
print('  開門宮 vs 日干宮：')
print('    開門生日干 → 留住對求測人有利')
print('    開門剋日干 → 留住只會阻礙發展（案例結論）')
print('  時干宮 vs 日干宮：')
print('    時干生日干 → 新工作帶來有利前景（案例結論）')
print('    時干剋日干 → 新工作排斥求測人')
print('    比和 → 互相歡迎')
print()
print('案例驗證：')
print('  開門(土)落艮8 → 剋日干(水)坎1 → 留住阻礙發展')
print('  時干(金)落兌7 → 生日干(水)坎1 → 新工作有利')
print('  結論：應該接受新挑戰 ✅')
print()

print('=' * 70)
print('Section 8: 日時同宮')
print('=' * 70)

print('案例：日干壬下臨丁，丁=時干 → 日時同宮')
print('解讀：求測人心裡只有新工作，早已決定')
print('加上壬+丁 = 合格 → 穩定、塵埃落定')
print('→ 來求測只是希望得到額外認同，增強決心')
print()

print('=' * 70)
print('Section 9: 新發現的不足')
print('=' * 70)

NEW_GAPS = [
    ('G36', '高', '地支刑衝害合未納入評分',
     '概念已量化但未加入評分公式',
     '地支關係需在天干/宮位評分中考慮'),
    ('G37', '中', '天干組合格局庫仍不完整',
     '僅有衝格+合格，師傅可能還會講更多',
     '待後續集數補充'),
    ('G38', '低', '辛+乙衝格邏輯未確認',
     '乙不屬六儀，無暗含地支',
     '可能透過其他邏輯解釋，待確認'),
    ('G39', '中', '開門解讀需場景化',
     'EP05=工作職位 EP06=目前職位 EP07=目前公司',
     '需建立開門在不同場景的含義映射'),
]

for gid, priority, name, current, expected in NEW_GAPS:
    print(f'  [{priority}] {gid}: {name}')
    print(f'       現狀: {current}')
    print(f'       期望: {expected}')
    print()

print('=' * 70)
print('Section 10: 結論')
print('=' * 70)

print('EP07 核心貢獻：')
print('  1. ✅ 地支刑衝害合完整量化（刑4種+衝6對+害6對+合10組）')
print('  2. ✅ 天干組合相衝的暗含地支邏輯解釋（3組驗證通過）')
print('  3. ✅ 天干組合格局庫擴充到14條（衝格10+合格4）')
print('  4. ✅ 留任vs跳槽用神框架')
print('  5. ✅ 日時同宮 = 心理傾向已確定')
print()
print('對 back test 的影響：')
print('  - 格局（天干組合）可作為宮位評分的新維度')
print('  - 衝格=變動信號 → 二元決策特徵')
print('  - 合格=穩定 → 對投資回測的解讀方向')
print('  - 日干vs時干生剋比和 → 投資者vs投資行為的關係')
