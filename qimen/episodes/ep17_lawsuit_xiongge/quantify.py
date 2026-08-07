#!/usr/bin/env python3
"""
EP17 量化腳本：官司訴訟預測 + 常用凶格
===================================================================

本集新知識點：
1. 官司訴訟六用神體系
2. 官司輸贏判斷方法（值符 vs 天乙 + 日干 vs 時干）
3. 開門宮取向（法院傾向哪一方）
4. 反吟局 + 官司 = 不會一次審完，輸了會上訴
5. 商業糾紛案例實戰分析
6. 飛干格（日干+庚）
7. 伏干格（庚+日干）
8. 刑格（庚+己）
9. 六儀擊刑（僅6個固定組合）
10. 五不遇時（10個同五行相剋組合）
11. 門迫（12個具體門宮組合）
"""

import json

GONG_NAMES = {1:'坎', 2:'坤', 3:'震', 4:'巽', 5:'中', 6:'乾', 7:'兌', 8:'艮', 9:'離'}
PALACE_WUXING = {1:'水', 2:'土', 3:'木', 4:'木', 5:'土', 6:'金', 7:'金', 8:'土', 9:'火'}
WUXING_KE = {
    '金':['木'], '木':['土'], '水':['火'], '火':['金'], '土':['水'],
}
WUXING_SHENG = {
    '金':['水'], '水':['木'], '木':['火'], '火':['土'], '土':['金'],
}
TIANGAN_WUXING = {'甲':'木','乙':'木','丙':'火','丁':'火','戊':'土','己':'土','庚':'金','辛':'金','壬':'水','癸':'水'}
TIANGAN = ['甲','乙','丙','丁','戊','己','庚','辛','壬','癸']
BAMEN = ['休門','生門','傷門','杜門','景門','死門','驚門','開門']

# ============================================================
# Section 1: 官司訴訟六用神
# ============================================================
print('=' * 70)
print('Section 1: 官司訴訟六用神')
print('=' * 70)

LAWSUIT_YONGSHEN = {
    '值符': {
        'represents': '原告',
        'detail': '值符所在宮位代表原告一方',
        'engine_note': '值符位置可從 qiju() 返回結果取得',
    },
    '天乙': {
        'represents': '被告',
        'detail': '值符落宮原地盤天干的天乙太乙 → 即值符落宮地盤天干本身',
        'engine_note': '需取值符落宮的地盤天干，該天干即為天乙太乙所在',
    },
    '開門': {
        'represents': '法院/法官',
        'detail': '開門所在宮位代表法院或法官的態度',
        'engine_note': '開門為八門之一，可從門盤取得',
    },
    '六合': {
        'represents': '證人/證據',
        'detail': '六合所在宮位代表證人和證據的情況',
        'engine_note': '六合為八神之一（或九星之一，視體系），可從神盤取得',
    },
    '景門': {
        'represents': '入稟狀/訴狀',
        'detail': '景門所在宮位代表入稟狀的質量',
        'engine_note': '景門為八門之一，可從門盤取得',
    },
    '驚門': {
        'represents': '律師',
        'detail': '驚門所在宮位代表律師的能力和表現',
        'engine_note': '驚門為八門之一，可從門盤取得',
    },
}

for name, info in LAWSUIT_YONGSHEN.items():
    print(f'\n  {name} → {info["represents"]}')
    print(f'    詳情: {info["detail"]}')
print()

# ============================================================
# Section 2: 官司輸贏判斷方法
# ============================================================
print('=' * 70)
print('Section 2: 官司輸贏判斷方法')
print('=' * 70)

JUDGMENT_METHOD = {
    'step1_值符vs天乙': {
        'method': '比較值符宮與天乙宮的生剋關係',
        'win': '值符宮剋天乙宮 → 原告贏',
        'lose': '天乙宮剋值符宮 → 被告贏（原告輸）',
        'equal': '比宮旺衰，旺者贏',
    },
    'step2_日干vs時干': {
        'method': '交叉驗證：日干=求測人，時干=所問之事',
        'consistency': '日干宮剋時干宮 → 與步驟1互相印證',
        'note': '兩步結果一致 → 判斷更可靠',
    },
    'step3_開門取向': {
        'method': '看開門（法院）生哪一方',
        'rule': '開門宮生值符宮 → 法院傾向原告',
        'rule2': '開門宮生天乙宮 → 法院傾向被告',
        'neutral': '開門宮不生任何一方 → 法院中立',
    },
}

