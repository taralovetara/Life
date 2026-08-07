#!/usr/bin/env python3
"""
EP14 量化腳本：李某某拘留事件案例分析 + 起念/外應 + 天干與宮位相衝
===================================================================

本集新知識點：
1. 起念原則（問事測事一定要在求測人起念的時間點起局）
2. 外應概念（外在環境突變 → 觸發起念 → 此時起局最準）
3. 天干與宮位地支相衝（NEW：壬暗含辰 vs 乾六含戌 → 辰戌相衝）
4. 兩種「衝」的區別（天干組合衝 vs 天干vs宮位衝）
5. 丁+壬 = 淫蕩之合（合格的一種，道德負面）
6. 辛 = 罪犯/被抓的人（犯罪用神）
7. 月干 = 舉報者/熟人通風報信
8. 三奇希望特性差異（乙=慢/婉轉/拖拉）
9. 寄宮在感情中的含義（寄宮=非正室）
10. 壬 = 嫌疑人/當事人
"""

import json

PALACE_WUXING = {1:'水', 2:'土', 3:'木', 4:'木', 5:'土', 6:'金', 7:'金', 8:'土', 9:'火'}
GONG_NAMES = {1:'坎', 2:'坤', 3:'震', 4:'巽', 5:'中', 6:'乾', 7:'兌', 8:'艮', 9:'離'}
WUXING_SHENG = {"金": "水", "水": "木", "木": "火", "火": "土", "土": "金"}
WUXING_KE   = {"金": "木", "木": "土", "土": "水", "水": "火", "火": "金"}

# ============================================================
# Section 1: 起念原則與外應
# ============================================================
print('=' * 70)
print('Section 1: 起念原則與外應')
print('=' * 70)

QINIAN = {
    'definition': '求測人突然想起想要問事測事的時刻',
    'rule': '起局一定要在起念的時間點',
    'why': '此時宇宙狀態與求測人的意念同步，分析才準確',
}

WAIYING = {
    'definition': '外在環境突然發生變化，觸發起念',
    'example': '鴿子飛入房間、突然聽到某個聲音、看到某個現象',
    'usage': '外應出現 → 心血來潮起念 → 立即用此刻時間起局',
}

print('\n起念原則：')
for k, v in QINIAN.items():
    print(f'  {k}: {v}')

print('\n外應：')
for k, v in WAIYING.items():
    print(f'  {k}: {v}')

print('\n⚠️ 師傅特別強調：起局原則會在以後的視頻詳細介紹')
print('   → 這是一個重要但尚未完整講解的概念')
print()

# ============================================================
# Section 2: 天干與宮位地支相衝（重大新發現）
# ============================================================
print('=' * 70)
print('Section 2: 天干與宮位地支相衝（重大新發現）')
print('=' * 70)

print('\n之前認識的「衝」只有一種：')
print('  G61: 天盤干暗含地支 vs 地盤干暗含地支 → 衝格')
print('  例: 庚(申)+癸(寅) → 申寅相衝 → 衝格')
print()
print('EP14 新發現第二種「衝」：')
print('  天盤干暗含地支 vs 落宮包含的地支 → 逢衝必動')
print('  例: 壬(辰)落乾六宮(戌) → 辰戌相衝 → 逢衝必動')
print()

# 暗含地支
TIANGAN_HIDDEN_DZ = {
    '戊': '子', '己': '戌', '庚': '申',
    '辛': '午', '壬': '辰', '癸': '寅',
}

# 宮位地支（八宮各包含哪些地支）
# 根據奇門遁甲，每宮包含特定的地支
PALACE_DIZHI = {
    1: ['子'],         # 坎
    2: ['未','申'],     # 坤
    3: ['卯'],         # 震
    4: ['辰','巳'],     # 巽
    5: [],             # 中（無地支）
    6: ['戌','亥'],     # 乾
    7: ['酉'],         # 兌
    8: ['丑','寅'],     # 艮
    9: ['午'],         # 離
}

# 六衝
LIUCHONG = [('子','午'), ('丑','未'), ('寅','申'), ('卯','酉'), ('辰','戌'), ('巳','亥')]

