#!/usr/bin/env python3
"""
EP10 量化腳本：買貨求財預測 + 地盤八卦完整信息
===================================================================

本集新知識點：
1. 貨物用神系統（時干=一般貨物，丁=電子，景門=字畫，庚=五金）
2. 真假判斷方法（用神宮符號組合分析）
3. 買到與否判斷（日干與貨物用神同宮=已/將在一起）
4. 賺錢與否判斷（生門宮 vs 日干宮/戊宮）
5. 時間預測（空亡=時辰未到，需要等待）
6. 應驗時間方法（農曆月份對應宮位）
7. 地盤八卦完整信息（人物/方位/時間/含義/狀態）
8. 天干顏色對應（癸=黑色/水，戊=黃色/土）
9. 新天干組合：癸+戊=合格（穩當實在）、戊+乙=合格
"""

import json

PALACE_WUXING = {1:'水', 2:'土', 3:'木', 4:'木', 5:'土', 6:'金', 7:'金', 8:'土', 9:'火'}
GONG_NAMES = {1:'坎', 2:'坤', 3:'震', 4:'巽', 5:'中', 6:'乾', 7:'兌', 8:'艮', 9:'離'}
WUXING_SHENG = {"金": "水", "水": "木", "木": "火", "火": "土", "土": "金"}
WUXING_KE   = {"金": "木", "木": "土", "土": "水", "水": "火", "火": "金"}

# ============================================================
# Section 1: 貨物用神系統
# ============================================================
print('=' * 70)
print('Section 1: 貨物用神系統')
print('=' * 70)

GOODS_YONGSHEN = {
    '時干': {
        'scope': '所有類型貨物（通用）',
        'note': '最常用的貨物用神',
    },
    '丁': {
        'scope': '電器電子產品',
        'note': '丁=火=電子/電器',
    },
    '景門': {
        'scope': '藝術品、字畫',
        'note': '景門=美麗=藝術品',
    },
    '庚': {
        'scope': '五金製品',
        'note': '庚=金=五金',
    },
}

print('\n貨物用神對照表：')
for k, v in GOODS_YONGSHEN.items():
    print(f'  {k} → {v["scope"]}')
    print(f'       備註: {v["note"]}')

print('\n⚠️ 師傅說更多貨物用神會在後續視頻陸續介紹')
print()

# ============================================================
# Section 2: 真假判斷方法
# ============================================================
print('=' * 70)
print('Section 2: 貨物真假判斷方法')
print('=' * 70)

print('\n判斷邏輯：分析貨物用神宮的所有符號')
print('  如果所有符號都指向「真品/好貨」→ 真品')
print('  如果出現「假/凶」符號（如玄武、驚門等）→ 可能是假貨')
print()

print('案例：字畫用神=景門，落巽四宮')
case_genuine = {
    '景門': '用神本身',
    '值符': '高貴、高級、名貴 → 真品信號',
    '天英星': '亮麗 → 真品信號',
    '癸+戊': '合格 → 穩當實在 → 真品信號',
}
for sym, meaning in case_genuine.items():
    print(f'  {sym}: {meaning}')
print('  結論：所有符號都顯示真品 ✅')
print()

# 時干交叉驗證
print('時干交叉驗證（時干也代表貨物）：')
case_shigan = {
    '九天': '高高在上、龍在九天 → 高價值',
    '杜門': '技術鑑定、檢測 → 經得起檢測',
    '天輔星': '吉星，對文化藝術最有利 → 真品',
    '戊+乙': '合格 → 穩當實在 → 真品',
}
for sym, meaning in case_shigan.items():
    print(f'  {sym}: {meaning}')
print('  結論：時干宮也確認真品 ✅')
print()

# ============================================================
# Section 3: 買到與否判斷
# ============================================================
print('=' * 70)
print('Section 3: 買到與否判斷')
print('=' * 70)

print('\n判斷方法：日干宮 vs 貨物用神宮')
print('  同宮 → 求測人和貨物已經或將會在一起 → 一定能買到')
print('  比和 → 關係密切，同進退 → 大概率買到')
print('  日干剋貨物 → 可以掌控 → 能買到')
print('  貨物剋日干 → 貨物不利於求測人 → 買不到或買了吃虧')
print()

