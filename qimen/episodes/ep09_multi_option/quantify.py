#!/usr/bin/env python3
"""
EP09 量化腳本：多選項投資決策 + 九星完整含義 + 天干入墓
===================================================================

本集新知識點：
1. 多選項決策方法：編號定位法（選項編號→對應宮位→用神宮）
2. 選項評估框架：各選項宮 vs 日干宮的生剋比和
3. 九星完整含義及吉凶分類（4吉3凶2中平）
4. 九星與性格判斷（天時=先天遺傳，江山易改秉性難移）
5. 天干入墓概念（日干癸入墓=渾渾噩噩、暫時性）
6. 新天干組合：乙+壬、癸+辛、癸+戊、丁+庚
7. 值符值使與決策狀態（同宮=已開始運作）
8. 選項間排序算法
"""

import json

PALACE_WUXING = {1:'水', 2:'土', 3:'木', 4:'木', 5:'土', 6:'金', 7:'金', 8:'土', 9:'火'}
GONG_NAMES = {1:'坎', 2:'坤', 3:'震', 4:'巽', 5:'中', 6:'乾', 7:'兌', 8:'艮', 9:'離'}
WUXING_SHENG = {"金": "水", "水": "木", "木": "火", "火": "土", "土": "金"}
WUXING_KE   = {"金": "木", "木": "土", "土": "水", "水": "火", "火": "金"}

# ============================================================
# Section 1: 多選項決策方法 — 編號定位法
# ============================================================
print('=' * 70)
print('Section 1: 多選項決策方法 — 編號定位法')
print('=' * 70)

print('\n核心原理：')
print('  當有多個選項需要比較時，為每個選項編號')
print('  編號對應的宮位 = 該選項的用神宮')
print('  然後分析各選項宮位與日干宮的生剋比和關係')
print()

print('編號對應宮位規則：')
print('  1號 → 坎一宮（水）')
print('  2號 → 坤二宮（土）')
print('  3號 → 震三宮（木）')
print('  4號 → 巽四宮（木）')
print('  5號 → 中五宮（土）— 通常不用')
print('  6號 → 乾六宮（金）')
print('  7號 → 兌七宮（金）')
print('  8號 → 艮八宮（土）')
print('  9號 → 離九宮（火）')
print()

print('案例：求測人有三個生意選項')
print('  1號：製衣生意（現有）→ 坎一宮')
print('  2號：代理水果 → 坤二宮')
print('  3號：代購網店 → 震三宮')
print('  日干癸 → 坤二宮（與2號同宮！）')
print()

# 編號定位函數
def option_palace(option_number):
    """選項編號→宮位"""
    return option_number  # 1-9 直接對應宮位

# ============================================================
# Section 2: 選項評估框架 — 生剋比和排序
# ============================================================
print('=' * 70)
print('Section 2: 選項評估框架 — 各選項 vs 日干')
print('=' * 70)

def wx_relation(wx_a, wx_b):
    """返回 A 對 B 的五行關係（從 A 的視角）"""
    if wx_a == wx_b: return '比和'
    if WUXING_SHENG.get(wx_a) == wx_b: return '生'      # A生B
    if WUXING_KE.get(wx_a) == wx_b: return '剋'          # A剋B
    if WUXING_SHENG.get(wx_b) == wx_a: return '被生'      # B生A
    if WUXING_KE.get(wx_b) == wx_a: return '被剋'        # B剋A
    return '未知'

def assess_option(option_palace, rigan_palace, option_name=''):
    """評估單個選項 vs 日干的關係"""
    r = wx_relation(PALACE_WUXING[option_palace], PALACE_WUXING[rigan_palace])
    # 注意：這裡是「選項宮 vs 日干宮」，但師傅的分析視角是日干對選項的影響
    # 需要反過來看：日干宮對選項宮的關係
    r2 = wx_relation(PALACE_WUXING[rigan_palace], PALACE_WUXING[option_palace])
    return r, r2

