#!/usr/bin/env python3
"""
EP12 量化腳本：追討欠債預測 + 伏吟局與反吟局
===================================================================

本集新知識點：
1. 追債用神系統（值符=債主、天乙=欠債人、傷門=追債人）
2. 天乙的定義與查找方法（值符落宮原地盤天星）
3. 追債成敗判斷（三用神宮生剋比和分析）
4. 伏吟局四種類型（星/門/天干/全伏吟）
5. 伏吟局含義與策略（利主不利客、被動、慢）
6. 伏吟局例外（收斂財貨有利：買入、追債）
7. 伏吟局最凶組合（天蓬+天蓬、死門+死門、庚+庚）
8. 反吟局四種類型（星/門/天干/全反吟）
9. 反吟局含義與策略（利客不利主、主動、快急動）
10. 反吟局例外（賣貨求財有利）
11. 新天干組合：己+辛（犯錯被困）、辛+戊（衝格/錢財逢衝必散）
12. 天干組合「衝格」新含義（逢衝必散）
"""

import json

PALACE_WUXING = {1:'水', 2:'土', 3:'木', 4:'木', 5:'土', 6:'金', 7:'金', 8:'土', 9:'火'}
GONG_NAMES = {1:'坎', 2:'坤', 3:'震', 4:'巽', 5:'中', 6:'乾', 7:'兌', 8:'艮', 9:'離'}
WUXING_SHENG = {"金": "水", "水": "木", "木": "火", "火": "土", "土": "金"}
WUXING_KE   = {"金": "木", "木": "土", "土": "水", "水": "火", "火": "金"}

def wx_rel(a, b):
    """五行關係：a vs b"""
    if a == b: return '比和'
    if WUXING_SHENG.get(a) == b: return f'{a}生{b}'
    if WUXING_KE.get(a) == b: return f'{a}剋{b}'
    if WUXING_SHENG.get(b) == a: return f'{b}生{a}'
    if WUXING_KE.get(b) == a: return f'{b}剋{a}'
    return '?'

# ============================================================
# Section 1: 追債用神系統
# ============================================================
print('=' * 70)
print('Section 1: 追債用神系統')
print('=' * 70)

DEBT_YONGSHEN = {
    '值符': {
        'role': '債主',
        'scope': '個人 or 公司',
        'note': '值符代表債權人，即放錢出去的一方',
    },
    '天乙': {
        'role': '欠債人',
        'scope': '個人 or 公司',
        'note': '值符所落宮位原來的地盤天星就是天乙',
    },
    '傷門': {
        'role': '追債人',
        'scope': '第三者（如討債公司）or 債主本身',
        'note': '傷門代表具體執行追債行動的人',
    },
}

print('\n追債三用神對照表：')
print(f'  {"用神":<6} {"角色":<10} {"範圍":<20} {"備註"}')
print('  ' + '-' * 60)
for k, v in DEBT_YONGSHEN.items():
    print(f'  {k:<6} {v["role"]:<10} {v["scope"]:<20} {v["note"]}')

print()

# ============================================================
# Section 2: 天乙的定義與查找
# ============================================================
print('=' * 70)
print('Section 2: 天乙的定義與查找方法')
print('=' * 70)

print('\n天乙定義：')
print('  天乙 = 值符所落宮位原來的地盤天星')
print()
print('查找步驟：')
print('  1. 找到值符落在哪一宮')
print('  2. 查看該宮原來（地盤）的天星是什麼')
print('  3. 該天星就是天乙（代表欠債人）')
print()

print('案例：')
print('  值符落震三宮')
print('  震三宮原來的天星 = 天衝星')
print('  → 天乙 = 天衝星 = 欠債人')
print()

# 九星本宮對照
JIUXING_BENGONG = {
    '天蓬星': 1, '天芮星': 2, '天衝星': 3, '天輔星': 4,
    '天禽星': 5, '天心星': 6, '天柱星': 7, '天任星': 8, '天英星': 9,
}

BENGONG_JIUXING = {v: k for k, v in JIUXING_BENGONG.items()}