print('案例：日干癸落巽四宮 = 景門落宮 → 同宮！')
print('  同宮 = 求測人和畫已經或將會在一起')
print('  日干臨值符值使 → 非常喜歡，一定會買')
print('  時干宮(木) vs 日干宮(木) = 比和 → 關係密切')
print('  結論：一定能買到 ✅（事實：已以380萬成交）')
print()

# ============================================================
# Section 4: 賺錢與否判斷（EP08框架驗證）
# ============================================================
print('=' * 70)
print('Section 4: 賺錢與否判斷 — EP08投資框架驗證')
print('=' * 70)

print('\nEP08 確立的投資分析框架在本集再次驗證：')
print('  生門宮 vs 日干宮 → 利潤對求測人的影響')
print('  生門宮 vs 戊宮 → 利潤 vs 成本')
print()

print('案例：')
print('  生門落坎一宮（水），臨玄武、天任星')
print('  日干宮=巽四宮（木），戊宮=震三宮（木）')
print()

# 計算
def wx_rel(a, b):
    if a == b: return '比和'
    if WUXING_SHENG.get(a) == b: return '生'
    if WUXING_KE.get(a) == b: return '剋'
    if WUXING_SHENG.get(b) == a: return '被生'
    if WUXING_KE.get(b) == a: return '被剋'
    return '?'

shengmen_wx = PALACE_WUXING[1]  # 坎一=水
rigan_wx = PALACE_WUXING[4]     # 巽四=木
wu_wx = PALACE_WUXING[3]         # 震三=木

r1 = wx_rel(shengmen_wx, rigan_wx)
r2 = wx_rel(shengmen_wx, wu_wx)
print(f'  生門({shengmen_wx}) vs 日干({rigan_wx}): {r1} → 利潤有利於求測人 ✅')
print(f'  生門({shengmen_wx}) vs 戊({wu_wx}): {r2} → 利潤有利於成本回收 ✅')
print()
print('  但生門臨玄武 → 這是一種投機行為')
print('  但生門臨空亡 → 時辰未到，需要等待')
print('  結論：會賺錢（約300萬），但不是馬上 ✅')
print()

# ============================================================
# Section 5: 時間預測
# ============================================================
print('=' * 70)
print('Section 5: 時間預測 — 空亡與應驗時間')
print('=' * 70)

print('\n空亡與時間的關係：')
print('  生門臨空亡 → 時辰未到 → 需要經歷一些時間')
print('  不能馬上轉手賺到錢')
print()

print('應驗時間判斷：')
print('  師傅預測：大概需要3-4個月，農曆五月可以賣出')
print('  ⚠️ 師傅未講解應驗時間的計算方法！')
print('  僅知道結果，不知道推導過程')
print()

# 地盤八卦與月份對應（本集後半段）
BAGUA_MONTH = {
    '乾': '農曆九月至十月',
    '坤': '農曆六月至七月',
    '震': '農曆二月',
    '巽': '農曆三月至四月',
    '坎': '農曆十一月',
    '離': '農曆五月',
    '艮': '農曆十二月至正月',
    '兌': '農曆八月',
}

print('地盤八卦與農曆月份對應：')
for gua, months in BAGUA_MONTH.items():
    print(f'  {gua}卦 → {months}')
print()

print('案例推測：師傅說農曆五月 → 離卦 → 離九宮')
print('  可能的邏輯：生門落坎一宮，坎的對宮是離九（水火相衝=變動）')
print('  或者：與某個用神落宮的應期有關')
print('  → 計算方法待後續集數補充')
print()

# ============================================================
# Section 6: 天干顏色對應
# ============================================================
print('=' * 70)
print('Section 6: 天干顏色對應')
print('=' * 70)

TIANGAN_COLOR = {
    '甲': {'wuxing': '木', 'color': '青綠色'},
    '乙': {'wuxing': '木', 'color': '青綠色'},
    '丙': {'wuxing': '火', 'color': '紅色'},
    '丁': {'wuxing': '火', 'color': '紅色'},
    '戊': {'wuxing': '土', 'color': '黃色'},
    '己': {'wuxing': '土', 'color': '黃色'},
    '庚': {'wuxing': '金', 'color': '白色'},
    '辛': {'wuxing': '金', 'color': '白色'},
    '壬': {'wuxing': '水', 'color': '黑色'},
    '癸': {'wuxing': '水', 'color': '黑色'},
}

