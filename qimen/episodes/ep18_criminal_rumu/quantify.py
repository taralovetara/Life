#!/usr/bin/env python3
"""
EP18 量化腳本：刑事訴訟預測 + 入墓格局
===================================================================

本集新知識點：
1. 刑事訴訟用神體系（疑犯/執法/檢控/法院/監獄/判刑）
2. 刑事訴訟階段判斷（拘捕/檢控/審理/定罪）
3. 定罪判斷規則（開門宮 vs 辛宮 生剋比和衝）
4. 定罪加重組合（庚+辛、辛+辛、辛+壬、辛+癸、庚剋辛、辛落巽4）
5. 伏吟局/反吟局對刑事訴訟的影響
6. 商業詐騙案實戰分析
7. 天干入墓（4組宮位，共10天干分佈）
8. 八門入墓（4組宮位，共8門分佈）
9. 入墓含義（身心受限制、能量被困）
10. 出墓與衝墓（時間到入墓地支/對衝地支）
11. 乙在坤二宮也屬入墓（代替甲的特殊規則）
"""

import json

GONG_NAMES = {1:'坎', 2:'坤', 3:'震', 4:'巽', 5:'中', 6:'乾', 7:'兌', 8:'艮', 9:'離'}
PALACE_WUXING = {1:'水', 2:'土', 3:'木', 4:'木', 5:'土', 6:'金', 7:'金', 8:'土', 9:'火'}
TIANGAN_WUXING = {'甲':'木','乙':'木','丙':'火','丁':'火','戊':'土','己':'土','庚':'金','辛':'金','壬':'水','癸':'水'}
BAMEN_WUXING = {'休門':'水','生門':'土','傷門':'木','杜門':'木','景門':'火','死門':'土','驚門':'金','開門':'金'}
TIANGAN = ['甲','乙','丙','丁','戊','己','庚','辛','壬','癸']
BAMEN = ['休門','生門','傷門','杜門','景門','死門','驚門','開門']
DIZHI_CHONG = {'子':'午','午':'子','丑':'未','未':'丑','寅':'申','申':'寅','卯':'酉','酉':'卯','辰':'戌','戌':'辰','巳':'亥','亥':'巳'}

# ============================================================
# Section 1: 刑事訴訟用神體系
# ============================================================
print('=' * 70)
print('Section 1: 刑事訴訟用神體系')
print('=' * 70)

CRIMINAL_YONGSHEN = {
    '疑犯': {
        'primary': '天干辛',
        'reason': '辛本身有犯錯、錯誤的意思，取此象意',
        'secondary': [
            ('疑犯親自求測', '日干也作為用神'),
            ('親朋替疑犯求測', '根據六親關係選年干/月干/時干'),
            ('兒女為父母求測', '年干為用神'),
        ],
        'rule': '天干辛 + 六親用神 一起分析，綜合判斷，不可偏廢',
    },
    '警察部門': {
        'symbols': ['傷門', '白虎', '天干庚'],
        'detail': '三個符號都代表警察/執法部門',
    },
    '檢控部門': {
        'symbols': ['杜門'],
        'detail': '杜門代表檢控部門（香港的律政司）',
    },
    '法院/法庭': {
        'symbols': ['開門'],
        'detail': '開門代表法庭、法院',
    },
    '監獄': {
        'symbols': {'天干辛': '天獄', '天干壬': '地牢', '天干癸': '天網'},
        'detail': '三個天干在現代都代表監獄',
    },
    '判刑': {
        'symbols': ['天干庚'],
        'detail': '庚除了代表警察之外，也是判刑的用神',
        'dual_role': '警察+判刑 = 執法全流程',
    },
}

for role, info in CRIMINAL_YONGSHEN.items():
    print(f'\n  {role}:')
    if 'primary' in info:
        print(f'    主用神: {info["primary"]}')
        print(f'    原因: {info["reason"]}')
    if 'secondary' in info:
        print(f'    輔助用神:')
        for cond, yongshen in info['secondary']:
            print(f'      {cond} -> {yongshen}')
    if 'rule' in info:
        print(f'    規則: {info["rule"]}')
    if 'symbols' in info:
        if isinstance(info['symbols'], dict):
            for sym, meaning in info['symbols'].items():
                print(f'    {sym} = {meaning}')
        else:
            print(f'    符號: {"、".join(info["symbols"])}')
    if 'detail' in info:
        print(f'    詳情: {info["detail"]}')
    if 'dual_role' in info:
        print(f'    雙重角色: {info["dual_role"]}')