print('九星本宮對照（用於查找天乙）：')
for star, palace in JIUXING_BENGONG.items():
    print(f'  {star} → {GONG_NAMES[palace]}{palace}宮')
print()

print('⚠️ 重要：天乙不是一個固定符號，而是動態計算的')
print('   每個盤局的天乙都不同，取決於值符落宮')
print()

# ============================================================
# Section 3: 追債成敗判斷方法
# ============================================================
print('=' * 70)
print('Section 3: 追債成敗判斷方法')
print('=' * 70)

print('\n核心方法：三用神宮的生剋比和分析')
print()

DEBT_ANALYSIS_FRAMEWORK = {
    'step1_zhifu': {
        'action': '分析值符宮（債主）',
        'check': '宮內符號組合 → 債主目前狀態',
    },
    'step2_tianyi': {
        'action': '分析天乙宮（欠債人）',
        'check': '宮內符號組合 → 欠債人目前狀態（特別看地盤干是否=戊=錢財）',
    },
    'step3_shangmen': {
        'action': '分析傷門宮（追債人）',
        'check': '宮內符號組合 → 追債人/公司的能力',
    },
    'step4_relations': {
        'action': '三宮五行生剋比和關係',
        'check': '值符宮 vs 天乙宮、值符宮 vs 傷門宮、天乙宮 vs 傷門宮',
    },
    'step5_auxiliary': {
        'action': '輔助分析（日干 vs 時干）',
        'check': '日干=求測人、時干=欠債人或討債這件事',
    },
}

print('追債分析五步框架：')
for step, info in DEBT_ANALYSIS_FRAMEWORK.items():
    print(f'  {info["action"]}')
    print(f'    分析: {info["check"]}')
print()

# 案例量化分析
print('案例量化分析：')
print()

case_debt = {
    'zhifu': {
        'name': '值符（債主）',
        'palace': 3, 'wuxing': '木',
        'symbols': {'門': '生門', '星': '天芮星', '天干組合': ['己+辛', '壬+辛']},
        'analysis': '生意人但生意一般，犯了錯被困惑纏繞',
    },
    'tianyi': {
        'name': '天乙（欠債人）= 天衝星',
        'palace': 6, 'wuxing': '金',
        'symbols': {'門': '驚門', '神': '六合', '其他': '驛馬'},
        'dipan_gan': '戊',
        'tiangan_zuhe': '辛+戊',
        'analysis': '人際關係好但擔驚受怕、四處走動躲避',
        'chongge': True,
        'chongge_analysis': '辛+戊=衝格（子午相衝），錢財逢衝必散，欠債人很缺錢',
    },
    'shangmen': {
        'name': '傷門（追債公司）',
        'palace': 4, 'wuxing': '木',
        'symbols': {'神': '九天', '星': '天柱星', '天干組合': '乙+庚'},
        'analysis': '正規大公司，手段乾淨利落，但乙+庚=合格，行動力不佳',
    },
}

# 五行關係計算
zhifu_wx = case_debt['zhifu']['wuxing']
tianyi_wx = case_debt['tianyi']['wuxing']
shangmen_wx = case_debt['shangmen']['wuxing']

print(f'  值符宮(震三宮) 五行={zhifu_wx}')
print(f'  天乙宮(乾六宮) 五行={tianyi_wx}')
print(f'  傷門宮(巽四宮) 五行={shangmen_wx}')
print()

r1 = wx_rel(tianyi_wx, zhifu_wx)
r2 = wx_rel(tianyi_wx, shangmen_wx)
r3 = wx_rel(zhifu_wx, shangmen_wx)

print(f'  天乙({tianyi_wx}) vs 值符({zhifu_wx}): {r1}')
print(f'    → 欠債人剋債主 → 一直不還錢，將債主拒之門外')
print()
print(f'  天乙({tianyi_wx}) vs 傷門({shangmen_wx}): {r2}')
print(f'    → 欠債人剋追債公司 → 反抗強烈，絕不合作')
print()
print(f'  值符({zhifu_wx}) vs 傷門({shangmen_wx}): {r3}')
print(f'    → 債主與追債公司比和 → 同一陣營，利益一致')
print()