# 評分規則（從日干視角看選項）
OPTION_SCORE = {
    '比和': +3.0,   # 同宮=順勢而為=最佳
    '剋':   +1.5,   # 日干剋選項=可掌控（但非最佳）
    '被剋': -3.0,   # 選項剋日干=不利=虧本
    '生':   +0.5,   # 日干生選項=付出多
    '被生': +2.0,   # 選項生日干=選項有利於求測人
}

print('\n選項評估規則（日干宮 vs 選項宮）：')
print('  比和（同宮）→ 順勢而為、榮辱與共 → 最佳選擇')
print('  日干剋選項 → 完全掌控、輕車熟路 → 可以但不最理想')
print('  選項剋日干 → 對求測人不利 → 否決')
print('  選項生日干 → 選項有利於求測人 → 好選擇')
print('  日干生選項 → 求測人付出多 → 一般')
print()

# 案例重現
print('案例重現：日干癸落坤二宮（土）')
case_options = [
    (1, '製衣生意（現有）'),
    (2, '代理水果'),
    (3, '代購網店'),
]
rigan_palace = 2  # 坤二宮

results = []
for palace, name in case_options:
    r, r2 = assess_option(palace, rigan_palace)
    # r = 選項對日干, r2 = 日干對選項
    # 師傅用日干對選項的視角
    score = OPTION_SCORE.get(r2, 0)
    results.append((palace, name, PALACE_WUXING[palace], r2, score))
    print(f'  {name}（{GONG_NAMES[palace]}{palace}宮，{PALACE_WUXING[palace]}）')
    print(f'    日干(土) vs 選項({PALACE_WUXING[palace]}): {r2} → 分數 {score:+.1f}')

print()
print('排序結果：')
results.sort(key=lambda x: x[4], reverse=True)
for i, (palace, name, wx, rel, score) in enumerate(results, 1):
    tag = '★ 首選' if i == 1 else ('✗ 否決' if score <= -2 else '○ 備選')
    print(f'  第{i}名: {name} ({rel}) {score:+.1f} {tag}')
print()

# ============================================================
# Section 3: 選項宮位符號解讀
# ============================================================
print('=' * 70)
print('Section 3: 選項宮位符號解讀（案例）')
print('=' * 70)

case_symbols = {
    1: {
        'name': '製衣生意',
        'palace': '坎一宮',
        'symbols': ['玄武', '開門', '天心星', '空亡'],
        'zuhe': ['乙+壬'],
        'analysis': (
            '玄武=表面不錯實際有問題；空亡=進入瓶頸難突破；'
            '天心星=花了不少心思經營；乙+壬=管理不好、員工認同感低、監守自盜'
        ),
    },
    2: {
        'name': '代理水果',
        'palace': '坤二宮',
        'symbols': ['值符', '景門', '天英星', '驛馬'],
        'zuhe': ['癸+辛', '癸+戊'],
        'analysis': (
            '值符=大貴人關照；驛馬=需要到處走動；天英星=脾氣急躁會犯錯誤；'
            '但值符保駕，困難都可化解'
        ),
    },
    3: {
        'name': '代購網店',
        'palace': '震三宮',
        'symbols': ['六合', '生門', '天任星'],
        'zuhe': ['丁+庚'],
        'analysis': (
            '六合=合夥經營；生門=能產生利潤；天任星=有責任心；'
            '丁+庚=工商註冊/營業牌照等法律文件會出問題，長期經營有隱憂'
        ),
    },
}

for p, info in case_symbols.items():
    print(f'\n  {info["name"]}（{info["palace"]}）')
    print(f'    符號: {"、".join(info["symbols"])}')
    print(f'    天干組合: {"、".join(info["zuhe"])}')
    print(f'    解讀: {info["analysis"]}')
print()

# ============================================================
# Section 4: 九星完整含義
# ============================================================
print('=' * 70)
print('Section 4: 九星完整含義及吉凶分類')
print('=' * 70)