def is_palace_chong(tiangan, palace):
    """檢查天干暗含地支是否與落宮地支相衝"""
    if tiangan not in TIANGAN_HIDDEN_DZ:
        return False, None
    tg_dz = TIANGAN_HIDDEN_DZ[tiangan]
    palace_dzs = PALACE_DIZHI.get(palace, [])
    for pdz in palace_dzs:
        for c1, c2 in LIUCHONG:
            if (tg_dz == c1 and pdz == c2) or (tg_dz == c2 and pdz == c1):
                return True, f'{tg_dz}{pdz}相衝'
    return False, None

def is_ganze_chong(tian_gan, di_gan):
    """G61: 天干組合衝格"""
    if tian_gan not in TIANGAN_HIDDEN_DZ or di_gan not in TIANGAN_HIDDEN_DZ:
        return False, None
    dz_tp = TIANGAN_HIDDEN_DZ[tian_gan]
    dz_dp = TIANGAN_HIDDEN_DZ[di_gan]
    for c1, c2 in LIUCHONG:
        if (dz_tp == c1 and dz_dp == c2) or (dz_tp == c2 and dz_dp == c1):
            return True, f'{dz_tp}{dz_dp}相衝'
    return False, None

print('兩種「衝」的對照：')
print(f'  {"類型":<20} {"機制":<35} {"含義"}')
print('  ' + '-' * 75)
print(f'  {"天干組合衝(G61)":<20} {"天盤干地支 vs 地盤干地支":<35} {"衝格（格局）"}')
print(f'  {"天干宮位衝(NEW)":<20} {"天盤干地支 vs 落宮地支":<35} {"逢衝必動（動態）"}')
print()

print('驗證案例（EP14 李某某）：')
print(f'  壬(暗含辰) 落乾六宮(戌亥) → ', end='')
is_c, r = is_palace_chong('壬', 6)
print(f'{"辰戌相衝 ✅" if is_c else "非衝"}')
print(f'  → 逢衝必動，李某某一定會被放出來')
print()

# 掃描所有天干×宮位的相衝
print('所有天干×宮位的相衝組合：')
palace_chong_all = []
for tg in TIANGAN_HIDDEN_DZ:
    for p in range(1, 10):
        is_c, reason = is_palace_chong(tg, p)
        if is_c:
            palace_chong_all.append((tg, p, reason))
            print(f'  {tg}({TIANGAN_HIDDEN_DZ[tg]}) 落 {GONG_NAMES[p]}{p}宮({"/".join(PALACE_DIZHI[p])}) → {reason}')
print(f'\n共 {len(palace_chong_all)} 個天干×宮位相衝組合')
print()

# ============================================================
# Section 3: 新天干組合
# ============================================================
print('=' * 70)
print('Section 3: EP14 新天干組合')
print('=' * 70)

EP14_ZUHE = {
    ('丁', '壬'): {
        'name': '淫蕩之合',
        'type': '合格（道德負面）',
        'detail': '會做一些純粹肉慾關係的男女之事',
        'source': 'EP14 李某某案例（地盤壬宮）',
        'note': '合格的一種，但在道德層面是負面的',
    },
    ('壬', '癸'): {
        'name': '（師傅未命名）',
        'type': '待確認',
        'detail': '與拘留、風化事件相關',
        'source': 'EP14 李某某案例（天盤壬宮）',
        'note': '天盤壬+癸，師傅用來判斷因風化事件被拘留',
    },
}

print('EP14 新天干組合：')
for (a, b), info in EP14_ZUHE.items():
    print(f'  {a}+{b}: {info["name"]}')
    print(f'    類型: {info["type"]}')
    print(f'    詳情: {info["detail"]}')
    print(f'    來源: {info["source"]}')
    print()

# 丁+壬 與之前記錄對照
print('丁+壬 與之前集數對照：')
print('  EP07: 丁+壬 = 合格（穩定）— 格局系統')
print('  EP08: 丁+壬 = 產品種類多 — 下臨組合解讀')
print('  EP14: 丁+壬 = 淫蕩之合 — 合格的道德負面')
print('  ⚠️ 同一組合三種解讀 → G47 再次確認：天干組合解讀必須考慮場景')
print()

# ============================================================
# Section 4: 新用神含義
# ============================================================
print('=' * 70)
print('Section 4: EP14 新用神含義')
print('=' * 70)