# 輔助分析
print('  輔助分析（日干 vs 時干）：')
print(f'    日干乙=求測人，落巽四宮（木）')
print(f'    時干辛=欠債人/討債事，落乾六宮（金）')
print(f'    時干宮({tianyi_wx}) vs 日干宮({zhifu_wx}): {r1}')
print(f'    → 金剋木 → 欠債人不會順順當當還錢')
print()
print('  結論：追債不成功 ❌')
print('    1. 欠債人沒錢（辛+戊衝格，錢財逢衝必散）')
print('    2. 欠債人反抗強烈（天乙剋值符和傷門）')
print('    3. 追債公司行動力不佳（乙+庚合格）')
print()

# ============================================================
# Section 4: 伏吟局
# ============================================================
print('=' * 70)
print('Section 4: 伏吟局')
print('=' * 70)

print('\n定義：符號落在原來的宮位不動，痛苦地呻吟')
print()

FUYIN_TYPES = {
    '星伏吟': {
        'definition': '九星停留在九星的本宮不動',
        'example': '天心星落乾六宮、天英星落離九宮',
        'check': '每顆星是否在其本宮',
    },
    '門伏吟': {
        'definition': '八門停留在八門的本宮不動',
        'example': '休門落坎一宮、驚門落兌七宮',
        'check': '每個門是否在其本宮',
    },
    '天干伏吟': {
        'definition': '宮位裡的天盤干和地盤干完全相同',
        'example': '戊+戊、丙+丙、庚+庚',
        'check': '每宮的天盤干是否=地盤干',
    },
    '全伏吟': {
        'definition': '星伏吟+門伏吟+天干伏吟同時出現',
        'example': '整個盤局所有符號完全不動',
        'check': '以上三種同時成立',
    },
}

print('伏吟局四種類型：')
for name, info in FUYIN_TYPES.items():
    print(f'  {name}')
    print(f'    定義: {info["definition"]}')
    print(f'    例: {info["example"]}')
print()

FUYIN_RULES = {
    'general': '利主不利客',
    'duration': '持續時間比較長',
    'strategy': '被動、靜觀其變、盡量慢和遲、絕對不可急進和主動出擊',
    'prediction': '事情拖拖拉拉、進展緩慢，最後可能無疾而終',
    'exception': '收斂財貨最為有利（買入貨物、追討欠債），而且肯定會有所收穫',
    'worst': '天蓬+天蓬、死門+死門、庚+庚 → 破財或死傷',
}

print('伏吟局規則：')
for k, v in FUYIN_RULES.items():
    label = {'general':'主客', 'duration':'時間', 'strategy':'策略',
             'prediction':'預測', 'exception':'例外', 'worst':'最凶'}[k]
    print(f'  {label}: {v}')
print()

# 伏吟檢測函數邏輯
print('伏吟檢測邏輯（偽代碼）：')
print('  def detect_fuyin(pan):')
print('    star_fuyin = all(star in its_own_palace for star in jiuxing)')
print('    men_fuyin = all(men in its_own_palace for men in bamen)')
print('    gan_fuyin = all(tianpan_gan == dipan_gan for palace in palaces)')
print('    if star_fuyin and men_fuyin and gan_fuyin:')
print('      return "全伏吟"')
print('    return [type for type, detected in ... if detected]')
print()

# ============================================================
# Section 5: 反吟局
# ============================================================
print('=' * 70)
print('Section 5: 反吟局')
print('=' * 70)

print('\n定義：符號落在原來宮位的對面，形成相衝的狀態')
print()

# 對衝宮位
OPPOSITE_PALACES = {1:9, 9:1, 2:8, 8:2, 3:7, 7:3, 4:6, 6:4}

print('對衝宮位對照：')
for p1, p2 in sorted(OPPOSITE_PALACES.items()):
    if p1 < p2:
        print(f'  {GONG_NAMES[p1]}{p1}宮 ↔ {GONG_NAMES[p2]}{p2}宮')
print()