for step, info in JUDGMENT_METHOD.items():
    print(f'\n  {step}:')
    print(f'    方法: {info["method"]}')
    for k, v in list(info.items())[1:]:
        print(f'    {k}: {v}')
print()

# ============================================================
# Section 3: 反吟局 + 官司
# ============================================================
print('=' * 70)
print('Section 3: 反吟局 + 官司')
print('=' * 70)

FANYIN_LAWSUIT = {
    'condition': '反吟局（天盤與地盤完全相反）',
    'meaning': '不會審一次就結束',
    'detail': [
        '一審結束後，輸的一方一定會上訴',
        '事情會反反覆覆',
        '不會那麼快有最終結果',
    ],
    'engine_note': '反吟局檢測已在 EP12 量化，engine 可直接使用',
}

print(f'  條件: {FANYIN_LAWSUIT["condition"]}')
print(f'  含義: {FANYIN_LAWSUIT["meaning"]}')
for d in FANYIN_LAWSUIT['detail']:
    print(f'  - {d}')
print()

# ============================================================
# Section 4: 商業糾紛案例用神分析
# ============================================================
print('=' * 70)
print('Section 4: 商業糾紛案例用神分析')
print('=' * 70)

CASE_STUDY = {
    'background': '商業糾紛官司',
    'judgment': '原告輸',
    'analysis': {
        '值符宮': {
            'wuxing': '金',
            'situation': '被天乙宮（火）剋 → 原告不利',
        },
        '天乙宮': {
            'wuxing': '火',
            'situation': '火剋金 → 被告佔優',
        },
        '六合宮': {
            'represents': '證人證據',
            'situation': '不利於原告',
        },
        '驚門宮': {
            'represents': '律師',
            'situation': '律師能力差（對原告不利）',
        },
        '開門宮': {
            'represents': '法院',
            'situation': '法院傾向被告',
        },
    },
    'fanyin': '本案為反吟局 → 輸了會上訴，不會一次結束',
    'cross_validation': '日干vs時干也顯示不利 → 多重印證',
}

print(f'  背景: {CASE_STUDY["background"]}')
print(f'  結果: {CASE_STUDY["judgment"]}')
print(f'  反吟: {CASE_STUDY["fanyin"]}')
print(f'  交叉驗證: {CASE_STUDY["cross_validation"]}')
print()
for name, info in CASE_STUDY['analysis'].items():
    print(f'  {name}:')
    for k, v in info.items():
        print(f'    {k}: {v}')
print()

# ============================================================
# Section 5: 飛干格
# ============================================================
print('=' * 70)
print('Section 5: 飛干格')
print('=' * 70)

FEIGAN_GE = {
    'name': '飛干格',
    'type': '凶格',
    'condition': '日干 + 庚（天盤日干落在地盤庚之上）',
    'condition_alt': '天盤某天干為日干，地盤同宮天干為庚',
    'meaning': '遭遇不測、身陷困境',
    'detail': [
        '庚為阻礙、阻力、變故',
        '日干代表求測人自己',
        '自己踩在庚上面 = 被阻礙壓住',
    ],
    'engine_note': '遍歷9宮，檢查天盤天干==日干 且 地盤天干==庚',
}

print(f'  {FEIGAN_GE["name"]}（{FEIGAN_GE["type"]}）')
print(f'  條件: {FEIGAN_GE["condition"]}')
print(f'  含義: {FEIGAN_GE["meaning"]}')
for d in FEIGAN_GE['detail']:
    print(f'  - {d}')
print()

# 飛干格所有可能組合
print('  飛干格所有可能組合（10個日干 × 1個庚 = 10個）：')
for tg in TIANGAN:
    print(f'    天盤{tg} + 地盤庚 → 飛干格')
print()

# ============================================================
# Section 6: 伏干格
# ============================================================
print('=' * 70)
print('Section 6: 伏干格')
print('=' * 70)