JIUXING_FULL = {
    '天心星': {
        'wuxing': '金', 'natal': 6, 'nature': '吉',
        'meaning': '有心計、有領導能力',
        'meaning2': '醫療治病',
        'personality': '善於策劃、有統帥才能',
    },
    '天任星': {
        'wuxing': '土', 'natal': 8, 'nature': '吉',
        'meaning': '老實古板、任勞任怨、責任心強',
        'meaning2': None,
        'personality': '踏實可靠、但欠靈活',
    },
    '天輔星': {
        'wuxing': '木', 'natal': 4, 'nature': '吉',
        'meaning': '斯文、有學識、文化教育',
        'meaning2': '對升學考官特別有利',
        'personality': '溫和、有教養、適合文職',
    },
    '天禽星': {
        'wuxing': '土', 'natal': 5, 'nature': '吉',
        'meaning': '中正、穩重',
        'meaning2': '九五之尊（大領導）',
        'personality': '穩重中正、有威嚴',
    },
    '天蓬星': {
        'wuxing': '水', 'natal': 1, 'nature': '凶',
        'meaning': '強盜、賊人',
        'meaning2': '有冒險精神、好酒色、容易破財',
        'personality': '膽大妄為、不拘小節',
    },
    '天芮星': {
        'wuxing': '土', 'natal': 2, 'nature': '凶',
        'meaning': '疾病、傷痛、問題、隱患',
        'meaning2': '包容接納、學習授業',
        'personality': '有問題需要解決',
    },
    '天柱星': {
        'wuxing': '金', 'natal': 7, 'nature': '凶',
        'meaning': '驚恐怪異、破壞折損',
        'meaning2': '能力強、頂樑柱',
        'personality': '驚恐、破敗',
    },
    '天衝星': {
        'wuxing': '木', 'natal': 3, 'nature': '中平',
        'meaning': '衝動、有衝勁',
        'meaning2': '對紀律部隊最有利',
        'personality': '容易衝動、有行動力',
    },
    '天英星': {
        'wuxing': '火', 'natal': 9, 'nature': '中平',
        'meaning': '光明、美麗',
        'meaning2': '血光之災、性格暴躁',
        'personality': '脾氣急躁、容易發火',
    },
}

print(f'\n{"星":<8} {"五行":<4} {"本宮":<4} {"吉凶":<4} {"含義1":<25} {"含義2":<25}')
print('-' * 75)
for name, info in JIUXING_FULL.items():
    m2 = info['meaning2'] or '-'
    print(f'{name:<8} {info["wuxing"]:<4} {info["natal"]:<4} {info["nature"]:<4} {info["meaning"]:<25} {m2:<25}')

print()
print('吉凶分類：')
print('  吉星（4顆）：天心、天任、天輔、天禽')
print('  凶星（3顆）：天蓬、天芮、天柱')
print('  中平（2顆）：天衝、天英')
print()

# 與 EP01 對照
print('與 EP01 九星吉凶對照：')
print('  EP01: 天任吉、天衝吉、天輔吉、天英凶、天芮凶、天柱凶、天蓬凶、天心吉')
print('  EP09: 天心吉、天任吉、天輔吉、天禽吉、天蓬凶、天芮凶、天柱凶、天衝中平、天英中平')
print('  差異：天衝 從吉→中平，天英 從凶→中平，天禽 新增為吉')
print('  → EP09 的分類更細緻，以 EP09 為準')
print()

# ============================================================
# Section 5: 九星與性格判斷
# ============================================================
print('=' * 70)
print('Section 5: 九星與性格判斷')
print('=' * 70)

print('\n師傅教法：')
print('  天盤 = 天時 = 天空星體運動對人類的影響')
print('  人的性格和先天遺傳有關')
print('  「江山易改，秉性難移」')
print('  → 通過用神所臨的九星判斷人的個性特徵')
print()

print('案例驗證：')
print('  日干癸臨天英星 → 脾氣挺急躁、容易發火 ✅')
print('  這與 EP08 案例中天衝星=容易衝動 一致')
print()