FANYIN_TYPES = {
    '星反吟': {
        'definition': '九星落在原宮位對衝的宮位',
        'example': '天蓬星落離九宮、天任星落坤二宮',
    },
    '門反吟': {
        'definition': '八門落在原宮位對衝的宮位',
        'example': '傷門落兌七宮、杜門落乾六宮',
    },
    '天干反吟': {
        'definition': '兩個對衝宮位裡天盤干和地盤干組合正好相反',
        'example': '坎一宮乙+戊、離九宮戊+乙',
    },
    '全反吟': {
        'definition': '星反吟+門反吟+天干反吟同時出現',
        'example': '整個盤局符號都在相反位置',
    },
}

print('反吟局四種類型：')
for name, info in FANYIN_TYPES.items():
    print(f'  {name}')
    print(f'    定義: {info["definition"]}')
    print(f'    例: {info["example"]}')
print()

FANYIN_RULES = {
    'general': '利客不利主',
    'duration': '持續時間比較短',
    'strategy': '主動出擊、快、急、動',
    'prediction': '事情有很大機會反覆，容易回到起點，虎頭蛇尾，有始無終',
    'exception': '賣貨求財最為有利（與伏吟相反）',
}

print('反吟局規則：')
for k, v in FANYIN_RULES.items():
    label = {'general':'主客', 'duration':'時間', 'strategy':'策略',
             'prediction':'預測', 'exception':'例外'}[k]
    print(f'  {label}: {v}')
print()

# ============================================================
# Section 6: 伏吟 vs 反吟 對照總結
# ============================================================
print('=' * 70)
print('Section 6: 伏吟 vs 反吟 對照總結')
print('=' * 70)

print(f'\n  {"維度":<12} {"伏吟":<24} {"反吟":<24}')
print('  ' + '-' * 62)
comparisons = [
    ('符號位置', '留在本宮不動', '落在對宮相衝'),
    ('主客關係', '利主不利客', '利客不利主'),
    ('持續時間', '比較長', '比較短'),
    ('行動策略', '被動、慢、靜觀其變', '主動、快、急、動'),
    ('事情特點', '拖拖拉拉、可能無疾而終', '反覆、虎頭蛇尾、有始無終'),
    ('財貨例外', '買入/追債有利', '賣貨求財有利'),
    ('吉凶判斷', '大多按凶判斷', '大多按凶判斷'),
]
for dim, fuyin, fanyin in comparisons:
    print(f'  {dim:<12} {fuyin:<24} {fanyin:<24}')

print()
print('共同點：')
print('  1. 大多數情況都按凶判斷')
print('  2. 建議遵從利主/利客原則行事')
print()

# ============================================================
# Section 7: 伏吟/反吟與主客關係
# ============================================================
print('=' * 70)
print('Section 7: 伏吟/反吟與主客關係的聯繫')
print('=' * 70)

print('\nEP11 確立的主客關係：')
print('  天盤干 = 客（主動方、外來的）')
print('  地盤干 = 主（被動方、原有的）')
print()

print('伏吟 = 天盤干=地盤干（同宮同干）→ 沒有客 → 利主')
print('  解釋：伏吟時天盤干和地盤干相同，代表「客」沒有變化')
print('  「客」不動，自然「主」佔優')
print()

print('反吟 = 符號跑到對宮 → 大幅變動 → 利客')
print('  解釋：反吟時符號劇烈變動，代表「客」在主動出擊')
print('  「客」主動，自然「客」佔優')
print()

print('⚠️ 這為伏吟/反吟的利主/利客提供了理論基礎')
print('   不只是經驗規則，而是與主客體系一脈相承')
print()

# ============================================================
# Section 8: 新天干組合
# ============================================================
print('=' * 70)
print('Section 8: EP12 新天干組合')
print('=' * 70)