print()

# ============================================================
# Section 2: 刑事訴訟階段判斷
# ============================================================
print('=' * 70)
print('Section 2: 刑事訴訟階段判斷')
print('=' * 70)

CRIMINAL_STAGES = [
    {'stage': '警方拘捕階段', 'condition': '天干辛臨白虎、天干庚、傷門、螣蛇',
     'meaning': '疑犯已被警方拘捕', 'detail': '警方正在調查案件和搜集證據'},
    {'stage': '檢控階段', 'condition': '天干辛臨杜門',
     'meaning': '案件已移交檢控部門', 'detail': '等待檢控部門審核及正式向法院提起訴訟'},
    {'stage': '法院審理階段', 'condition': '通過開門宮與天干辛宮的生剋關係判斷',
     'meaning': '案件正在法院審理中', 'detail': '需分析開門宮與辛宮的生/剋/比和'},
]

for s in CRIMINAL_STAGES:
    print(f'\n  {s["stage"]}:')
    print(f'    條件: {s["condition"]}')
    print(f'    含義: {s["meaning"]}')
    print(f'    詳情: {s["detail"]}')
print()

# ============================================================
# Section 3: 定罪判斷規則（核心）
# ============================================================
print('=' * 70)
print('Section 3: 定罪判斷規則（核心）')
print('=' * 70)

CONVICTION_RULES = [
    {'id': 'R01', 'condition': '開門宮生天干辛宮', 'result': '不會判有罪',
     'verdict': '無罪'},
    {'id': 'R02', 'condition': '開門宮與天干辛宮比和', 'result': '定罪但酌情減輕',
     'verdict': '定罪（輕判/緩刑）'},
    {'id': 'R03', 'condition': '開門宮與天干辛宮相衝或相剋', 'result': '一定定罪，判刑較重',
     'verdict': '定罪（重判）'},
    {'id': 'R04', 'condition': '宮位中出現庚+辛', 'result': '一定定罪，判刑很重',
     'verdict': '定罪（重判）'},
    {'id': 'R05', 'condition': '辛+辛、辛+壬、辛+癸', 'result': '定罪判刑，有牢獄之災',
     'verdict': '定罪+監禁'},
    {'id': 'R06', 'condition': '天干庚宮剋天干辛宮', 'result': '定罪判刑',
     'verdict': '定罪'},
    {'id': 'R07', 'condition': '天干辛落在巽四宮', 'result': '容易被判有罪',
     'verdict': '傾向定罪'},
]

print(f'  {"編號":<5} {"條件":<35} {"結果":<25}')
print('  ' + '-' * 65)
for r in CONVICTION_RULES:
    print(f'  {r["id"]:<5} {r["condition"]:<35} {r["result"]:<25}')
print()
print('  無罪條件（默認）：')
print('    如果盤局沒有出現以上各種定罪情況 -> 疑犯會被判無罪')
print()

# ============================================================
# Section 4: 伏吟局/反吟局對刑事訴訟的影響
# ============================================================
print('=' * 70)
print('Section 4: 伏吟局/反吟局對刑事訴訟的影響')
print('=' * 70)

JU_TYPE_CRIMINAL = [
    {'ju_type': '伏吟局', 'meaning': '案件審理會拖很長時間',
     'advice': '要做好打持久戰的準備',
     'cross_ref': 'EP17 民事訴訟中伏吟局=事情不動，刑事同理'},
    {'ju_type': '反吟局', 'meaning': '案件審理速度快',
     'advice': '要做好上訴或者重審的準備',
     'cross_ref': 'EP17 民事訴訟中反吟局=會上訴，刑事同理'},
]

for j in JU_TYPE_CRIMINAL:
    print(f'  {j["ju_type"]}:')
    print(f'    含義: {j["meaning"]}')
    print(f'    建議: {j["advice"]}')
    print(f'    對照: {j["cross_ref"]}')