XING_PERSONALITY = {
    '天蓬星': '膽大妄為、不拘小節、好酒色',
    '天任星': '老實古板、任勞任怨、責任心強',
    '天衝星': '衝動、有衝勁、行動力強',
    '天輔星': '斯文、有學識、溫和',
    '天英星': '脾氣急躁、容易發火',
    '天禽星': '中正穩重、有威嚴',
    '天芮星': '有問題需要解決、包容接納',
    '天柱星': '驚恐、能力強但不穩定',
    '天心星': '有心計、善策劃、有領導力',
}

print('九星性格判斷速查表：')
for star, personality in XING_PERSONALITY.items():
    nature = JIUXING_FULL[star]['nature']
    print(f'  {star}（{nature}）→ {personality}')
print()

# ============================================================
# Section 6: 天干入墓概念
# ============================================================
print('=' * 70)
print('Section 6: 天干入墓 — 首次出現')
print('=' * 70)

print('\n案例：日干癸入墓')
print('  解讀：求測人目前狀態不好，渾渾噩噩，舉棋不定')
print('  但這種情況只是暫時性的')
print('  因為她本身能力和能量都很強，適當時候會破繭而出')
print()

print('⚠️ 師傅未詳細講解入墓的計算方法')
print('   僅知道含義：渾渾噩噩、舉棋不定、暫時性的低潮')
print('   計算邏輯待後續集數補充')
print()

RUMU = {
    'meaning': '入墓=渾渾噩噩、舉棋不定',
    'nature': '暫時性的低潮，非永久',
    'case': '日干癸入墓 → 求測人狀態不好但會好返',
    'calc_method': '待補充',
}

# ============================================================
# Section 7: 新天干組合
# ============================================================
print('=' * 70)
print('Section 7: EP09 新天干組合含義')
print('=' * 70)

EP09_TIANGAN_ZUHE = {
    ('乙', '壬'): {'meaning': '管理不好、員工認同感低、監守自盜',
                   'context': '製衣生意內部管理問題', 'source': 'EP09案例'},
    ('壬', '乙'): {'meaning': '管理不好、員工認同感低、監守自盜',
                   'context': '同上', 'source': 'EP09案例'},
    ('癸', '辛'): {'meaning': '（待確認，案例未單獨解讀）',
                   'context': '代理水果生意', 'source': 'EP09案例'},
    ('辛', '癸'): {'meaning': '（待確認）',
                   'context': '同上', 'source': 'EP09案例'},
    ('癸', '戊'): {'meaning': '（待確認，案例未單獨解讀）',
                   'context': '代理水果生意', 'source': 'EP09案例'},
    ('戊', '癸'): {'meaning': '（待確認）',
                   'context': '同上', 'source': 'EP09案例'},
    ('丁', '庚'): {'meaning': '法律文件問題（工商註冊/營業牌照）',
                   'context': '代購網店的長期經營隱憂', 'source': 'EP09案例'},
    ('庚', '丁'): {'meaning': '法律文件問題',
                   'context': '同上', 'source': 'EP09案例'},
}

print('EP09 案例中新出現的天干組合：')
for (a, b), info in EP09_TIANGAN_ZUHE.items():
    if a < b or '待確認' not in info['meaning']:
        print(f'  {a}+{b}: {info["meaning"]}')
print()

# 與 EP07/EP08 格局庫對照
print('與之前集數格局庫對照：')
print('  乙+壬 → EP08=變動，EP09=管理不好/監守自盜')
print('  → 又一個矛盾！同一天干組合在不同集數有不同解讀')
print('  丁+庚 → EP07 未收錄，EP09=法律文件問題（新增）')
print('  → 可能說明：天干組合的解讀高度依賴場景')
print()

# ============================================================
# Section 8: 值符值使與決策狀態
# ============================================================
print('=' * 70)
print('Section 8: 值符值使與決策狀態')
print('=' * 70)

print('\n案例發現：')
print('  日干癸和2號選項（代理水果）同落坤二宮')
print('  而且臨值符和值使')
print('  → 說明求測人根本已經開始運作這門生意了')
print('  → 「射出去的箭已經沒法回頭」')
print()