EP12_ZUHE = {
    ('己', '辛'): {
        'meaning': '犯錯被困',
        'detail': '在一些事情上犯了錯，被困惑纏繞，不得安寧',
        'source': 'EP12追債案例（值符宮）',
        'type': '下臨組合解讀',
    },
    ('壬', '辛'): {
        'meaning': '（同宮出現，師傅未單獨解讀）',
        'detail': '與己+辛同在震三宮，師傅未對此組合做獨立解讀',
        'source': 'EP12追債案例（值符宮）',
        'type': '待確認',
    },
    ('辛', '戊'): {
        'meaning': '衝格（錢財逢衝必散）',
        'detail': '子午相衝形成衝格，逢衝必動、逢衝必散，錢財一衝全散',
        'source': 'EP12追債案例（天乙宮/乾六宮）',
        'type': '格局（衝格）',
    },
    ('乙', '庚'): {
        'meaning': '合格',
        'detail': '事情還沒開始就遇到合格，很難真正開展起來，行動力不佳',
        'source': 'EP12追債案例（傷門宮）',
        'type': '格局（合格）',
    },
}

print('EP12 新天干組合：')
for (a, b), info in EP12_ZUHE.items():
    print(f'  {a}+{b}: {info["meaning"]}')
    print(f'    類型: {info["type"]}')
    print(f'    詳情: {info["detail"]}')
    print(f'    來源: {info["source"]}')
    print()

# 衝格含義擴展
print('衝格含義擴展：')
print('  之前（EP01-EP10）：逢衝必動')
print('  EP12 新增：逢衝必散（特別是錢財）')
print('  → 衝格 = 動 + 散，兩層含義')
print()

# 合格含義擴展
print('合格含義更新：')
print('  之前：穩當、實在')
print('  EP12 新增：事情難以開展、行動力不佳')
print('  → 合格 = 穩定不動 = 在需要行動時反而是負面的')
print()

# ============================================================
# Section 9: 追債框架與伏吟/反吟的交叉
# ============================================================
print('=' * 70)
print('Section 9: 追債框架與伏吟/反吟的交叉應用')
print('=' * 70)

print('\n關鍵發現：伏吟局對追債最有利！')
print()
print('  伏吟 = 利主 = 被動 = 收斂財貨有利 = 追討欠債適合')
print('  → 債主是「主」（被動方，等别人還錢）')
print('  → 伏吟利主 → 對債主有利')
print('  → 但伏吟也代表拖拖拉拉 → 追債過程會慢')
print()

print('反吟局對追債的影響：')
print('  反吟 = 利客 = 主動 = 持續時間短')
print('  → 如果債主主動追債（做客）→ 反吟有利')
print('  → 但反吟容易虎頭蛇尾 → 可能追到一半放棄')
print()

print('實際應用策略：')
print('  伏吟局追債 → 慢慢來，不要急，最終會有收穫')
print('  反吟局追債 → 快速行動，但不能半途而廢')
print()

# ============================================================
# Section 10: 八門本宮對照（伏吟/反吟檢測用）
# ============================================================
print('=' * 70)
print('Section 10: 八門本宮對照（伏吟/反吟檢測基礎數據）')
print('=' * 70)

BAMEN_BENGONG = {
    '休門': 1, '死門': 2, '傷門': 3, '杜門': 4,
    # 中五宮無門
    '開門': 6, '驚門': 7, '生門': 8, '景門': 9,
}

print('\n八門本宮對照：')
print(f'  {"門":<8} {"本宮":<12} {"對宮（反吟）":<16}')
print('  ' + '-' * 38)
for men, palace in BAMEN_BENGONG.items():
    opp = OPPOSITE_PALACES.get(palace, '?')
    opp_name = GONG_NAMES.get(opp, '?') if opp != '?' else '?'
    print(f'  {men:<8} {GONG_NAMES[palace]}{palace}宮        {opp_name}{opp}宮')
print()

# 九星對宮
print('九星本宮與對宮：')
print(f'  {"星":<10} {"本宮":<12} {"對宮（反吟）":<16}')
print('  ' + '-' * 40)
for star, palace in JIUXING_BENGONG.items():
    opp = OPPOSITE_PALACES.get(palace, '?')
    opp_name = GONG_NAMES.get(opp, '?') if opp != '?' else '?'
    print(f'  {star:<10} {GONG_NAMES[palace]}{palace}宮        {opp_name}{opp}宮')
print()