NEW_YONGSHEN = {
    '壬': {
        'new_meaning': '嫌疑人/當事人（犯罪場景）',
        'previous': '水、血液、動脈（EP13人體）、時干（多集）',
        'source': 'EP14 李某某案例',
    },
    '辛': {
        'new_meaning': '罪犯/被抓的人',
        'previous': '金、肺部（EP13人體）、天干組合',
        'source': 'EP14 李某某案例',
    },
    '月干': {
        'new_meaning': '舉報者/通風報信的熟人',
        'previous': '平輩/同事/朋友（EP04）',
        'source': 'EP14 李某某案例',
    },
    '值符': {
        'new_meaning': '知名度高/名人',
        'previous': '最吉神/高貴（EP03-EP12）',
        'source': 'EP14 李某某案例',
    },
    '九天': {
        'new_meaning_confirmed': '坐飛機/空中交通',
        'previous': '科技/雲端/高處（EP12）',
        'source': 'EP14 李某某案例（機場被捕說法可信）',
    },
}

print('新用神含義：')
for sym, info in NEW_YONGSHEN.items():
    key = 'new_meaning_confirmed' if 'new_meaning_confirmed' in info else 'new_meaning'
    print(f'  {sym}:')
    print(f'    新含義: {info[key]}')
    print(f'    之前: {info["previous"]}')
    print()

# ============================================================
# Section 5: 三奇希望特性差異
# ============================================================
print('=' * 70)
print('Section 5: 三奇希望特性差異')
print('=' * 70)

SANQI_HOPE = {
    '乙': {
        'nature': '希望/奇蹟來得不夠直接',
        'character': '慢、婉轉、拖拉',
        'implication': '有希望但過程漫長、不會很快解決',
    },
    '丙': {
        'nature': '（師傅未在本集詳述）',
        'character': '待補充',
        'implication': '待補充',
    },
    '丁': {
        'nature': '（師傅未在本集詳述）',
        'character': '待補充',
        'implication': '待補充',
    },
}

print('三奇代表希望和奇蹟，但各有特性：')
for qi, info in SANQI_HOPE.items():
    print(f'  {qi}奇: {info["nature"]} — {info["character"]}')

print('\n案例應用：')
print('  辛(罪犯) 落震三宮，下臨乙奇')
print('  乙奇 = 希望但慢/拖拉')
print('  → 李某某會被放出來，但過程不會快，會有後續麻煩')
print()

# ============================================================
# Section 6: 案例量化分析
# ============================================================
print('=' * 70)
print('Section 6: 李某某案例完整分析')
print('=' * 70)

def wx_rel(a, b):
    if a == b: return '比和'
    if WUXING_SHENG.get(a) == b: return f'{a}生{b}'
    if WUXING_KE.get(a) == b: return f'{a}剋{b}'
    if WUXING_SHENG.get(b) == a: return f'{b}生{a}(被生)'
    if WUXING_KE.get(b) == a: return f'{b}剋{a}(被剋)'
    return '?'

case = {
    'ren_tian': {'palace': 6, 'symbols': ['九天', '傷門', '天柱星', '空亡', '壬+癸']},
    'ren_di': {'palace': 7, 'symbols': ['值符', '生門', '天芮星', '丁+壬', '戊']},
    'yi': {'palace': 4, 'symbols': ['六合', '丙']},
    'geng': {'palace': 2, 'symbols': ['丁（地盤）', '寄宮']},
    'xin': {'palace': 3, 'symbols': ['白虎', '死門', '乙（地盤）']},
    'wu_yuegan': {'palace': 7, 'symbols': []},
    'shengmen_wu': {'palace': 7, 'symbols': []},
}

print('\n案例符號匯總：')
print(f'  壬(天盤/當事人): 乾六宮 → 九天/傷門/天柱星/空亡/壬+癸')
print(f'    → 尊貴名聲在外 + 因男女風化被拘留 + 可能在機場被捕')
print()
print(f'  壬(地盤/之前): 兌七宮 → 值符/生門/天芮星/丁+壬/戊')
print(f'    → 知名度高收入豐厚 + 犯了錯 + 肉慾關係牽涉金錢')
print()
print(f'  乙(女方陳某): 巽四宮 → 六合/丙')
print(f'    → 感情生活豐富，有其他男朋友')
print()
print(f'  庚(男方李某): 坤二宮 → 地盤丁/寄宮')
print(f'    → 有其他女朋友，寄宮=非正室')
print()
print(f'  辛(罪犯): 震三宮 → 白虎/死門/乙')
print(f'    → 確認被拘留 + 白虎=兇險 + 死門=困住')
print()