FUGAN_GE = {
    'name': '伏干格',
    'type': '凶格',
    'condition': '庚 + 日干（天盤庚落在地盤日干之上）',
    'condition_alt': '天盤天干為庚，地盤同宮天干為日干',
    'meaning': '遭遇不測、身陷困境 + 失去行動自由',
    'difference_from_feigan': '伏干比飛干更嚴重，多了「失去行動自由」',
    'detail': [
        '庚為阻礙壓在求測人頭上',
        '比飛干格更直接、更壓迫',
        '可能意味着被限制、被拘留等',
    ],
    'engine_note': '遍歷9宮，檢查天盤天干==庚 且 地盤天干==日干',
}

print(f'  {FUGAN_GE["name"]}（{FUGAN_GE["type"]}）')
print(f'  條件: {FUGAN_GE["condition"]}')
print(f'  含義: {FUGAN_GE["meaning"]}')
print(f'  與飛干格區別: {FUGAN_GE["difference_from_feigan"]}')
for d in FUGAN_GE['detail']:
    print(f'  - {d}')
print()

print('  伏干格所有可能組合（10個）：')
for tg in TIANGAN:
    print(f'    天盤庚 + 地盤{tg} → 伏干格')
print()

# ============================================================
# Section 7: 刑格
# ============================================================
print('=' * 70)
print('Section 7: 刑格')
print('=' * 70)

XING_GE = {
    'name': '刑格',
    'type': '凶格',
    'condition': '庚 + 己（天盤庚落在地盤己之上）',
    'meaning': '阻滯困難、官司破財患病',
    'detail': [
        '庚為阻礙，己為宅基地、財庫',
        '庚壓在己上面 = 財庫被破、家宅不安',
        '特別容易引起官司、破財、患病',
    ],
    'engine_note': '檢查天盤庚落在地盤己的宮位',
}

print(f'  {XING_GE["name"]}（{XING_GE["type"]}）')
print(f'  條件: {XING_GE["condition"]}')
print(f'  含義: {XING_GE["meaning"]}')
for d in XING_GE['detail']:
    print(f'  - {d}')
print()

# ============================================================
# Section 8: 六儀擊刑
# ============================================================
print('=' * 70)
print('Section 8: 六儀擊刑')
print('=' * 70)

LIUYI_XINGXING = [
    {'tiangan': '壬', 'palace': 4, 'palace_name': '巽四宮', 'note': '壬落巽宮'},
    {'tiangan': '癸', 'palace': 4, 'palace_name': '巽四宮', 'note': '癸落巽宮'},
    {'tiangan': '辛', 'palace': 9, 'palace_name': '離九宮', 'note': '辛落離宮'},
    {'tiangan': '己', 'palace': 2, 'palace_name': '坤二宮', 'note': '己落坤宮'},
    {'tiangan': '戊', 'palace': 3, 'palace_name': '震三宮', 'note': '戊落震宮'},
    {'tiangan': '庚', 'palace': 8, 'palace_name': '艮八宮', 'note': '庚落艮宮'},
]

print(f'  六儀擊刑（僅此6個固定組合，不可擴展）：')
print(f'  {"天干":<4} {"宮位":<10} {"五行":<4} {"備註"}')
print('  ' + '-' * 40)
for item in LIUYI_XINGXING:
    tg_wx = TIANGAN_WUXING[item['tiangan']]
    p_wx = PALACE_WUXING[item['palace']]
    note = ''
    # 巽宮屬木，壬癸屬水 → 水生木，非刑
    # 但六儀擊刑是固定組合，不按五行生剋解釋
    print(f'  {item["tiangan"]:<4} {item["palace_name"]:<10} {tg_wx}→{p_wx}  {item["note"]}')
print()

print('  ⚠️ 關鍵：六儀擊刑只有這6個，是固定組合，不是按五行推算的')
print('  用途：檢測盤局中是否存在這些組合 → 存在則為凶')
print()