# ============================================================
# Section 11: 與之前集數的對照
# ============================================================
print('=' * 70)
print('Section 11: 與之前集數的對照')
print('=' * 70)

print('1. 主客關係（EP11）→ EP12 伏吟/反吟')
print('   EP11: 天盤=客、地盤=主')
print('   EP12: 伏吟利主（不動=主佔優）、反吟利客（變動=客佔優）')
print('   ✅ 邏輯一致，主客理論可以解釋伏吟/反吟')
print()

print('2. 合格含義演變（EP07→EP12）')
print('   EP07: 合格=穩定（丁+戊、壬+丁）')
print('   EP10: 合格=穩當實在（癸+戊、戊+乙）')
print('   EP12: 合格=行動力不佳、難以開展（乙+庚）')
print('   ⚠️ 合格從純正面變為雙刃劍')
print()

print('3. 衝格含義擴展（EP01→EP12）')
print('   之前: 逢衝必動')
print('   EP12: 逢衝必散（辛+戊=錢財逢衝必散）')
print('   → 衝格=動+散')
print()

print('4. 用神多面性（EP09）→ EP12 天乙')
print('   EP09: 同一符號在不同場景有不同含義')
print('   EP12: 天乙不是固定符號，而是動態計算的用神')
print('   → 用神體系更複雜：有固定的（值符/傷門）也有動態的（天乙）')
print()

print('5. 五行生剋（全系列核心）→ EP12 再次確認')
print('   追債案例完全依賴五行生剋比和判斷')
print('   金剋木=欠債人壓制債主')
print('   ✅ 五行生剋是奇門遁甲最核心的分析工具')
print()

# ============================================================
# Section 12: EP12 新發現的不足
# ============================================================
print('=' * 70)
print('Section 12: EP12 新發現的不足')
print('=' * 70)