print()

# ============================================================
# Section 5: 商業詐騙案例實戰分析
# ============================================================
print('=' * 70)
print('Section 5: 商業詐騙案例實戰分析')
print('=' * 70)

CASE_FRAUD = {
    'background': '商業詐騙案，疑犯被警方控告，保釋候審，一星期後開庭',
    'question': '法院會不會判有罪？用不用坐牢？',
    'analysis': [
        {'step': 1, 'yongshen': '天干辛（疑犯）', 'location': '震三宮',
         'companions': ['太陰', '杜門', '天蓬星', '辛+癸'],
         'interpretation': '辛臨杜門=已被檢控起訴，處於監控狀態；天蓬星=大盜之星；辛+癸=被困於法網',
         'conclusion': '很大機率要坐牢'},
        {'step': 2, 'yongshen': '開門（法院）', 'location': '兌七宮',
         'companions': ['九地', '天干庚'],
         'interpretation': '法院態度強硬、公正、保守',
         'relation': '開門兌七宮(金)衝剋辛震三宮(木)',
         'conclusion': '罪成機率非常大'},
        {'step': 3, 'yongshen': '日干己（第二用神）', 'location': '巽四宮',
         'interpretation': '己落巽四宮=執法部門宮位，不吉利',
         'relation': '開門兌七宮(金)剋日干己巽四宮(木)',
         'conclusion': '交叉驗證確認有罪'},
        {'step': 4, 'yongshen': '天干庚（判刑）', 'location': '兌七宮（與開門同宮）',
         'interpretation': '判刑與法院同宮=判刑由法院作出',
         'relation': '庚宮也衝剋辛宮和日干宮',
         'conclusion': '多角度完全一致'},
    ],
    'final_verdict': '必輸無疑，牢獄之災一定跑不掉',
    'additional': '師傅認為此案具備運籌可操作性，留待以後分享',
}

print(f'  背景: {CASE_FRAUD["background"]}')
print(f'  問題: {CASE_FRAUD["question"]}')
print()
for a in CASE_FRAUD['analysis']:
    print(f'  步驟 {a["step"]}: {a["yongshen"]}')
    print(f'    落宮: {a["location"]}')
    if a.get('companions'):
        print(f'    同宮: {"、".join(a["companions"])}')
    print(f'    解讀: {a["interpretation"]}')
    if a.get('relation'):
        print(f'    關係: {a["relation"]}')
    print(f'    結論: {a["conclusion"]}')
    print()
print(f'  最終判斷: {CASE_FRAUD["final_verdict"]}')
print(f'  補充: {CASE_FRAUD["additional"]}')
print()

# ============================================================
# Section 6: 天干入墓
# ============================================================
print('=' * 70)
print('Section 6: 天干入墓')
print('=' * 70)

TIANGAN_RUMU = {
    '坤二宮': ['甲', '癸'],
    '乾六宮': ['乙', '丙', '戊'],
    '艮八宮': ['丁', '己', '庚'],
    '巽四宮': ['辛', '壬'],
}

TIANGAN_RUMU_MAP = {}
for palace, tgs in TIANGAN_RUMU.items():
    for tg in tgs:
        TIANGAN_RUMU_MAP[tg] = palace

print('  天干入墓分佈（十二長生中墓的狀態）：')
print(f'  {"宮位":<10} {"入墓天干":<15} {"數量"}')
print('  ' + '-' * 35)
for palace, tgs in TIANGAN_RUMU.items():
    print(f'  {palace:<10} {"、".join(tgs):<15} {len(tgs)}')
print()

print('  反向查詢（天干 -> 入墓宮位）：')
for tg in TIANGAN:
    rumu_palace = TIANGAN_RUMU_MAP.get(tg, '無')
    print(f'    {tg}({TIANGAN_WUXING[tg]}) -> 入墓於{rumu_palace}')
print()

print('  特殊規則：')
print('    甲在奇門中不出現（遁於六儀之下）')
print('    所以甲入墓以同為五行屬木的乙來代替')
print('    -> 乙在乾六宮入墓（正常）')
print('    -> 乙在坤二宮也屬入墓（代替甲的特殊規則）')
print('    -> 乙有兩個入墓宮位！')
print()