# 驗證：為何這6個是六儀擊刑
print('  六儀擊刑的傳統解釋（天干落入受刑之宮）：')
XINGXING_EXPLAIN = [
    ('壬', '巽4', '壬水入辰/巳，辰為水之墓庫'),
    ('癸', '巽4', '癸水入辰/巳，辰為水之墓庫'),
    ('辛', '離9', '辛金入午，午火剋金，受刑'),
    ('己', '坤2', '己土入未/坤，受刑之位'),
    ('戊', '震3', '戊土入卯，木剋土，受刑'),
    ('庚', '艮8', '庚金入寅/艮，受刑之位'),
]
for tg, palace, explain in XINGXING_EXPLAIN:
    print(f'    {tg}落{palace}: {explain}')
print()

# ============================================================
# Section 9: 五不遇時
# ============================================================
print('=' * 70)
print('Section 9: 五不遇時')
print('=' * 70)

WUBUYUSHI = [
    {'day_gan': '甲', 'hour_gan': '庚', 'relation': '木剋土（甲木→庚金，金剋木）', 'actual': '庚金剋甲木'},
    {'day_gan': '乙', 'hour_gan': '辛', 'relation': '乙木→辛金，金剋木', 'actual': '辛金剋乙木'},
    {'day_gan': '丙', 'hour_gan': '壬', 'relation': '丙火→壬水，水剋火', 'actual': '壬水剋丙火'},
    {'day_gan': '丁', 'hour_gan': '癸', 'relation': '丁火→癸水，水剋火', 'actual': '癸水剋丁火'},
    {'day_gan': '戊', 'hour_gan': '甲', 'relation': '戊土→甲木，木剋土', 'actual': '甲木剋戊土'},
    {'day_gan': '己', 'hour_gan': '乙', 'relation': '己土→乙木，木剋土', 'actual': '乙木剋己土'},
    {'day_gan': '庚', 'hour_gan': '丙', 'relation': '庚金→丙火，火剋金', 'actual': '丙火剋庚金'},
    {'day_gan': '辛', 'hour_gan': '丁', 'relation': '辛金→丁火，火剋金', 'actual': '丁火剋辛金'},
    {'day_gan': '壬', 'hour_gan': '戊', 'relation': '壬水→戊土，土剋水', 'actual': '戊土剋壬水'},
    {'day_gan': '癸', 'hour_gan': '己', 'relation': '癸水→己土，土剋水', 'actual': '己土剋癸水'},
]

print('  五不遇時（10個組合，時干剋日干 = 不利）：')
print(f'  {"日干":<4} {"時干":<4} {"時干五行":<6} {"日干五行":<6} {"剋制關係"}')
print('  ' + '-' * 50)
for item in WUBUYUSHI:
    h_wx = TIANGAN_WUXING[item['hour_gan']]
    d_wx = TIANGAN_WUXING[item['day_gan']]
    print(f'  {item["day_gan"]:<4} {item["hour_gan"]:<4} {h_wx:<6} {d_wx:<6} {item["actual"]}')
print()

# 驗證：所有組合確實是時干剋日干
print('  驗證：所有10個組合是否滿足「時干五行剋日干五行」')
all_valid = True
for item in WUBUYUSHI:
    h_wx = TIANGAN_WUXING[item['hour_gan']]
    d_wx = TIANGAN_WUXING[item['day_gan']]
    valid = d_wx in WUXING_KE.get(h_wx, [])
    if not valid:
        all_valid = False
        print(f'    ❌ {item["day_gan"]}日{item["hour_gan"]}時: {h_wx}不剋{d_wx}')
if all_valid:
    print('    ✅ 全部10個組合驗證通過')
print()

print('  規律總結：')
print('    甲乙（木）日 → 庚辛（金）時 → 金剋木')
print('    丙丁（火）日 → 壬癸（水）時 → 水剋火')
print('    戊己（土）日 → 甲乙（木）時 → 木剋土')
print('    庚辛（金）日 → 丙丁（火）時 → 火剋金')
print('    壬癸（水）日 → 戊己（土）時 → 土剋水')
print('    → 同五行對的兩個天干，被其「相剋」五行對的時干剋')
print()

# ============================================================
# Section 10: 門迫
# ============================================================
print('=' * 70)
print('Section 10: 門迫')
print('=' * 70)