print('\n天干五行對應顏色：')
print(f'  {"天干":<4} {"五行":<4} {"顏色":<8}')
print('  ' + '-' * 20)
for tg, info in TIANGAN_COLOR.items():
    print(f'  {tg:<6} {info["wuxing"]:<4} {info["color"]:<8}')

print('\n案例應用：')
print('  癸=黑色(水) + 戊=黃色(土) → 水墨畫')
print('  師傅通過天干顏色判斷畫的類型')
print()

# ============================================================
# Section 7: 新天干組合
# ============================================================
print('=' * 70)
print('Section 7: EP10 新天干組合')
print('=' * 70)

EP10_ZUHE = {
    ('癸', '戊'): {'meaning': '合格', 'detail': '穩當、實在', 'source': 'EP10案例（景門宮）'},
    ('戊', '癸'): {'meaning': '合格', 'detail': '穩當、實在', 'source': 'EP10案例'},
    ('戊', '乙'): {'meaning': '合格', 'detail': '穩當、實在', 'source': 'EP10案例（時干宮）'},
    ('乙', '戊'): {'meaning': '合格', 'detail': '穩當、實在', 'source': 'EP10案例'},
}

print('EP10 案例中的天干組合：')
for (a, b), info in EP10_ZUHE.items():
    if a < b:
        print(f'  {a}+{b}: {info["meaning"]}（{info["detail"]}）')

print()
print('與 EP07 格局庫對照：')
print('  EP07: 丁+戊=合格、壬+丁=合格')
print('  EP10: 癸+戊=合格、戊+乙=合格')
print('  → 合格的組合越來越多，但「合格」的定義似乎較寬鬆')
print()

# 與 EP08/EP09 矛盾對照
print('天干組合解讀系統矛盾更新：')
contradictions = [
    ('丁+壬', 'EP07=合格(穩定)', 'EP08=產品種類多'),
    ('乙+壬', 'EP08=變動', 'EP09=管理不好/監守自盜'),
]
for zuhe, v1, v2 in contradictions:
    print(f'  {zuhe}: {v1} vs {v2}')
print('  → 矛盾僅出現在下臨組合解讀，格局（合格/衝格）暫未見矛盾')
print()

# ============================================================
# Section 8: 杜門新含義
# ============================================================
print('=' * 70)
print('Section 8: 杜門含義擴展')
print('=' * 70)

DUMEN_EVOLUTION = {
    'EP03': '封閉、隱藏心思',
    'EP04': '高科技行業',
    'EP08': '資金來路受阻、不通',
    'EP10': '技術鑑定、檢測（經得起檢測）',
}

print('\n杜門含義演變：')
for ep, meaning in DUMEN_EVOLUTION.items():
    print(f'  {ep}: {meaning}')
print()
print('核心不變：杜門=堵塞、不通')
print('  正向解讀：堵塞=經得起檢測（假的被擋住）')
print('  負向解讀：堵塞=受阻、不通')
print()

# ============================================================
# Section 9: 地盤八卦完整信息
# ============================================================
print('=' * 70)
print('Section 9: 地盤八卦完整信息')
print('=' * 70)

DIPAN_BAGUA = {
    '乾卦': {
        'palace': 6, 'wuxing': '金', 'direction': '西北',
        'nature': '天', 'family': '父、長輩領導',
        'meaning': '最重要的人或最貴重的事物',
        'month': '農曆九月十月',
        'state': '高貴、重要、領導',
    },
    '坤卦': {
        'palace': 2, 'wuxing': '土', 'direction': '西南',
        'nature': '地', 'family': '母',
        'meaning': '社會大眾',
        'month': '農曆六月七月',
        'state': '包容、承載、大眾',
    },
    '震卦': {
        'palace': 3, 'wuxing': '木', 'direction': '正東',
        'nature': '雷', 'family': '長子',
        'meaning': '震動、突然暴起',
        'month': '農曆二月',
        'state': '震動、突然變化、暴起',
    },
    '巽卦': {
        'palace': 4, 'wuxing': '木', 'direction': '東南',
        'nature': '風', 'family': '長女',
        'meaning': '自由活動、搖擺不定',
        'month': '農曆三月四月',
        'state': '自由、搖擺、靈活',
    },
    '坎卦': {
        'palace': 1, 'wuxing': '水', 'direction': '正北',
        'nature': '水', 'family': '中男（二兒子）',
        'meaning': '艱難、險阻',
        'month': '農曆十一月',
        'state': '艱難、險阻、困境',
    },
    '離卦': {
        'palace': 9, 'wuxing': '火', 'direction': '正南',
        'nature': '火', 'family': '中女（二女兒）',
        'meaning': '光明、美麗',
        'month': '農曆五月',
        'state': '光明、美麗、顯露',
    },
    '艮卦': {
        'palace': 8, 'wuxing': '土', 'direction': '東北',
        'nature': '山', 'family': '少男（小兒子）',
        'meaning': '靜止、安定',
        'month': '農曆十二月正月',
        'state': '靜止、不動、等待',
    },
    '兌卦': {
        'palace': 7, 'wuxing': '金', 'direction': '正西',
        'nature': '澤', 'family': '少女（小女兒）',
        'meaning': '缺憾、不完整、言辭口舌',
        'month': '農曆八月',
        'state': '缺憾、口舌、不完整',
    },
}