print('洞察：')
print('  當求測人的用神宮與某個選項同宮時')
print('  表示求測人內心已經偏向這個選項')
print('  如果同時臨值符值使，更說明已經在行動中')
print('  來求測只是為自己的選擇增加信心')
print()

DECISION_STATE = {
    '同宮+值符值使': '已經開始運作，求測只是增加信心',
    '同宮': '內心已偏向，但可能未行動',
    '不同宮': '尚未做決定，真正需要幫助選擇',
}

for state, meaning in DECISION_STATE.items():
    print(f'  {state} → {meaning}')
print()

# ============================================================
# Section 9: 選項排序算法總結
# ============================================================
print('=' * 70)
print('Section 9: 選項排序算法總結')
print('=' * 70)

print('\n完整的多選項決策算法：')
print('  Step 1: 為各選項編號（1-9），對應宮位')
print('  Step 2: 找到日干落宮')
print('  Step 3: 計算日干宮 vs 各選項宮的五行關係')
print('  Step 4: 按以下優先級排序：')
print('          比和（同宮）> 選項生日干 > 日干剋選項 > 日干生選項 > 選項剋日干')
print('  Step 5: 排除選項剋日干的（否決）')
print('  Step 6: 在剩餘選項中選擇排序最高的')
print('  Step 7: 檢查首選的宮位符號，確認有無隱患')
print('  Step 8: 檢查日干是否與某選項同宮（判斷求測人是否已做決定）')
print()

# 量化為函數
print('量化函數設計：')
print('  def rank_options(qiju_result, option_names):')
print('      rigan_palace = find_rigan_palace(qiju_result)')
print('      scores = []')
print('      for i, name in enumerate(option_names, 1):')
print('          palace = i  # 編號即宮位')
print('          rel = wx_relation(PALACE_WUXING[rigan_palace], PALACE_WUXING[palace])')
print('          scores.append((name, palace, rel, OPTION_SCORE[rel]))')
print('      scores.sort(key=lambda x: x[3], reverse=True)')
print('      return scores')
print()

# ============================================================
# Section 10: 與之前集數的對照
# ============================================================
print('=' * 70)
print('Section 10: 與之前集數的對照')
print('=' * 70)

print('1. 九星吉凶（EP01）→ EP09 修正')
print('   EP01: 天衝=吉、天英=凶')
print('   EP09: 天衝=中平、天英=中平、天禽=吉（新增）')
print('   → EP09 更準確，應以 EP09 為準')
print()
print('2. 用神多面性（EP06/EP08）→ EP09 擴展')
print('   EP09 確認：同一個盤局可以同時分析多個選項')
print('   每個選項的宮位就是編號對應的宮位')
print('   → 這是全新的用神定位方法')
print()
print('3. 值符（EP05/EP06/EP08）→ EP09 第四次出現')
print('   EP05=管理層 EP06=管理層 EP08=老闆 EP09=大貴人')
print('   → 值符的核心含義是「高端/貴人」在不同場景的表現')
print()
print('4. 天干組合矛盾持續擴大')
print('   乙+壬: EP08=變動 vs EP09=管理不好')
print('   丁+壬: EP07=合格 vs EP08=產品多')
print('   → 天干組合很可能是「格局層面」和「下臨組合解讀」兩個不同系統')
print()
print('5. 空亡（EP05/EP08）→ EP09 再次出現')
print('   EP08=無法落實 EP09=進入瓶頸難突破')
print('   → 含義持續擴展中')
print()

# ============================================================
# Section 11: EP09 新發現的不足
# ============================================================
print('=' * 70)
print('Section 11: EP09 新發現的不足')
print('=' * 70)