MENPO = [
    {'men': '休門', 'palace': 9, 'palace_name': '離九宮', 'men_wx': '水', 'palace_wx': '火',
     'relation': '水剋火（門剋宮）'},
    {'men': '開門', 'palace': 3, 'palace_name': '震三宮', 'men_wx': '金', 'palace_wx': '木',
     'relation': '金剋木（門剋宮）'},
    {'men': '開門', 'palace': 4, 'palace_name': '巽四宮', 'men_wx': '金', 'palace_wx': '木',
     'relation': '金剋木（門剋宮）'},
    {'men': '驚門', 'palace': 3, 'palace_name': '震三宮', 'men_wx': '金', 'palace_wx': '木',
     'relation': '金剋木（門剋宮）'},
    {'men': '驚門', 'palace': 4, 'palace_name': '巽四宮', 'men_wx': '金', 'palace_wx': '木',
     'relation': '金剋木（門剋宮）'},
    {'men': '生門', 'palace': 1, 'palace_name': '坎一宮', 'men_wx': '土', 'palace_wx': '水',
     'relation': '土剋水（門剋宮）'},
    {'men': '死門', 'palace': 1, 'palace_name': '坎一宮', 'men_wx': '土', 'palace_wx': '水',
     'relation': '土剋水（門剋宮）'},
    {'men': '傷門', 'palace': 2, 'palace_name': '坤二宮', 'men_wx': '木', 'palace_wx': '土',
     'relation': '木剋土（門剋宮）'},
    {'men': '傷門', 'palace': 8, 'palace_name': '艮八宮', 'men_wx': '木', 'palace_wx': '土',
     'relation': '木剋土（門剋宮）'},
    {'men': '杜門', 'palace': 2, 'palace_name': '坤二宮', 'men_wx': '木', 'palace_wx': '土',
     'relation': '木剋土（門剋宮）'},
    {'men': '杜門', 'palace': 8, 'palace_name': '艮八宮', 'men_wx': '木', 'palace_wx': '土',
     'relation': '木剋土（門剋宮）'},
    {'men': '景門', 'palace': 6, 'palace_name': '乾六宮', 'men_wx': '火', 'palace_wx': '金',
     'relation': '火剋金（門剋宮）'},
    {'men': '景門', 'palace': 7, 'palace_name': '兌七宮', 'men_wx': '火', 'palace_wx': '金',
     'relation': '火剋金（門剋宮）'},
]

BAMEN_WUXING = {
    '休門':'水', '生門':'土', '傷門':'木', '杜門':'木',
    '景門':'火', '死門':'土', '驚門':'金', '開門':'金',
}

print(f'  門迫（門的五行剋宮的五行 = 共{len(MENPO)}個組合）：')
print(f'  {"門":<6} {"宮位":<10} {"門五行":<6} {"宮五行":<6} {"關係"}')
print('  ' + '-' * 50)
for item in MENPO:
    print(f'  {item["men"]:<6} {item["palace_name"]:<10} {item["men_wx"]:<6} {item["palace_wx"]:<6} {item["relation"]}')
print()

# 驗證門迫：門五行剋宮五行
print('  驗證：所有門迫組合是否滿足「門五行剋宮五行」')
all_mp_valid = True
for item in MENPO:
    valid = item['palace_wx'] in WUXING_KE.get(item['men_wx'], [])
    if not valid:
        all_mp_valid = False
        print(f'    ❌ {item["men"]}落{item["palace_name"]}: {item["men_wx"]}不剋{item["palace_wx"]}')
if all_mp_valid:
    print('    ✅ 全部門迫組合驗證通過（門剋宮）')
print()

# 統計各門被門迫的情況
print('  各門門迫統計：')
from collections import Counter
men_count = Counter(m['men'] for m in MENPO)
for men in BAMEN:
    cnt = men_count.get(men, 0)
    if cnt > 0:
        palaces = [m['palace_name'] for m in MENPO if m['men'] == men]
        print(f'    {men}: {cnt}個 → {"、".join(palaces)}')
    else:
        print(f'    {men}: 無門迫')
print()

# ============================================================
# Section 11: 門迫完整推導（為何是這12個）
# ============================================================
print('=' * 70)
print('Section 11: 門迫完整推導')
print('=' * 70)

print('  門迫定義：門的五行剋所在宮位的五行（門剋宮）')
print('  → 遍歷8門 × 9宮，找出所有「門剋宮」的組合')
print()