print(f'\n{"卦":<6} {"宮":<4} {"五行":<4} {"方位":<6} {"象":<6} {"家庭":<10} {"含義":<20} {"月份":<16}')
print('-' * 80)
for name, info in DIPAN_BAGUA.items():
    print(f'{name:<6} {info["palace"]:<4} {info["wuxing"]:<4} {info["direction"]:<6} {info["nature"]:<6} {info["family"]:<10} {info["meaning"]:<20} {info["month"]:<16}')

print()
print('地盤的兩大功能：')
print('  1. 代表地理位置和時間')
print('  2. 包含萬事萬物的信息（八卦代表萬物）')
print()

print('地盤狀態判斷：')
print('  日干落某宮 → 該宮八卦的狀態 = 求測人目前的狀態')
print('  例：日干落艮八宮 → 艮=靜止 → 求測人處於靜止不動狀態')
print()

print('地盤人物定位用神：')
print('  預測父親 → 年干 + 乾六宮')
print('  → 地盤宮位可以作為輔助用神')
print()

# ============================================================
# Section 10: 買貨求財完整分析框架
# ============================================================
print('=' * 70)
print('Section 10: 買貨求財完整分析框架')
print('=' * 70)

BUYING_FRAMEWORK = {
    'step1_find_yongshen': {
        'action': '確定貨物用神',
        'rule': '一般貨物=時干，特殊貨物有專門用神（丁=電子/景門=字畫/庚=五金）',
    },
    'step2_authenticity': {
        'action': '判斷真假',
        'rule': '分析貨物用神宮的所有符號（門/星/神/天干組合）',
        'positive': ['值符', '吉星', '合格', '天輔(文化)'],
        'negative': ['玄武', '驚門', '天芮'],
    },
    'step3_can_buy': {
        'action': '判斷能否買到',
        'rule': '日干宮 vs 貨物用神宮（同宮=一定買到，比和=大概率）',
    },
    'step4_profit': {
        'action': '判斷能否賺錢',
        'rule': '生門宮 vs 日干宮/戊宮（生=有利，剋=不利）',
    },
    'step5_timing': {
        'action': '判斷何時可賣出',
        'rule': '空亡=時辰未到需等待，應驗時間待補充',
    },
}

print('\n買貨求財五步分析框架：')
for step, info in BUYING_FRAMEWORK.items():
    print(f'  {info["action"]}')
    print(f'    方法: {info["rule"]}')
print()

# ============================================================
# Section 11: 與之前集數的對照
# ============================================================
print('=' * 70)
print('Section 11: 與之前集數的對照')
print('=' * 70)

print('1. 投資框架（EP08）→ EP10 驗證')
print('   EP08: 生門=利潤、戊=資金、三組關係')
print('   EP10: 生門宮生日干宮+戊宮=有利润 ✅ 完美驗證')
print()
print('2. 四維模型（EP03）→ EP10 確認地盤功能')
print('   EP03: 地盤=地利 → EP10: 地盤=地理位置+時間+萬物信息')
print('   ✅ 地盤功能大幅擴展')
print()
print('3. 同宮判斷（EP09）→ EP10 再次確認')
print('   EP09: 日干與選項同宮=已開始運作')
print('   EP10: 日干與貨物用神同宮=已經或將會在一起')
print('   ✅ 同宮=「已經或將會在一起」一致')
print()
print('4. 空亡（EP05/EP08/EP09）→ EP10 新含義')
print('   EP05=停滯 → EP08=無法落實 → EP09=瓶頸 → EP10=時辰未到需等待')
print('   → 空亡的核心含義：尚未發生/需要等待')
print()
print('5. 杜門（EP03→EP10）→ 含義持續擴展')
print('   正向：技術鑑定/檢測（EP10新）')
print('   負向：資金受阻（EP08）')
print()