NEW_GAPS = [
    ('G57', '高', '伏吟/反吟自動檢測未實現',
     '已有四種類型定義和本宮對照數據，但未編寫檢測函數',
     '需在 engine.py 中實現 detect_fuyin() 和 detect_fanyin()'),
    ('G58', '高', '天乙動態查找未實現',
     '天乙=值符落宮原地盤天星，邏輯清楚但未編碼',
     '需在 engine.py 中實現 find_tianyi() 函數'),
    ('G59', '中', '伏吟/反吟與具體預測場景的整合不完整',
     '知道伏吟利追債/買入、反吟利賣貨，但其他場景未明確',
     '需建立 場景→伏吟/反吟策略 映射表'),
    ('G60', '中', '合格在「需要行動」場景下的負面含義未系統化',
     'EP12揭示合格=行動力差，但之前集數合格都是正面的',
     '需建立 合格的雙面性 規則：靜態場景=好、動態場景=差'),
    ('G61', '中', '追債框架中天干組合「衝格」的具體計算規則不明',
     '辛+戊=衝格因為「子午相衝」，但子午對應關係未解釋',
     '需找到天干與地支的對應關係以理解衝格計算'),
    ('G62', '低', '伏吟最凶組合的量化閾值未定義',
     '天蓬+天蓬、死門+死門、庚+庚=最凶，但「凶」的程度未量化',
     '可建立 FUYIN_WORST 清單和嚴重程度評分'),
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

print('EP12 的核心貢獻：')
print('  1. 追債用神系統（值符=債主、天乙=欠債人、傷門=追債人）')
print('  2. 天乙動態查找方法（值符落宮原地盤天星）')
print('  3. 追債成敗判斷框架（三用神五行生剋比和）')
print('  4. 伏吟局完整定義與規則（四種類型、利主不利客、收斂財貨例外）')
print('  5. 反吟局完整定義與規則（四種類型、利客不利主、賣貨求財例外）')
print('  6. 伏吟/反吟與主客關係的理論聯繫')
print('  7. 衝格擴展含義（逢衝必散）')
print('  8. 合格雙面性（穩定=行動力差）')
print()

print('對 backtest 的影響：')
print('  - 伏吟/反吟檢測 → 盤局分類的重要維度')
print('  - 伏吟=利主不利客 → 影響策略選擇（被動 vs 主動）')
print('  - 反吟=利客不利主 → 影響入場時機（快 vs 慢）')
print('  - 追債框架 → 可擴展為「收回資金」的一般性框架')
print('  - 天乙概念 → 動態用神查找，增加引擎複雜度')
print()

# ============================================================
# Section 14: JSON 輸出
# ============================================================

ep12_data = {
    "episode": 12,
    "title": "追討欠債預測 + 伏吟局與反吟局",
    "debt_yongshen": DEBT_YONGSHEN,
    "debt_analysis_framework": DEBT_ANALYSIS_FRAMEWORK,
    "tianyi_definition": {
        "rule": "值符所落宮位原來的地盤天星就是天乙",
        "steps": [
            "找到值符落在哪一宮",
            "查看該宮原來（地盤）的天星",
            "該天星就是天乙（代表欠債人）",
        ]
    },
    "jiuxing_bengong": JIUXING_BENGONG,
    "bamen_bengong": BAMEN_BENGONG,
    "opposite_palaces": OPPOSITE_PALACES,
    "fuyin_types": FUYIN_TYPES,
    "fuyin_rules": FUYIN_RULES,
    "fanyin_types": FANYIN_TYPES,
    "fanyin_rules": FANYIN_RULES,
    "fuyin_vs_fanyin": {
        "伏吟": {
            "符號位置": "留在本宮不動",
            "主客關係": "利主不利客",
            "持續時間": "比較長",
            "行動策略": "被動、慢、靜觀其變",
            "事情特點": "拖拖拉拉、可能無疾而終",
            "財貨例外": "買入/追債有利",
        },
        "反吟": {
            "符號位置": "落在對宮相衝",
            "主客關係": "利客不利主",
            "持續時間": "比較短",
            "行動策略": "主動、快、急、動",
            "事情特點": "反覆、虎頭蛇尾、有始無終",
            "財貨例外": "賣貨求財有利",
        },
    },
    "new_tiangan_zuhe": {
        f"{a}+{b}": {
            "meaning": v["meaning"],
            "detail": v["detail"],
            "type": v["type"],
            "source": v["source"],
        } for (a, b), v in EP12_ZUHE.items()
    },
    "case_study": {
        "zhifu_palace": 3,
        "tianyi_palace": 6,
        "shangmen_palace": 4,
        "zhifu_wuxing": zhifu_wx,
        "tianyi_wuxing": tianyi_wx,
        "shangmen_wuxing": shangmen_wx,
        "relations": {
            "天乙vs值符": r1,
            "天乙vs傷門": r2,
            "值符vs傷門": r3,
        },
        "conclusion": "追債不成功",
        "reasons": [
            "欠債人沒錢（辛+戊衝格，錢財逢衝必散）",
            "欠債人反抗強烈（天乙金剋值符木和傷門木）",
            "追債公司行動力不佳（乙+庚合格）",
        ],
    },
    "new_gaps": [
        {"id": g[0], "priority": g[1], "name": g[2], "current": g[3], "expected": g[4]}
        for g in [
            ('G57','高','伏吟/反吟自動檢測未實現','已有定義和數據但未編碼','需實現detect函數'),
            ('G58','高','天乙動態查找未實現','邏輯清楚但未編碼','需實現find_tianyi()'),
            ('G59','中','伏吟/反吟與場景整合不完整','僅知追債/買賣','需建立場景映射'),
            ('G60','中','合格雙面性未系統化','EP12揭示合格=行動力差','需建立合格雙面性規則'),
            ('G61','中','衝格計算規則不明','子午相衝對應關係未解釋','需找到天干地支對應'),
            ('G62','低','伏吟最凶組合量化閾值未定義','天蓬+天蓬等=最凶但程度未量化','可建立評分'),
        ]
    ],
}

output_path = '/home/z/my-project/download/ep12_debt_collection.json'
with open(output_path, 'w') as f:
    json.dump(ep12_data, f, ensure_ascii=False, indent=2)
print(f'\n→ 已輸出 {output_path}')
print('\n' + '*' * 70)
print('  EP12 量化完成！')
print('*' * 70)