print(f'  {"門":<6} {"門五":<4} {"可落宮（不迫）":<40} {"門迫宮（門剋宮）"}')
print('  ' + '-' * 80)
for men, m_wx in BAMEN_WUXING.items():
    safe_palaces = []
    danger_palaces = []
    for p, p_wx in PALACE_WUXING.items():
        if p == 5:
            continue  # 中宮不入
        if p_wx in WUXING_KE.get(m_wx, []):
            danger_palaces.append(f'{GONG_NAMES[p]}({p})')
        else:
            safe_palaces.append(f'{GONG_NAMES[p]}({p})')
    print(f'  {men:<6} {m_wx:<4} {"、".join(safe_palaces):<40} {"、".join(danger_palaces) if danger_palaces else "無"}')
print()

# ============================================================
# Section 12: 與之前集數的對照
# ============================================================
print('=' * 70)
print('Section 12: 與之前集數的對照')
print('=' * 70)

print('1. 用神體系擴充')
print('   EP08(投資): 值符=投資者、值使=項目...')
print('   EP09(多選一): 值符=自己、各宮=各選項...')
print('   EP10(買貨): 值符=買方、生門=賣方...')
print('   EP11(合作): 值符=自己、天乙=對方...')
print('   EP12(追債): 值符=債權人、天乙=債務人...')
print('   EP17(本集): 值符=原告、天乙=被告 + 開門=法院、六合=證據、景門=訴狀、驚門=律師')
print('   → 官司場景用神最多（6個），因為官司涉及多個角色')
print()

print('2. 天乙太乙的定義演變')
print('   EP11(合作): 天乙=對方（值符落宮地盤天干）')
print('   EP12(追債): 天乙=債務人（同上）')
print('   EP17(官司): 天乙=被告（同上，第三次確認）')
print('   → 天乙的定義已穩定：值符落宮原地盤天干')
print()

print('3. 反吟局的應用擴展')
print('   EP12(追債): 反吟=事情反反覆覆')
print('   EP17(官司): 反吟=不會一次審完，輸了會上訴')
print('   → 同一格局在不同場景有不同含義，但核心「反覆」不變')
print()

print('4. 十干剋應 vs 新凶格')
print('   EP13(十干剋應): 庚+日干已在81組合中（但未單獨定義為格局）')
print('   EP17: 飛干格(日干+庚)、伏干格(庚+日干)正式命名為凶格')
print('   → 飛干/伏干是十干剋應中特定組合的「格局化」')
print()

print('5. 格局系統擴充總結')
prev_geju = ['衝格', '合格', '伏吟', '反吟', '螣蛇夭矯', '青龍逃走', '十干剋應(81組)',
             '玉女守門', '三奇貴人升殿', '奇遊祿位', '天輔吉時']
new_geju = ['飛干格(10組)', '伏干格(10組)', '刑格(1組)', '六儀擊刑(6組)']
print(f'   之前已有: {"、".join(prev_geju)}')
print(f'   EP17新增: {"、".join(new_geju)}')
print(f'   加上五不遇時(10組)和門迫(12組) → 格局檢測庫大幅擴充')
print()

# ============================================================
# Section 13: EP17 新發現的不足
# ============================================================
print('=' * 70)
print('Section 13: EP17 新發現的不足')
print('=' * 70)

NEW_GAPS_EP17 = [
    ('G86', '中', '官司用神中的天乙確定方法',
     '值符落宮地盤天干=天乙，但需確認是否天乙太乙（八神）還是值符落宮地盤天干本身',
     '師傅明確：值符落宮原地盤天干就是天乙太乙'),
    ('G87', '中', '門迫對官司判斷的具體影響',
     '開門（法院）門迫會怎樣？驚門（律師）門迫會怎樣？',
     '需建立門迫×用神的交叉影響規則'),
    ('G88', '低', '五不遇時的時辰天干推算',
     '需要從日干推算各時辰的天干（與EP16天輔吉時的甲X時類似）',
     '需實現日上起時法則'),
    ('G89', '低', '六儀擊刑的嚴重程度排序',
     '6個六儀擊刑是否同等嚴重？有沒有分級？',
     '需等待師傅後續講解或案例分析'),
    ('G90', '低', '飛干格/伏干格在官司場景的特殊含義',
     '一般含義已知，但官司中飛干=原告遭遇不測？伏干=原告失去自由？',
     '需確認格局含義的場景化解讀'),
]