print('  入墓的含義：')
for m in ['身心都受到限制，被困住', '渾渾噩噩，糊里糊塗',
          '自身所有能量都被困住，沒有辦法發揮出來', '性格比較內向，不愛說話']:
    print(f'    - {m}')
print()
print('  用神入墓的判斷：')
print('    用神本身入墓 -> 非常差狀態，無所作為')
print('    用神下臨地盤干入墓 -> 思前想後，猶豫不決')
print()

# ============================================================
# Section 7: 出墓與衝墓
# ============================================================
print('=' * 70)
print('Section 7: 出墓與衝墓')
print('=' * 70)

TIANGAN_RUMU_DZ = {
    '甲': '未', '乙': '未', '丙': '戌', '丁': '丑',
    '戊': '戌', '己': '丑', '庚': '丑', '辛': '戌',
    '壬': '辰', '癸': '辰',
}

print('  出墓：時間到了入墓的地支上面')
print('  衝墓：時間到了入墓地支的對衝位上面')
print()
print(f'  {"天干":<4} {"入墓宮":<10} {"入墓地支":<8} {"對衝地支":<8}')
print('  ' + '-' * 35)
for tg in TIANGAN:
    rumu_palace = TIANGAN_RUMU_MAP.get(tg, '?')
    rumu_dz = TIANGAN_RUMU_DZ.get(tg, '?')
    chong_dz = DIZHI_CHONG.get(rumu_dz, '?')
    print(f'  {tg:<4} {rumu_palace:<10} {rumu_dz}年/月/日/時  {chong_dz}年/月/日/時')
print()

print('  時間單位選擇原則：')
for r in ['需要經歷較長時間的事 -> 採用年或者月',
          '事情較快完成 -> 採用日或者時',
          '根據問測之事的實際情況來定']:
    print(f'    - {r}')
print()

# ============================================================
# Section 8: 八門入墓
# ============================================================
print('=' * 70)
print('Section 8: 八門入墓')
print('=' * 70)

WUXING_RUMU = {'土': '巽', '水': '巽', '木': '坤', '火': '乾', '金': '艮'}

print('  五行入墓分佈：')
for wx, target in WUXING_RUMU.items():
    target_palace = ''
    for p, p_wx in PALACE_WUXING.items():
        if p_wx == target and p != 5:
            target_palace = f'{GONG_NAMES[p]}{p}'
            break
    print(f'    {wx}入墓於{target} -> {target_palace}')
print()

BAMEN_RUMU = {
    '巽四宮': ['生門', '死門', '休門'],
    '坤二宮': ['傷門', '杜門'],
    '乾六宮': ['景門'],
    '艮八宮': ['開門', '驚門'],
}

BAMEN_RUMU_MAP = {}
for palace, mens in BAMEN_RUMU.items():
    for men in mens:
        BAMEN_RUMU_MAP[men] = palace

print('  八門入墓分佈：')
print(f'  {"宮位":<10} {"入墓門":<20} {"入墓規則"}')
print('  ' + '-' * 55)
for palace, mens in BAMEN_RUMU.items():
    rules = set()
    for men in mens:
        rules.add(f'{BAMEN_WUXING[men]}入墓於{WUXING_RUMU[BAMEN_WUXING[men]]}')
    print(f'  {palace:<10} {"、".join(mens):<20} {"/".join(rules)}')
print()

print('  反向查詢（門 -> 入墓宮位）：')
for men in BAMEN:
    rumu_palace = BAMEN_RUMU_MAP.get(men, '無')
    print(f'    {men}({BAMEN_WUXING[men]}) -> 入墓於{rumu_palace}')
print()

print('  八門入墓的應用：')
print('    場景1 - 八門作為用神：狀態跟天干入墓基本相同')
print('      例子：開門(公司)在艮八宮入墓 -> 公司停滯、經營混亂')
print('    場景2 - 八門作為值使：事情很難向前推進')
print('      連帶執行團隊領頭人都處處受困，事情毫無進展')
print()