# ============================================================
# Section 12: EP10 新發現的不足
# ============================================================
print('=' * 70)
print('Section 12: EP10 新發現的不足')
print('=' * 70)

NEW_GAPS = [
    ('G52', '高', '應驗時間計算未實現',
     '師傅能預測3-4個月後農曆五月可賣出，但未講計算方法',
     '需找到應驗時間的推導規則'),
    ('G53', '中', '貨物用神庫不完整',
     '僅有時干/丁/景門/庚四種',
     '待後續集數補充更多貨物類型'),
    ('G54', '中', '天干顏色系統未驗證',
     '案例中用癸=黑+戊=黃判斷水墨畫，但未系統講解',
     '需確認五行對應顏色的完整規則'),
    ('G55', '低', '地盤狀態判斷未系統化',
     '日干落宮八卦=求測人狀態，概念清楚但未編碼',
     '可建立 DIPAN_STATE 評分'),
    ('G56', '低', '地盤人物用神未系統化',
     '父親=乾六宮，但完整的人物-宮位映射未建立',
     '可建立 FAMILY_PALACE 映射'),
]

for gid, priority, name, current, expected in NEW_GAPS:
    print(f'  [{priority}] {gid}: {name}')
    print(f'       現狀: {current}')
    print(f'       期望: {expected}')
    print()

# ============================================================
# Section 13: 結論
# ============================================================
print('=' * 70)
print('Section 13: 結論')
print('=' * 70)

print('EP10 的核心貢獻：')
print('  1. 貨物用神系統（時干/丁/景門/庚）')
print('  2. 真假判斷方法（用神宮全符號分析）')
print('  3. 買到與否判斷（日干與貨物同宮=一定能買到）')
print('  4. EP08 投資框架驗證（生門 vs 日干/戊）')
print('  5. 時間預測概念（空亡=時辰未到）')
print('  6. 天干顏色對應')
print('  7. 地盤八卦完整信息（人物/方位/時間/狀態）')
print('  8. 杜門正向解讀（技術鑑定/檢測）')
print()
print('對 back test 的影響：')
print('  - 買貨求財框架 = 交易決策的完整模型')
print('  - 真假判斷 = 質量/風險評估維度')
print('  - 同宮判斷 = 持有狀態判斷')
print('  - 應驗時間 = 如果能破解，可預測最佳賣出時機')
print()

# ============================================================
# Section 14: JSON 輸出
# ============================================================

ep10_data = {
    "episode": 10,
    "title": "買貨求財預測 + 地盤八卦完整信息",
    "goods_yongshen": GOODS_YONGSHEN,
    "buying_framework": BUYING_FRAMEWORK,
    "dipan_bagua": DIPAN_BAGUA,
    "tiangan_color": TIANGAN_COLOR,
    "new_tiangan_zuhe": {f"{a}+{b}": v for (a,b), v in EP10_ZUHE.items()},
    "dumen_evolution": DUMEN_EVOLUTION,
    "new_gaps": [
        {"id": g[0], "priority": g[1], "name": g[2], "current": g[3], "expected": g[4]}
        for g in [
            ('G52','高','應驗時間計算未實現','師傅能預測時間但未講方法','需找到應驗時間推導規則'),
            ('G53','中','貨物用神庫不完整','僅有四種','待後續集數補充'),
            ('G54','中','天干顏色系統未驗證','案例中出現但未系統講解','需確認五行對應顏色規則'),
            ('G55','低','地盤狀態判斷未系統化','概念清楚但未編碼','可建立DIPAN_STATE評分'),
            ('G56','低','地盤人物用神未系統化','僅有父親=乾六宮','可建立FAMILY_PALACE映射'),
        ]
    ],
}

output_path = '/home/z/my-project/download/ep10_buying_goods.json'
with open(output_path, 'w') as f:
    json.dump(ep10_data, f, ensure_ascii=False, indent=2)
print(f'\n→ 已輸出 {output_path}')
print('\n' + '*' * 70)
print('  EP10 量化完成！')
print('*' * 70)
