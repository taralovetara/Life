#!/usr/bin/env python3
"""
EP19 量化腳本：考試升學預測 + 值符與值使
===================================================================

本集新知識點：
1. 考試升學四用神體系（考生/學校/天輔星/試卷）
2. 考生用神確定規則（親自求測 vs 代測六親）
3. 升學結果判斷方法（四用神宮位生剋關係）
4. DSE升學案例實戰分析
5. 多校錄取的選擇方法（編號法）
6. 小值符（八神之首，消災解難）
7. 大值符（旬首天星，大權力+大吉祥）
8. 六十甲子與旬的結構（6旬，每旬10組）
9. 值符值使的固定對應關係
10. 值使的定義與角色（執行領導）
11. 值符值使隨時間更替的規律
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
BAMEN_WUXING = {'休門':'水','生門':'土','傷門':'木','杜門':'木','景門':'火','死門':'土','驚門':'金','開門':'金'}
TIANGAN = ['甲','乙','丙','丁','戊','己','庚','辛','壬','癸']
BAMEN = ['休門','生門','傷門','杜門','景門','死門','驚門','開門']

# ============================================================
# Section 1: 考試升學四用神體系
# ============================================================
print('=' * 70)
print('Section 1: 考試升學四用神體系')
print('=' * 70)

EXAM_YONGSHEN = {
    '考生': {
        'rules': [
            {'condition': '考生親自來求測', 'yongshen': '日干',
             'reason': '日干代表求測人自己'},
            {'condition': '家人/朋友代為求測', 'yongshen': '六親用神',
             'reason': '根據考生與求測人的六親關係確定'},
            {'condition': '父母為兒女求測', 'yongshen': '時干',
             'reason': '兒女對應時干（子女位）'},
        ],
        'engine_note': '需實現六親關係->用神天干的完整映射',
    },
    '錄取學校': {
        'yongshen': '年干',
        'reason': '年干=太歲=國家最高領導，古代讀書人進京趕考需通過皇帝測試',
        'detail': [
            '年干代表最終錄取考生的那間學校',
            '如果填報多間學校，年干是最後錄取的那間',
        ],
        'engine_note': '年干可從 qiju() 返回結果直接取得',
    },
    '繼續升學機會': {
        'yongshen': '天輔星',
        'reason': '天輔星代表有機會繼續讀書、繼續升學',
        'detail': [
            '就算公開試成績不夠好，不一定沒機會繼續上學',
            '還可以重讀、去海外上學、到社會找工作等',
            '天輔星用於判斷最終是否有書讀',
        ],
        'engine_note': '天輔星為九星之一，可從星盤取得',
    },
    '試卷/試題': {
        'yongshen': '景門',
        'reason': '景門代表考試的試卷和試題',
        'detail': [
            '景門與考生的關係決定作答情況',
            '景門生考生宮 -> 考生答題好，成績好',
            '景門剋考生宮 -> 試題太難，考生答不好',
        ],
        'engine_note': '景門為八門之一，可從門盤取得',
    },
}

for role, info in EXAM_YONGSHEN.items():
    print(f'\n  {role}:')
    if 'yongshen' in info:
        print(f'    用神: {info["yongshen"]}')
    if 'reason' in info:
        print(f'    原因: {info["reason"]}')
    if 'rules' in info:
        for r in info['rules']:
            print(f'    規則: {r["condition"]} -> {r["yongshen"]} ({r["reason"]})')
    if 'detail' in info:
        for d in info['detail']:
            print(f'    - {d}')
    if 'engine_note' in info:
        print(f'    [Engine] {info["engine_note"]}')
print()

# ============================================================
# Section 2: 升學結果判斷方法
# ============================================================
print('=' * 70)
print('Section 2: 升學結果判斷方法')
print('=' * 70)

EXAM_JUDGMENT = [
    {'step': 1, 'check': '景門宮 vs 考生宮',
     'sheng': '景門宮生考生宮 -> 考生答題好，成績不差',
     'ke': '景門宮剋考生宮 -> 試題對考生不利',
     'bihe': '景門宮與考生宮比和 -> 成績一般'},
    {'step': 2, 'check': '年干宮 vs 考生宮',
     'sheng': '年干宮生考生宮 -> 學校會錄取考生',
     'ke': '年干宮剋考生宮 -> 學校不會錄取',
     'bihe': '年干宮與考生宮比和 -> 錄取與否需看其他因素'},
    {'step': 3, 'check': '天輔星宮 vs 考生宮',
     'sheng': '天輔星宮生考生宮 -> 有機會繼續升學',
     'ke': '天輔星宮剋考生宮 -> 升學機會渺茫',
     'bihe': '天輔星宮與考生宮比和 -> 升學看運氣'},
    {'step': 4, 'check': '綜合判斷',
     'all_sheng': '三個用神都生考生 -> 大吉，一定考上',
     'mixed': '部分生部分剋 -> 需綜合權衡',
     'all_ke': '三個用神都剋考生 -> 凶，考不上',
     'note': '年干和天輔星同宮會雙重印證（如案例中同落坤二宮）'},
]

for j in EXAM_JUDGMENT:
    print(f'\n  步驟{j["step"]}: {j["check"]}')
    for k, v in list(j.items())[2:]:
        print(f'    {k}: {v}')
print()

# ============================================================
# Section 3: DSE升學案例實戰分析
# ============================================================
print('=' * 70)
print('Section 3: DSE升學案例實戰分析')
print('=' * 70)

CASE_DSE = {
    'background': '母親為兒子求測DSE成績和升學結果',
    'question': '兒子DSE考得好不好？能否入讀本地大學？需不需要報海外大學？',
    'analysis': [
        {'step': 1, 'yongshen': '考生（時干己）', 'palace': '乾六宮',
         'companions': ['太陰', '驚門', '天芮星', '空亡', '驛馬'],
         'tiangan_combo': ['己+庚', '丙+庚'],
         'interpretation': '考生心裡非常擔心，忐忑不安，四處找人商量，東奔西跑，身心俱疲',
         'note': '日干和時干都是己 -> 母子同頻共振，可憐天下父母心'},
        {'step': 2, 'yongshen': '景門（試卷試題）', 'palace': '坤二宮',
         'relation': '坤二宮(土)生乾六宮(金)',
         'interpretation': '試卷生考生 -> 考生答題不錯，DSE考得挺好',
         'conclusion': '成績不差'},
        {'step': 3, 'yongshen': '年干戊（錄取學校）', 'palace': '坤二宮',
         'companions': ['值符', '天輔星'],
         'tiangan_combo': ['戊+丙', '戊+己'],
         'relation': '坤二宮(土)生乾六宮(金)',
         'interpretation': '學校有相當高名氣的傳統名校（雖然世界排名有所下滑），會錄取考生',
         'conclusion': '成績足夠考上本地大學'},
        {'step': 4, 'yongshen': '天輔星（繼續升學）', 'palace': '坤二宮',
         'relation': '與年干、景門同宮，也生乾六宮',
         'interpretation': '天輔星與學校、試題同宮 -> 三重印證',
         'conclusion': '一定可以繼續學業，繼續升學'},
    ],
    'result': '幾個月後確認：兒子考得挺好，考上歷史悠久的本地大學電子工程專業',
}

print(f'  背景: {CASE_DSE["background"]}')
print(f'  問題: {CASE_DSE["question"]}')
print()
for a in CASE_DSE['analysis']:
    print(f'  步驟{a["step"]}: {a["yongshen"]}')
    print(f'    落宮: {a["palace"]}')
    if a.get('companions'):
        print(f'    同宮: {"、".join(a["companions"])}')
    if a.get('tiangan_combo'):
        print(f'    天干組合: {"、".join(a["tiangan_combo"])}')
    if a.get('relation'):
        print(f'    關係: {a["relation"]}')
    print(f'    解讀: {a["interpretation"]}')
    if a.get('conclusion'):
        print(f'    結論: {a["conclusion"]}')
    if a.get('note'):
        print(f'    備註: {a["note"]}')
    print()
print(f'  實際結果: {CASE_DSE["result"]}')
print()

# 驗證五行生剋關係
print('  五行生剋驗證：')
test_cases = [
    ('坤二宮(土)', '乾六宮(金)', '土生金'),
]
for src, dst, expected in test_cases:
    src_wx = src.split('(')[1].rstrip(')')
    dst_wx = dst.split('(')[1].rstrip(')')
    actual = '生' if dst_wx in WUXING_SHENG.get(src_wx, []) else ('剋' if dst_wx in WUXING_KE.get(src_wx, []) else '其他')
    status = 'OK' if expected in actual else 'FAIL'
    print(f'    {src} -> {dst}: 期望{expected}, 實際{src_wx}{actual}{dst_wx} [{status}]')
print()

# ============================================================
# Section 4: 多校錄取選擇方法
# ============================================================
print('=' * 70)
print('Section 4: 多校錄取選擇方法')
print('=' * 70)

print('  當多於一家學校錄取考生時：')
print('    1. 求測人對幾家學校進行編號（如學校A=1, 學校B=2, ...）')
print('    2. 逐一分析每間學校與考生之間的生剋關係')
print('    3. 選擇生考生宮的那間學校')
print('    4. 此方法與 EP09(多選一投資) 的編號法原理相同')
print()
print('  交叉參照：')
print('    EP09(投資多選一): 各宮位=各選項，比較與值符的關係')
print('    EP19(升學多選一): 各學校編號後逐一與考生比較')
print('    -> 核心方法一致：逐一比較生剋關係')
print()

# ============================================================
# Section 5: 小值符
# ============================================================
print('=' * 70)
print('Section 5: 小值符')
print('=' * 70)

XIAO_ZHIFU = {
    'identity': '八神之首',
    'nature': '神秘力量的一種',
    'ability': '所到之處消災解難',
    'auspiciousness': '吉祥力量非常強大',
    'location': '神盤八神裡的值符',
    'cross_ref': 'EP04(八神)已詳細講解',
    'relationship_with_dazhifu': '小值符一般跟隨大值符一起出現，從不分開，可說二位一體',
}

for k, v in XIAO_ZHIFU.items():
    label = k.replace('_', ' ')
    print(f'  {label}: {v}')
print()

# ============================================================
# Section 6: 六十甲子與旬的結構
# ============================================================
print('=' * 70)
print('Section 6: 六十甲子與旬的結構')
print('=' * 70)

TIANGAN_10 = ['甲','乙','丙','丁','戊','己','庚','辛','壬','癸']
DIZHI_12 = ['子','丑','寅','卯','辰','巳','午','未','申','酉','戌','亥']

LIUSHI_JIAZI = []
for i in range(60):
    tg = TIANGAN_10[i % 10]
    dz = DIZHI_12[i % 12]
    LIUSHI_JIAZI.append(tg + dz)

XUN_NAMES = ['甲子旬', '甲戌旬', '甲申旬', '甲午旬', '甲辰旬', '甲寅旬']
XUNS = []
for x in range(6):
    xun_start = x * 10
    xun = LIUSHI_JIAZI[xun_start:xun_start+10]
    XUNS.append({'name': XUN_NAMES[x], 'xunshou': xun[0], 'combinations': xun})

print(f'  六十甲子 = 10天干 x 12地支的最小公倍數 = 60個干支組合')
print(f'  分為6旬，每旬10個組合：')
print()
for xun in XUNS:
    print(f'  {xun["name"]}（旬首：{xun["xunshou"]}）：')
    print(f'    {"、".join(xun["combinations"])}')
print()

XUNSHOU_LIST = [xun['xunshou'] for xun in XUNS]
print('  六個旬首：')
print(f'    {"、".join(XUNSHOU_LIST)}')
print()

DIZHI_SET = set(DIZHI_12)
XUNKONG = []
for xun in XUNS:
    xun_dz = set(c[1] for c in xun['combinations'])
    missing = sorted(DIZHI_SET - xun_dz, key=lambda z: DIZHI_12.index(z))
    XUNKONG.append({'xun': xun['name'], 'xunkong': missing})

print('  旬空（每旬缺少的兩個地支）：')
for xk in XUNKONG:
    print(f'    {xk["xun"]}: {"、".join(xk["xunkong"])}空')
print()

# ============================================================
# Section 7: 大值符
# ============================================================
print('=' * 70)
print('Section 7: 大值符')
print('=' * 70)

DA_ZHIFU = {
    'definition': '剛好落在旬首的那顆天星',
    'power_source': '旬首擁有最大權力，掌控整旬全部',
    'role': '這一旬裡的老大，擁有旬首的能量和權力',
    'example': '現在是甲寅旬，甲寅臨天輔星 -> 天輔星就是大值符',
    'combined_with_xiaozhifu': '在盤局中的值符同時擁有大值符和小值符的性質',
    'combined_meaning': '既代表大權力，也代表大吉祥',
    'corporate_analogy': '董事會/董事會主席，掌握整個企業決策權',
}

for k, v in DA_ZHIFU.items():
    label = k.replace('_', ' ')
    print(f'  {label}: {v}')
print()

print('  大值符確定邏輯：')
print('    1. 確定當前時間所屬的旬（由日柱確定）')
print('    2. 找到該旬的旬首天干地支組合')
print('    3. 查看旬首天干落在哪顆天星上')
print('    4. 該天星即為大值符')
print()

# ============================================================
# Section 8: 值使的定義與角色
# ============================================================
print('=' * 70)
print('Section 8: 值使的定義與角色')
print('=' * 70)

ZHISHI = {
    'definition': '值符那個天星原來宮位的八門就是值使',
    'role': '將值符所做的決策具體落實執行的指揮人',
    'power': '除值符之外，這一旬裡權力最大的',
    'corporate_analogy': '首席執行官(CEO)',
    'relationship': '值符(董事會主席)發佈指令 -> 值使(CEO)帶領執行',
    'same_team': '值符與值使屬於同一個領導團隊，同氣連支',
}

for k, v in ZHISHI.items():
    label = k.replace('_', ' ')
    print(f'  {label}: {v}')
print()

print('  值使確定邏輯：')
print('    1. 先確定值符是哪顆天星')
print('    2. 找到該天星的本位宮（原來固定所在的宮位）')
print('    3. 該本位宮對應的八門就是值使')
print('    4. 兩者關係固定不變：知道一個就可確定另一個')
print()

# ============================================================
# Section 9: 九星本位宮與值使的固定對應
# ============================================================
print('=' * 70)
print('Section 9: 九星本位宮與值使的固定對應')
print('=' * 70)

TIANXING_HOME = {
    '天蓬': 1, '天芮': 2, '天沖': 3, '天輔': 4,
    '天禽': 5, '天心': 6, '天柱': 7, '天任': 8, '天英': 9,
}

BAMEN_HOME = {
    '休門': 1, '生門': 8, '傷門': 3, '杜門': 4,
    '景門': 9, '死門': 2, '驚門': 7, '開門': 6,
}

print(f'  {"值符(星)":<8} {"星本位宮":<10} {"值使(門)":<8}')
print('  ' + '-' * 30)
ZHIFU_ZHISHI_MAP = {}
for star, home_palace in TIANXING_HOME.items():
    zhishi_men = '??'
    note = ''
    if home_palace == 5:
        zhishi_men = '死門'
        note = '(中宮寄坤)'
    else:
        for men, mp in BAMEN_HOME.items():
            if mp == home_palace:
                zhishi_men = men
                break
    ZHIFU_ZHISHI_MAP[star] = zhishi_men
    print(f'  {star:<8} {GONG_NAMES[home_palace]}{home_palace}宮    {zhishi_men:<8} {note}')
print()

print('  特殊情況：天禽星本位中五宮')
print('    中五宮無門，寄於坤二宮')
print('    當值符為天禽星時，值使為死門（坤二宮之門）')
print()

ZHISHI_ZHIFU_MAP = {}
for star, men in ZHIFU_ZHISHI_MAP.items():
    if men not in ZHISHI_ZHIFU_MAP:
        ZHISHI_ZHIFU_MAP[men] = []
    ZHISHI_ZHIFU_MAP[men].append(star)

print('  反向查詢（值使 -> 可能的值符）：')
for men in BAMEN:
    stars = ZHISHI_ZHIFU_MAP.get(men, [])
    if stars:
        print(f'    {men} -> {"、".join(stars)}')
print()

# ============================================================
# Section 10: 值符值使隨時間更替
# ============================================================
print('=' * 70)
print('Section 10: 值符值使隨時間更替')
print('=' * 70)

TIME_TRANSITION = [
    {'rule': '時間從一旬進入另一旬', 'effect': '旬首改變，值符值使跟著改變'},
    {'rule': '值符值使失去權力', 'effect': '前旬的值符值使下台，完全喪失權力'},
    {'rule': '企業比喻', 'effect': '如同企業定期更換董事會成員和CEO'},
    {'rule': '應用意義', 'effect': '不同時間起局，值符值使不同，預測結果可能不同'},
]

for t in TIME_TRANSITION:
    print(f'  {t["rule"]}: {t["effect"]}')
print()

print('  值符值使在盤局中的意義：')
for m in ['值符 = 當前旬的決策者，代表大權力+大吉祥',
          '值使 = 當前旬的執行者，代表行動力和推進力',
          '值符落宮 = 決策者的位置和狀態',
          '值使落宮 = 執行者的位置和狀態',
          '值符值使同宮 = 決策與執行一致，事情順利',
          '值符值使相衝 = 決策與執行矛盾，事情受阻']:
    print(f'    - {m}')
print()

# ============================================================
# Section 11: 值符值使與之前集數用神的整合
# ============================================================
print('=' * 70)
print('Section 11: 值符值使與之前集數用神的整合')
print('=' * 70)

ZHIFU_USAGE = [
    ('EP08(投資)', '值符=投資者', '值符本身作為求測人用神'),
    ('EP09(多選一)', '值符=自己', '以值符宮位為基準比較各選項'),
    ('EP10(買貨)', '值符=買方', '值符代表交易中的一方'),
    ('EP11(合作)', '值符=自己,天乙=對方', '值符落宮地盤天干=天乙'),
    ('EP12(追債)', '值符=債權人,天乙=債務人', '值符 vs 天乙判斷輸贏'),
    ('EP17(民事官司)', '值符=原告,天乙=被告', '加上開門=法院等六用神'),
    ('EP18(刑事訴訟)', '辛=疑犯,開門=法院', '值符不再直接作為用神'),
    ('EP19(本集-升學)', '日干/時干=考生,年干=學校', '值符作為吉神參考'),
]

print(f'  {"集數":<20} {"值符角色":<30} {"說明"}')
print('  ' + '-' * 75)
for ep, role, note in ZHIFU_USAGE:
    print(f'  {ep:<20} {role:<30} {note}')
print()

print('  觀察：')
print('    - 值符在多數場景中代表求測人或一方當事人')
print('    - EP18刑事訴訟中值符退出核心用神位置（辛取代）')
print('    - EP19升學預測也未直接用值符（用日干/時干/年干）')
print('    - 值符作為吉神出現在宮中時仍代表正能量')
print()

# ============================================================
# Section 12: 與之前集數的對照
# ============================================================
print('=' * 70)
print('Section 12: 與之前集數的對照')
print('=' * 70)

cross_refs = [
    ('升學用神 vs 投資用神',
     'EP08(投資): 值符=投資者、生門=利潤',
     'EP19(升學): 日干/時干=考生、年干=學校、景門=試題、天輔=升學',
     '升學場景用神更多元，涉及4個不同角色'),
    ('六親用神再確認',
     'EP02(婚姻): 時干=丈夫/妻子',
     'EP19(升學): 時干=兒女（父母為兒女求測）',
     '時干=子女位的映射再次確認，與EP02一致'),
    ('天輔星的新角色',
     '之前: 天輔星僅作為九星之一，影響文書/學業',
     'EP19: 天輔星直接作為用神，代表繼續升學的機會',
     '天輔星從輔助參考提升為核心用神之一'),
    ('景門的多重角色',
     'EP17(官司): 景門=入稟狀/訴狀',
     'EP19(升學): 景門=試卷/試題',
     '景門都代表文件/文書類事物'),
    ('年干的新角色',
     '之前: 年干主要作為太歲的間接參考',
     'EP19: 年干直接作為用神，代表錄取學校',
     '年干從太歲象意擴展為具體的機構用神'),
    ('值符值使的理論深度',
     'EP01-EP16: 值符值使被使用但未系統講解',
     'EP19: 完整講解大值符、小值符、值使的定義和關係',
     '補全了奇門基礎理論的重要一環'),
    ('編號選擇法通用化',
     'EP09(投資多選一): 編號法選擇最佳選項',
     'EP19(升學多選一): 同樣使用編號法',
     '編號法是通用方法，適用於所有多選一場景'),
]

for title, before, after, insight in cross_refs:
    print(f'  {title}:')
    print(f'    之前: {before}')
    print(f'    本集: {after}')
    print(f'    洞察: {insight}')
    print()

# ============================================================
# Section 13: EP19 新發現的不足
# ============================================================
print('=' * 70)
print('Section 13: EP19 新發現的不足')
print('=' * 70)

NEW_GAPS_EP19 = [
    ('G99', '高', '六親關係->用神天干的完整映射表',
     '師傅多次提到根據六親關係選年干/月干/時干，但始終未給出完整映射',
     '需建立父母/子女/兄弟/夫妻/朋友->四干的完整映射'),
    ('G100', '高', '旬的確定方法（從日期推算）',
     '師傅講了旬的概念和大值符的確定，但未講如何從日期推算當前旬',
     '需實現日期->日柱->旬->旬首的完整推算鏈'),
    ('G101', '中', '值使的實際落宮確定方法',
     '師傅講了值使是值符星本位宮的門，但值使在盤局中落在哪個宮？',
     '需確認值使是否隨時辰飛動（類似值符隨時辰飛動）'),
    ('G102', '中', '天禽星值符的值使確定',
     '天禽星本位中五宮，中宮無門，師傅未明確說此時值使如何確定',
     '需確認是寄坤宮的死門還是其他處理方式'),
    ('G103', '中', '值符值使同宮/相衝的具體判斷',
     '提到同宮=順利、相衝=受阻，但相衝的定義未明確',
     '需確認是宮位對衝還是五行相剋'),
    ('G104', '低', '考試預測的量化評分函數',
     '四用神生剋關係需轉化為可計算評分',
     '需實現 exam_prediction() 函數'),
    ('G105', '低', '多校選擇的編號與宮位對應方法',
     '編號法提到但未詳細講解編號如何對應宮位',
     '需參考EP09的編號法實現'),
]

for gid, priority, name, current, expected in NEW_GAPS_EP19:
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

contributions = [
    '考試升學四用神（考生=日干/時干、學校=年干、天輔星=升學機會、景門=試題）',
    '考生用神確定規則（親自求測用日干，代測按六親選干）',
    '升學結果判斷三步法（景門vs考生 -> 年干vs考生 -> 天輔vs考生）',
    'DSE升學案例實戰（四用神全部生考生，大吉）',
    '多校錄取選擇方法（編號法，與EP09通用）',
    '小值符定義（八神之首，消災解難）',
    '大值符定義（旬首天星，大權力+大吉祥）',
    '六十甲子與旬的完整結構（6旬、每旬10組、旬空）',
    '值使定義（值符星本位宮的門=CEO角色）',
    '值符值使固定對應表（9星->9門映射）',
    '值符值使隨時間更替規律',
]
print('EP19 的核心貢獻：')
for i, c in enumerate(contributions, 1):
    print(f'  {i:>2}. {c}')
print()

print('對 backtest 的影響：')
print('  - 考試升學 = 新的預測場景類型')
print('  - 四用神生剋分析 = 可實現 exam_prediction() 函數')
print('  - 旬的結構 = 值符值使確定的基礎理論')
print('  - 值使的引入 = 盤局解讀的新維度')
print('  - 累計 Gap: G01-G105')
print()

# ============================================================
# Section 15: JSON 輸出
# ============================================================

ep19_data = {
    "episode": 19,
    "title": "考試升學預測 + 值符與值使",
    "exam_yongshen": {
        "考生": {
            "rules": [{"condition": r["condition"], "yongshen": r["yongshen"]} for r in EXAM_YONGSHEN['考生']['rules']],
        },
        "錄取學校": {"yongshen": "年干", "reason": EXAM_YONGSHEN['錄取學校']['reason']},
        "繼續升學機會": {"yongshen": "天輔星", "reason": EXAM_YONGSHEN['繼續升學機會']['reason']},
        "試卷試題": {"yongshen": "景門", "reason": EXAM_YONGSHEN['試卷/試題']['reason']},
    },
    "exam_judgment": [
        {"step": j["step"], "check": j["check"]}
        for j in EXAM_JUDGMENT if "sheng" in j
    ] + [{"step": 4, "check": "綜合判斷", "note": "三用神綜合權衡"}],
    "case_dse": {
        "background": CASE_DSE['background'],
        "result": CASE_DSE['result'],
        "analysis": [
            {"step": a["step"], "yongshen": a["yongshen"], "palace": a["palace"]}
            for a in CASE_DSE['analysis']
        ],
    },
    "zhifu": {
        "xiaozhifu": {"identity": XIAO_ZHIFU['identity'], "ability": XIAO_ZHIFU['ability']},
        "dazhifu": {"definition": DA_ZHIFU['definition'], "role": DA_ZHIFU['role'],
                     "corporate_analogy": DA_ZHIFU['corporate_analogy']},
    },
    "liushi_jiazi": {
        "total": 60,
        "xun_count": 6,
        "xun_names": XUN_NAMES,
        "xunshou_list": XUNSHOU_LIST,
        "xunkong": [{"xun": xk["xun"], "kong": xk["xunkong"]} for xk in XUNKONG],
    },
    "zhishi": {
        "definition": ZHISHI['definition'],
        "role": ZHISHI['role'],
        "corporate_analogy": ZHISHI['corporate_analogy'],
    },
    "zhifu_zhishi_map": ZHIFU_ZHISHI_MAP,
    "tianxing_home": TIANXING_HOME,
    "bamen_home": BAMEN_HOME,
    "new_gaps": [
        {"id": g[0], "priority": g[1], "name": g[2], "current": g[3], "expected": g[4]}
        for g in NEW_GAPS_EP19
    ],
}

output_path = '/home/z/my-project/download/ep19_exam_zhifu_zhishi.json'
with open(output_path, 'w') as f:
    json.dump(ep19_data, f, ensure_ascii=False, indent=2)
print(f'-> 已輸出 {output_path}')
print('\n' + '*' * 70)
print('  EP19 量化完成！')
print('*' * 70)