print('五行關鍵分析：')
print(f'  乙宮(巽4/木) vs 庚宮(坤2/土): 木剋土 → 乙剋庚')
print(f'    → 女方在某種程度上壓制/影響男方')
print()

print('月干(舉報者)分析：')
print(f'  月干戊 落兌七宮(金)')
print(f'  天干辛 落震三宮(木)')
print(f'  金(兌7) 剋 木(震3) → 月干剋辛')
print(f'    → 熟人通風報信給警察')
print()

print('財富/事業影響分析：')
print(f'  生門+戊(財富) 落兌七宮(金)')
print(f'  天干辛(李某某) 落震三宮(木)')
print(f'  金剋木 → 財富和事業衝剋李某某')
print(f'    → 以往天之驕子身份將不復存在')
print()

print('放出來的判斷：')
print(f'  1. 壬(辰) 落乾六(戌) → 辰戌相衝 → 逢衝必動 → 會被放出來')
print(f'  2. 辛 落震三宮，下臨乙奇 → 乙奇=慢/拖拉的希望 → 會放出但過程漫長')
print(f'  3. 結論：一定會放出來，但長時間影響生活和事業')
print()

# ============================================================
# Section 7: 寄宮在感情中的含義
# ============================================================
print('=' * 70)
print('Section 7: 寄宮在感情中的含義')
print('=' * 70)

print('\n寄宮 = 該符號不屬於這個宮位的本來配置')
print('  在感情場景中：寄宮 = 不是正室/不是正式關係')
print()
print('案例：')
print('  庚(李某某) 落坤二宮，地盤丁在此宮')
print('  丁不屬於坤二宮 → 寄宮')
print('  → 李某某和這段關係「不是正式的」→ 不是正室')
print()

# ============================================================
# Section 8: 與之前集數的對照
# ============================================================
print('=' * 70)
print('Section 8: 與之前集數的對照')
print('=' * 70)

print('1. 衝的概念擴展')
print('   EP12: 逢衝必動、逢衝必散')
print('   EP13 G61: 天干組合衝格（庚申+癸寅=衝格）')
print('   EP14: 天干vs宮位相衝（壬辰+乾六戌=逢衝必動）')
print('   → 衝有三種：天干組合衝格、天干宮位衝、宮位與宮位衝(EP05)')
print()

print('2. 用神多面性（EP06→EP14）')
print('   壬: 水/血液(EP13) → 嫌疑人(EP14)')
print('   辛: 金/肺部(EP13) → 罪犯(EP14)')
print('   月干: 平輩(EP04) → 舉報者(EP14)')
print('   值符: 吉神(EP01) → 名人(EP14)')
print('   九天: 科技(EP12) → 坐飛機(EP14)')
print()

print('3. 丁+壬 三種解讀（G47 再確認）')
print('   EP07: 合格=穩定（格局系統）')
print('   EP08: 產品種類多（下臨組合）')
print('   EP14: 淫蕩之合（道德負面合格）')
print('   → 場景決定解讀：格局系統 vs 下臨組合 vs 場景特殊含義')
print()

print('4. 四干社會關係驗證（EP04）')
print('   月干=平輩/朋友 → EP14: 月干戊衝剋辛 → 熟人舉報 ✅')
print('   EP04 建立的四干系統在 EP14 案例中完美驗證')
print()

print('5. 逢衝必動（EP12）在 EP14 驗證')
print('   壬(辰)落乾六(戌) → 逢衝必動 → 李某某會被放出來')
print('   辛+乙 = 衝格 → 逢衝必動 → 事情會有變化')
print('   → 兩次「逢衝必動」都指向「會放出來」')
print()

# ============================================================
# Section 9: EP14 新發現的不足
# ============================================================
print('=' * 70)
print('Section 9: EP14 新發現的不足')
print('=' * 70)