PALACE_NAME_TO_NUM = {'坤二宮':2,'乾六宮':6,'巽四宮':4,'艮八宮':8}
print('  驗證：八門入墓宮位與五行入墓規則一致性')
all_valid = True
for men, palace_str in BAMEN_RUMU_MAP.items():
    men_wx = BAMEN_WUXING[men]
    expected_wx = WUXING_RUMU[men_wx]
    palace_num = PALACE_NAME_TO_NUM[palace_str]
    actual_wx = PALACE_WUXING[palace_num]
    if actual_wx != expected_wx:
        all_valid = False
        print(f'    X {men}({men_wx})入墓於{palace_str}({actual_wx}), 應入墓於{expected_wx}')
if all_valid:
    print('    OK 全部八門入墓與五行入墓規則一致')
print()

# ============================================================
# Section 9: 與之前集數的對照
# ============================================================
print('=' * 70)
print('Section 9: 與之前集數的對照')
print('=' * 70)

cross_refs = [
    ('刑事vs民事用神',
     'EP17(民事): 值符=原告、天乙=被告、開門=法院',
     'EP18(刑事): 辛=疑犯、庚=警察+判刑、杜門=檢控',
     '刑事用神更多，涉及國家機器全流程'),
    ('庚的多重角色',
     'EP17: 庚在飛干格/伏干格中代表阻礙',
     'EP18: 庚=警察部門+判刑用神',
     '庚是奇門中最具殺傷力的天干'),
    ('辛的多重角色',
     'EP17: 辛+乙=白虎猖狂/青龍逃走',
     'EP18: 辛=疑犯/天獄 + 辛+壬/癸=牢獄之災',
     '辛在刑事場景中是核心用神'),
    ('入墓與十二長生',
     'EP14/EP15: 建立完整十二長生表',
     'EP18: 入墓=十二長生中墓的狀態在九宮分佈',
     '入墓是十二長生的具體應用場景之一'),
    ('門迫 vs 八門入墓',
     'EP17 門迫: 門五行剋宮五行 -> 門受壓迫',
     'EP18 入墓: 門五行入墓於特定宮位 -> 門被困住',
     '兩者都是門的受限狀態，但機制不同'),
    ('伏吟/反吟擴充',
     'EP12: 伏吟=慢/反吟=反覆',
     'EP18: 伏吟=持久戰/反吟=速度快+上訴',
     '同一格局在不同類型訴訟中有更精細解讀'),
]

for title, before, after, insight in cross_refs:
    print(f'  {title}:')
    print(f'    之前: {before}')
    print(f'    本集: {after}')
    print(f'    洞察: {insight}')
    print()

# ============================================================
# Section 10: EP18 新發現的不足
# ============================================================
print('=' * 70)
print('Section 10: EP18 新發現的不足')
print('=' * 70)

NEW_GAPS_EP18 = [
    ('G91', '高', '天干入墓地支的完整對應表',
     '師傅只明確舉例丁入墓於丑，其餘需推導',
     '需用十二長生理論推導完整對應表'),
    ('G92', '高', '六親關係->用神的完整映射',
     '師傅提到根據六親關係選年干/月干/時干，但未列全',
     '需建立完整的六親->四干映射表'),
    ('G93', '中', '刑事訴訟的量化評分函數',
     '定罪判斷規則是定性的，需轉化為可計算評分',
     '需實現 criminal_verdict() 函數'),
    ('G94', '中', '入墓對評分的影響權重',
     '入墓=非常差狀態，但具體扣多少分？',
     '需設計入墓的評分加減規則'),
    ('G95', '中', '出墓/衝墓的時間計算',
     '需要從起局時間推算未來出墓/衝墓時間點',
     '需實現時間推算函數'),
    ('G96', '低', '運籌操作的具體方法',
     '師傅提到具備運籌可操作性但未講解',
     '需等待後續集數分享'),
    ('G97', '低', '辛落巽四宮=執法部門的原理',
     '師傅說巽四宮代表執法部門，但未解釋原因',
     '需研究巽四宮與執法的象意關聯'),
    ('G98', '低', '雙重用神分析的信號加權',
     '刑事訴訟需同時看辛+六親用神，如何加權？',
     '需設計多用神加權算法'),
]