NEW_GAPS = [
    ('G46', '高', '入墓計算未實現',
     '僅知含義（渾渾噩噩）無計算方法',
     '需找到入墓的具體計算規則（哪個天干入哪個宮的墓）'),
    ('G47', '高', '天干組合解讀系統矛盾',
     '乙+壬: EP08=變動 EP09=管理不好; 丁+壬: EP07=合格 EP08=產品多',
     '需要區分「格局」（EP07定義）和「下臨組合解讀」（案例中的用法）'),
    ('G48', '中', '多選項決策函數未實現',
     '算法已量化但無代碼',
     '需建立 rank_options(qiju_result, option_names) 函數'),
    ('G49', '中', '驛馬計算仍未實現',
     'EP06出現概念，EP09再次出現（到處走動），但仍無計算方法',
     '需找到驛馬的具體計算規則'),
    ('G50', '低', '值使含義未系統化',
     '本集出現「值符和值使」但之前主要講值符',
     '需補充值使的完整含義和計算方法'),
    ('G51', '低', '九星吉凶評分需更新',
     'EP01的分類與EP09不同',
     '以EP09為準：吉+1.5、凶-1.5、中平0'),
]

for gid, priority, name, current, expected in NEW_GAPS:
    print(f'  [{priority}] {gid}: {name}')
    print(f'       現狀: {current}')
    print(f'       期望: {expected}')
    print()

# ============================================================
# Section 12: 結論
# ============================================================
print('=' * 70)
print('Section 12: 結論')
print('=' * 70)

print('EP09 的核心貢獻：')
print('  1. 多選項決策方法：編號定位法')
print('  2. 選項評估排序算法（比和>被生>剋>生>被剋）')
print('  3. 九星完整含義及修正後的吉凶分類')
print('  4. 九星性格判斷系統（天時=先天遺傳）')
print('  5. 天干入墓概念（暫時性低潮）')
print('  6. 新天干組合（乙+壬=管理不好、丁+庚=法律文件問題）')
print('  7. 值符值使與決策狀態判斷')
print('  8. 選項宮位符號解讀（綜合門星神組合）')
print()
print('對 back test 的影響：')
print('  - 多選項決策 = 多基金/多股票比較的量化基礎')
print('  - 排序算法可以直接轉化為 ranking 特徵')
print('  - 編號定位法簡單直接，適合系統化')
print('  - 天干組合解讀矛盾需要優先解決')
print()

# ============================================================
# Section 13: JSON 輸出
# ============================================================

ep09_data = {
    "episode": 9,
    "title": "多選項投資決策 + 九星完整含義 + 天干入墓",
    "option_method": {
        "name": "編號定位法",
        "rule": "選項編號1-9直接對應宮位",
        "assessment": "日干宮 vs 各選項宮的五行生剋比和",
        "ranking": "比和 > 被生 > 剋 > 生 > 被剋",
    },
    "option_scores": OPTION_SCORE,
    "jiuxing_full": JIUXING_FULL,
    "xing_personality": XING_PERSONALITY,
    "rumu": RUMU,
    "new_tiangan_zuhe": {f"{a}+{b}": v for (a,b), v in EP09_TIANGAN_ZUHE.items()},
    "decision_state": DECISION_STATE,
    "new_gaps": [
        {"id": g[0], "priority": g[1], "name": g[2], "current": g[3], "expected": g[4]}
        for g in [
            ('G46','高','入墓計算未實現','僅知含義無計算方法','需找到入墓的具體計算規則'),
            ('G47','高','天干組合解讀系統矛盾','乙+壬和丁+壬在不同集數有不同解讀','需區分格局和下臨組合解讀'),
            ('G48','中','多選項決策函數未實現','算法已量化但無代碼','需建立rank_options函數'),
            ('G49','中','驛馬計算仍未實現','EP06/EP09出現但無計算方法','需找到驛馬的具體計算規則'),
            ('G50','低','值使含義未系統化','本集出現但之前主要講值符','需補充值使的完整含義'),
            ('G51','低','九星吉凶評分需更新','EP01與EP09分類不同','以EP09為準'),
        ]
    ],
}

output_path = '/home/z/my-project/download/ep09_multi_option.json'
with open(output_path, 'w') as f:
    json.dump(ep09_data, f, ensure_ascii=False, indent=2)
print(f'\n→ 已輸出 {output_path}')
print('\n' + '*' * 70)
print('  EP09 量化完成！')
print('*' * 70)