NEW_GAPS = [
    ('G69', '高', '起念原則未完整講解',
     '師傅說會在以後視頻詳細介紹，目前只有基本概念',
     '需等待後續集數，或自行研究'),
    ('G70', '高', '天干宮位相衝未納入引擎',
     '已發現第二種衝類型，但 engine 無檢測',
     '需實現 is_palace_chong() 並加入引擎'),
    ('G71', '中', '宮位地支數據不完整',
     'PALACE_DIZHI 目前是簡化版，可能不完全準確',
     '需確認每宮的完整地支歸屬'),
    ('G72', '中', '三奇希望特性只知乙奇',
     '丙奇、丁奇的希望特性師傅未講',
     '需等待後續集數'),
    ('G73', '低', '犯罪場景用神體系未系統化',
     '壬=嫌疑人、辛=罪犯，但完整體系未知',
     '需更多犯罪預測案例'),
]

for gid, priority, name, current, expected in NEW_GAPS:
    print(f'  [{priority}] {gid}: {name}')
    print(f'       現狀: {current}')
    print(f'       期望: {expected}')
    print()

# ============================================================
# Section 10: 結論
# ============================================================
print('=' * 70)
print('Section 10: 結論')
print('=' * 70)

print('EP14 的核心貢獻：')
print('  1. 起念原則（問事必須在起念的時間點起局）')
print('  2. 外應概念（環境突變觸發起念）')
print('  3. 天干與宮位地支相衝（第二種衝類型）')
print('  4. 丁+壬 = 淫蕩之合（合格道德負面）')
print('  5. 辛 = 犯罪用神、月干 = 舉報者')
print('  6. 乙奇希望特性（慢/婉轉/拖拉）')
print('  7. 寄宮在感情=非正室')
print('  8. 四干社會關係（EP04）在犯罪案例中驗證')
print()

print('對 backtest 的影響：')
print('  - 天干宮位相衝 = 新的動態指標（逢衝必動=變化即將發生）')
print('  - 可作為「即將變盤」的信號')
print('  - 起念原則 = 如果要做實際預測，必須記錄準確起念時間')
print()

# ============================================================
# Section 11: JSON 輸出
# ============================================================

ep14_data = {
    "episode": 14,
    "title": "李某某案例分析 + 起念/外應 + 天干與宮位相衝",
    "qinian_principle": QINIAN,
    "waiying_concept": WAIYING,
    "two_types_of_chong": {
        "天干組合衝": {
            "mechanism": "天盤干暗含地支 vs 地盤干暗含地支",
            "meaning": "衝格（格局）",
            "source": "EP13 G61",
        },
        "天干宮位衝": {
            "mechanism": "天盤干暗含地支 vs 落宮包含地支",
            "meaning": "逢衝必動（動態變化）",
            "source": "EP14",
        },
    },
    "palace_dizhi": PALACE_DIZHI,
    "all_palace_chong": [
        {"tiangan": a, "palace": p, "reason": r} for a, p, r in palace_chong_all
    ],
    "new_tiangan_zuhe": {
        f"{a}+{b}": v for (a, b), v in EP14_ZUHE.items()
    },
    "new_yongshen": NEW_YONGSHEN,
    "sanqi_hope": SANQI_HOPE,
    "case_analysis": {
        "conclusion": "李某某一定會被放出來，但長時間影響生活和事業",
        "key_evidence": [
            "壬(辰)落乾六(戌)=辰戌相衝→逢衝必動",
            "辛下臨乙奇=慢的希望→會放出但過程漫長",
            "月干戊衝剋辛=熟人舉報",
            "生門+戊衝剋辛=財富事業受衝擊",
        ],
    },
    "new_gaps": [
        {"id": g[0], "priority": g[1], "name": g[2], "current": g[3], "expected": g[4]}
        for g in [
            ('G69','高','起念原則未完整講解','只有基本概念','需等待或自行研究'),
            ('G70','高','天干宮位相衝未納入引擎','已發現第二種衝','需實現檢測'),
            ('G71','中','宮位地支數據不完整','簡化版','需確認'),
            ('G72','中','三奇希望特性只知乙奇','丙丁未講','需等待'),
            ('G73','低','犯罪場景用神未系統化','壬=嫌疑辛=罪犯','需更多案例'),
        ]
    ],
}

output_path = '/home/z/my-project/download/ep14_li_case.json'
with open(output_path, 'w') as f:
    json.dump(ep14_data, f, ensure_ascii=False, indent=2)
print(f'\n→ 已輸出 {output_path}')
print('\n' + '*' * 70)
print('  EP14 量化完成！')
print('*' * 70)