for gid, priority, name, current, expected in NEW_GAPS_EP18:
    print(f'  [{priority}] {gid}: {name}')
    print(f'       現狀: {current}')
    print(f'       期望: {expected}')
    print()

# ============================================================
# Section 11: 結論
# ============================================================
print('=' * 70)
print('Section 11: 結論')
print('=' * 70)

contributions = [
    '刑事訴訟用神體系（辛=疑犯、庚=警察+判刑、杜門=檢控、開門=法院）',
    '監獄三天干（辛=天獄、壬=地牢、癸=天網）',
    '刑事訴訟階段判斷（拘捕->檢控->審理三階段）',
    '定罪判斷7條規則（開門vs辛的生剋比和衝 + 加重組合）',
    '伏吟=持久戰、反吟=速度快+上訴',
    '商業詐騙案例實戰（多角度交叉驗證方法）',
    '天干入墓（4組宮位，含乙代甲特殊規則）',
    '八門入墓（4組宮位，基於五行入墓規則）',
    '出墓/衝墓時間判斷（入墓地支/對衝地支）',
    '預測者的職業操守（如實翻譯，不加主觀情緒）',
]
print('EP18 的核心貢獻：')
for i, c in enumerate(contributions, 1):
    print(f'  {i:>2}. {c}')
print()

print('對 backtest 的影響：')
print('  - 刑事訴訟 = 新的預測場景，可建立 criminal_verdict() 函數')
print('  - 入墓檢測 = 可自動判斷用神是否入墓，影響評分')
print('  - 出墓/衝墓 = 可計算何時擺脫入墓狀態（時間預測）')
print('  - 定罪規則 = 可實現為可計算的邏輯判斷')
print('  - 累計 Gap: G01-G98')
print()

# ============================================================
# Section 12: JSON 輸出
# ============================================================

ep18_data = {
    "episode": 18,
    "title": "刑事訴訟預測 + 入墓格局",
    "criminal_yongshen": {
        "疑犯": {"primary": "天干辛", "secondary_rules": CRIMINAL_YONGSHEN['疑犯']['secondary'],
                  "rule": CRIMINAL_YONGSHEN['疑犯']['rule']},
        "警察部門": {"symbols": CRIMINAL_YONGSHEN['警察部門']['symbols']},
        "檢控部門": {"symbols": CRIMINAL_YONGSHEN['檢控部門']['symbols']},
        "法院": {"symbols": CRIMINAL_YONGSHEN['法院/法庭']['symbols']},
        "監獄": CRIMINAL_YONGSHEN['監獄']['symbols'],
        "判刑": {"symbols": CRIMINAL_YONGSHEN['判刑']['symbols'],
                 "dual_role": CRIMINAL_YONGSHEN['判刑']['dual_role']},
    },
    "conviction_rules": [{"id": r["id"], "condition": r["condition"], "verdict": r["verdict"]} for r in CONVICTION_RULES],
    "ju_type_criminal": [{"type": j["ju_type"], "meaning": j["meaning"], "advice": j["advice"]} for j in JU_TYPE_CRIMINAL],
    "tiangan_rumu": {palace: tgs for palace, tgs in TIANGAN_RUMU.items()},
    "tiangan_rumu_map": TIANGAN_RUMU_MAP,
    "tiangan_rumu_special": "乙在坤二宮也屬入墓（代替甲）",
    "bamen_rumu": {palace: mens for palace, mens in BAMEN_RUMU.items()},
    "bamen_rumu_map": BAMEN_RUMU_MAP,
    "wuxing_rumu": WUXING_RUMU,
    "new_gaps": [{"id": g[0], "priority": g[1], "name": g[2], "current": g[3], "expected": g[4]} for g in NEW_GAPS_EP18],
}

output_path = '/home/z/my-project/download/ep18_criminal_rumu.json'
with open(output_path, 'w') as f:
    json.dump(ep18_data, f, ensure_ascii=False, indent=2)
print(f'-> 已輸出 {output_path}')
print('\n' + '*' * 70)
print('  EP18 量化完成！')
print('*' * 70)