for gid, priority, name, current, expected in NEW_GAPS_EP17:
    print(f'  [{priority}] {gid}: {name}')
    print(f'       現狀: {current}')
    print(f'       期望: {expected}')
    print()

# ============================================================
# Section 14: 結論
# ============================================================
print('=' * 70)
print('Section 14: 結論')
print('=' * 70)

print('EP17 的核心貢獻：')
print('  1. 官官司訴訟六用神（值符/天乙/開門/六合/景門/驚門）')
print('  2. 官司輸贏判斷三步法（值符vs天乙 → 日干vs時干 → 開門取向）')
print('  3. 反吟局+官司 = 會上訴，不會一次結束')
print('  4. 飛干格（日干+庚）= 遭遇不測')
print('  5. 伏干格（庚+日干）= 遭遇不測+失去自由')
print('  6. 刑格（庚+己）= 官司破財患病')
print('  7. 六儀擊刑（僅6個固定組合）')
print('  8. 五不遇時（10個同五行相剋組合）')
print('  9. 門迫（12個門宮組合，門剋宮）')
print(' 10. 商業糾紛案例實戰演示')
print()

print('對 backtest 的影響：')
print('  - 官司用神 = 新的預測場景類型')
print('  - 3個新凶格 + 六儀擊刑 + 五不遇時 + 門迫 = 大幅擴充格局檢測庫')
print('  - 門迫可自動檢測（門的五行 vs 宮的五行）')
print('  - 五不遇時可自動檢測（日干 vs 時干五行）')
print('  - 累計 Gap: G01-G90')
print()

# ============================================================
# Section 15: JSON 輸出
# ============================================================

ep17_data = {
    "episode": 17,
    "title": "官司訴訟預測 + 常用凶格",
    "lawsuit_yongshen": {
        name: {"represents": info["represents"], "detail": info["detail"]}
        for name, info in LAWSUIT_YONGSHEN.items()
    },
    "judgment_method": {
        step: {k: v for k, v in info.items() if k != 'method'}
        for step, info in JUDGMENT_METHOD.items()
    },
    "fanyin_lawsuit": {
        "meaning": FANYIN_LAWSUIT['meaning'],
        "detail": FANYIN_LAWSUIT['detail'],
    },
    "xiong_ge": {
        "飛干格": {
            "condition": FEIGAN_GE['condition'],
            "meaning": FEIGAN_GE['meaning'],
            "total_combinations": 10,
        },
        "伏干格": {
            "condition": FUGAN_GE['condition'],
            "meaning": FUGAN_GE['meaning'],
            "total_combinations": 10,
        },
        "刑格": {
            "condition": XING_GE['condition'],
            "meaning": XING_GE['meaning'],
            "total_combinations": 1,
        },
    },
    "liuyi_xingxing": [
        {"tiangan": x['tiangan'], "palace": x['palace'], "palace_name": x['palace_name']}
        for x in LIUYI_XINGXING
    ],
    "wubuyushi": [
        {"day_gan": w['day_gan'], "hour_gan": w['hour_gan']}
        for w in WUBUYUSHI
    ],
    "menpo": [
        {"men": m['men'], "palace": m['palace'], "palace_name": m['palace_name'],
         "men_wuxing": m['men_wx'], "palace_wuxing": m['palace_wx']}
        for m in MENPO
    ],
    "bamen_wuxing": BAMEN_WUXING,
    "new_gaps": [
        {"id": g[0], "priority": g[1], "name": g[2], "current": g[3], "expected": g[4]}
        for g in NEW_GAPS_EP17
    ],
}

output_path = '/home/z/my-project/download/ep17_lawsuit_xiongge.json'
with open(output_path, 'w') as f:
    json.dump(ep17_data, f, ensure_ascii=False, indent=2)
print(f'→ 已輸出 {output_path}')
print('\n' + '*' * 70)
print('  EP17 量化完成！')
print('*' * 70)
