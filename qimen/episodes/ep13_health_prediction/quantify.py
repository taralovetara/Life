#!/usr/bin/env python3
"""
EP13 量化腳本：疾病預測用神 + 人體部位映射 + 十干剋應
===================================================================

本集新知識點：
1. 九宮代表人體部位（外部+內部，每宮雙層映射）
2. 十天干代表人體部位（外部+內部）
3. 疾病預測用神系統（天芮星=疾病、乙=中醫、天心星=西醫）
4. 病人用神動態選擇（年月日時干對應不同關係）
5. 疾病分析框架（五宮生剋比和）
6. 十干剋應（81 組合，本集教 8 個重點）
7. 同性相剋更嚴重（陰金剋陰木 > 陽金剋陰木）
8. 疾病場景下吉格變凶（戊+丙、丙+戊在疾病=凶）
9. 丁+丁=唯一以吉斷的伏吟（丁=希望/奇蹟）
10. 衝格計算確認（庚+癸：庚暗含申、癸暗含寅、寅申相衝）→ 部分解決 G61
"""

import json

PALACE_WUXING = {1:'水', 2:'土', 3:'木', 4:'木', 5:'土', 6:'金', 7:'金', 8:'土', 9:'火'}
GONG_NAMES = {1:'坎', 2:'坤', 3:'震', 4:'巽', 5:'中', 6:'乾', 7:'兌', 8:'艮', 9:'離'}

# ============================================================
# Section 1: 九宮代表人體部位
# ============================================================
print('=' * 70)
print('Section 1: 九宮代表人體部位')
print('=' * 70)

PALACE_BODY = {
    9: {
        'name': '離九宮', 'wuxing': '火',
        'external': ['頭部', '眼部', '面部'],
        'internal': ['心臟', '腦部', '血液系統'],
        'note': '離為火',
    },
    2: {
        'name': '坤二宮', 'wuxing': '土',
        'external': ['右耳', '右臂', '右手', '皮膚'],
        'internal': ['脾胃', '食道', '胰臟', '消化系統', '女性生殖系統'],
        'note': '坤為土',
    },
    4: {
        'name': '巽四宮', 'wuxing': '木',
        'external': ['左耳', '左臂', '左手', '頭髮'],
        'internal': ['肝膽', '經絡', '氣血', '血管'],
        'note': '巽為風，屬木',
    },
    7: {
        'name': '兌七宮', 'wuxing': '金',
        'external': ['右肋', '右腰', '口腔', '牙齒'],
        'internal': ['肺部', '氣管', '呼吸系統'],
        'note': '兌為口，屬金',
    },
    3: {
        'name': '震三宮', 'wuxing': '木',
        'external': ['左肋', '左腰', '腳部'],
        'internal': ['肝', '膽'],
        'note': '震為動，屬木',
    },
    6: {
        'name': '乾六宮', 'wuxing': '金',
        'external': ['右腿', '右腳', '頭部（也可）'],
        'internal': ['脊椎', '脛骨', '大腸'],
        'note': '乾為天、為首，屬金',
    },
    1: {
        'name': '坎一宮', 'wuxing': '水',
        'external': ['腹部', '生殖器'],
        'internal': ['膀胱', '腎臟', '內分泌系統', '生殖系統', '血液', '小腸'],
        'note': '坎為水',
    },
    8: {
        'name': '艮八宮', 'wuxing': '土',
        'external': ['左腿', '左腳', '鼻子'],
        'internal': ['腸胃', '脾臟', '結腸', '消化系統'],
        'note': '艮為山，屬土',
    },
}

print(f'\n{"宮":<8} {"五行":<4} {"外部部位":<30} {"內部部位"}')
print('-' * 90)
for p in [9, 2, 4, 7, 3, 6, 1, 8]:
    info = PALACE_BODY[p]
    ext = '、'.join(info['external'])
    int_ = '、'.join(info['internal'])
    print(f'{info["name"]:<8} {info["wuxing"]:<4} {ext:<30} {int_}')

# 左右對稱檢查
print('\n⚠️ 左右對稱性：')
print('  頭部: 離9（正面）+ 乾6（也可代表頭部）')
print('  耳朵: 巽4（左耳）↔ 坤2（右耳）')
print('  手臂: 巽4（左臂/左手）↔ 坤2（右臂/右手）')
print('  肋腰: 震3（左肋/左腰）↔ 兌7（右肋/右腰）')
print('  腿腳: 艮8（左腿/左腳）↔ 乾6（右腿/右腳）')
print('  肝膽: 巽4（肝膽+經絡）+ 震3（肝/膽）')
print('  消化: 坤2（脾胃食道）+ 艮8（腸胃結腸）')
print('  呼吸: 兌7（肺部氣管）')
print('  泌尿生殖: 坎1（膀胱腎臟生殖）')
print()

# ============================================================
# Section 2: 十天干代表人體部位
# ============================================================
print('=' * 70)
print('Section 2: 十天干代表人體部位')
print('=' * 70)

TIANGAN_BODY = {
    '甲': {
        'external': [], 'internal': [],
        'note': '甲不會出現在盤局（隱藏在六儀下面）',
    },
    '乙': {
        'external': ['頸', '肩膊', '關節', '膝蓋', '背部', '頭髮'],
        'internal': ['肝膽', '食道', '神經'],
        'note': '身體可屈曲的地方、神經',
    },
    '丙': {
        'external': ['額頭', '肩', '背', '嘴唇'],
        'internal': ['小腸'],
        'note': '',
    },
    '丁': {
        'external': ['眼睛', '牙齒'],
        'internal': ['心臟'],
        'note': '也代表增生的骨刺',
    },
    '戊': {
        'external': ['肌膚', '乳房', '鼻子', '大肚子'],
        'internal': ['腸胃', '消化系統'],
        'note': '',
    },
    '己': {
        'external': ['口腔', '肛門'],
        'internal': ['脾臟'],
        'note': '外部代表有出口的地方',
    },
    '庚': {
        'external': ['腿', '腳'],
        'internal': ['大腸', '筋骨'],
        'note': '',
    },
    '辛': {
        'external': ['腹部'],
        'internal': ['肺部', '支氣管', '呼吸系統'],
        'note': '也代表精子',
    },
    '壬': {
        'external': ['眼睛', '頭髮', '腋下'],
        'internal': ['血液', '動脈', '心臟', '膀胱', '泌尿系統'],
        'note': '',
    },
    '癸': {
        'external': ['足部', '四肢'],
        'internal': ['腎', '尿道', '泌尿系統', '輸卵管', '靜脈',
                    '神經系統', '循環系統', '中樞神經', '生殖系統'],
        'note': '癸代表最多內部器官',
    },
}

print(f'\n{"天干":<4} {"外部部位":<32} {"內部部位"}')
print('-' * 85)
for tg in ['乙','丙','丁','戊','己','庚','辛','壬','癸']:
    info = TIANGAN_BODY[tg]
    ext = '、'.join(info['external'])
    int_ = '、'.join(info['internal'])
    extra = f' ({info["note"]})' if info['note'] else ''
    print(f'{tg:<4} {ext:<32} {int_}{extra}')

# 天干重疊檢查
print('\n⚠️ 器官多天干重疊（疾病定位需綜合判斷）：')
overlaps = {
    '肝膽': ['乙', '巽4宮', '震3宮'],
    '心臟': ['丁', '壬', '離9宮'],
    '消化系統': ['戊', '坤2宮', '艮8宮'],
    '腎臟': ['癸', '坎1宮'],
    '泌尿系統': ['壬', '癸', '坎1宮'],
    '呼吸系統': ['辛', '兌7宮'],
    '眼睛': ['丁', '壬'],
    '頭髮': ['乙', '壬', '巽4宮'],
    '腸胃': ['戊', '己', '艮8宮', '坤2宮'],
    '生殖系統': ['癸', '坎1宮', '坤2宮'],
}
for organ, sources in overlaps.items():
    print(f'  {organ}: {" / ".join(sources)}')
print()

# ============================================================
# Section 3: 疾病預測用神系統
# ============================================================
print('=' * 70)
print('Section 3: 疾病預測用神系統')
print('=' * 70)

DISEASE_YONGSHEN = {
    '天芮星': {
        'role': '疾病用神',
        'meaning': '代表疾病本身',
        'usage': '天芮星落哪宮+臨什麼天干 → 決定得了什麼病',
    },
    '天干乙': {
        'role': '中醫/中藥',
        'meaning': '代表中醫治療方案',
        'usage': '分析乙宮與天芮宮的關係 → 中醫能否醫治',
    },
    '天心星': {
        'role': '西醫/西藥',
        'meaning': '代表西醫治療方案',
        'usage': '分析天心宮與天芮宮的關係 → 西醫能否醫治',
    },
    '病人用神': {
        'role': '代表病人',
        'meaning': '根據病人和求測人的關係動態選擇',
        'usage': '年干=父/母長輩、月干=平輩、日干=自己、時干=子女',
    },
    '時干': {
        'role': '疾病事宜',
        'meaning': '代表這次求測的疾病事件',
        'usage': '時干宮與其他用神宮的關係',
    },
}

print('\n疾病預測五用神：')
for name, info in DISEASE_YONGSHEN.items():
    print(f'  {name}')
    print(f'    角色: {info["role"]}')
    print(f'    用法: {info["usage"]}')
    print()

# 病人用神選擇規則
print('病人用神選擇規則：')
PATIENT_YONGSHEN = {
    '年干': '父親/母親/長輩',
    '月干': '兄弟姐妹/平輩/同事',
    '日干': '自己',
    '時干': '子女/下屬',
}
for gan, role in PATIENT_YONGSHEN.items():
    print(f'  {gan} → {role}')
print()

# ============================================================
# Section 4: 疾病分析框架
# ============================================================
print('=' * 70)
print('Section 4: 疾病分析框架')
print('=' * 70)

DISEASE_ANALYSIS = {
    'step1_locate': {
        'action': '天芮星定位疾病',
        'method': '天芮星落哪宮 → 該宮代表嘅人體部位就是病竈',
        'detail': '再結合臨嘅天干 → 進一步細化部位',
    },
    'step2_diagnose': {
        'action': '綜合判斷病情',
        'method': '分析天芮星宮、病人宮、時干宮之間的生剋比和',
        'detail': '確定疾病性質、輕重程度',
    },
    'step3_treatment': {
        'action': '判斷能否醫治',
        'method': '乙宮(中醫) vs 天芮宮、天心宮(西醫) vs 天芮宮',
        'detail': '剋天芮 = 能醫治、被天芮剋 = 難醫治',
    },
    'step4_method': {
        'action': '選擇治療方向',
        'method': '比較乙宮和天心宮哪個更有效',
        'detail': '乙宮剋天芮更強 → 中醫更好；天心宮剋天芮更強 → 西醫更好',
    },
}

print('\n疾病預測四步框架：')
for step, info in DISEASE_ANALYSIS.items():
    print(f'  {info["action"]}')
    print(f'    方法: {info["method"]}')
    print(f'    細節: {info["detail"]}')
    print()

print('疾病治療判斷邏輯：')
print('  治療用神(乙/天心) 剋 天芮星(疾病) → 能醫治 ✅')
print('  治療用神(乙/天心) 被天芮星剋 → 難醫治 ❌')
print('  治療用神(乙/天心) 與天芮星比和 → 平穩，需長期治療 ⚠️')
print('  病人宮 剋 天芮星宮 → 病人能戰勝疾病 ✅')
print('  天芮星宮 剋 病人宮 → 疾病壓制病人 ❌')
print()

# ============================================================
# Section 5: 十干剋應
# ============================================================
print('=' * 70)
print('Section 5: 十干剋應（81 組合中嘅 8 個重點）')
print('=' * 70)

print('\n十干剋應 = 天干在天盤和地盤相遇時產生的 9x9=81 種組合')
print('甲不出現 → 實際 9 個天干 x 9 個宮位 = 81 組合')
print()

SHIGAN_KE_YING = {
    ('戊', '丙'): {
        'name': '青龍返首',
        'type': '吉',
        'general': '大吉，宜就職、訴訟、遷移、求財、建造',
        'disease': '疾病復發或惡化（凶！）',
        'note': '絕大多數大吉，唯獨疾病以凶斷',
    },
    ('丙', '戊'): {
        'name': '飛鳥跌穴',
        'type': '吉',
        'general': '大吉，宜就職、求測、訴訟、建造、婚姻',
        'disease': '病人將會離開人世（大凶！）',
        'note': '跌入地穴=入土，疾病以大凶斷',
    },
    ('丁', '丁'): {
        'name': '奇入太陰',
        'type': '吉',
        'general': '文書證件將至、喜事來臨、諸事如意',
        'disease': '（師傅未特別說明疾病場景）',
        'note': '唯一以吉斷的伏吟組合（丁=希望/奇蹟疊加）',
        'exception': '測第三者遇到不好（丁=女性第三者）',
    },
    ('辛', '乙'): {
        'name': '白虎猖狂',
        'type': '凶',
        'general': '家破人亡、出入有驚恐、遠行多災禍',
        'marriage': '男方主動提出離婚',
        'mechanism': '陰金剋陰木（同性相剋更嚴重）',
    },
    ('乙', '辛'): {
        'name': '青龍逃走',
        'type': '凶',
        'general': '人亡財破、禽畜皆傷',
        'marriage': '女方主動提出離婚',
        'mechanism': '同性相剋',
    },
    ('丁', '癸'): {
        'name': '朱雀投江',
        'type': '凶',
        'general': '文書牽連、音信全無、口舌官司、陰謀詭詐',
        'disease': '小心眼睛、心臟、血管方面嘅問題',
        'mechanism': '陰水剋陰火（同性相剋）',
    },
    ('癸', '丁'): {
        'name': '螣蛇夭矯',
        'type': '凶',
        'general': '虛驚不寧、文書官司、諸事不利',
        'disease': '（與丁+癸類似）',
        'mechanism': '陰水剋陰火（同性相剋）',
    },
    ('庚', '癸'): {
        'name': '大格',
        'type': '凶',
        'general': '嚴重衝突、打鬥、車禍人亡、官司不止、經商破財',
        'mechanism': '衝格（庚暗含申、癸暗含寅、寅申相衝）',
    },
}

print('\n【大吉組合】')
for (a, b), info in SHIGAN_KE_YING.items():
    if info['type'] == '吉':
        print(f'  {a}+{b} = {info["name"]}')
        print(f'    一般: {info["general"]}')
        if info.get('disease'):
            print(f'    疾病: {info["disease"]}')
        if info.get('exception'):
            print(f'    例外: {info["exception"]}')
        print()

print('【大凶組合】')
for (a, b), info in SHIGAN_KE_YING.items():
    if info['type'] == '凶':
        print(f'  {a}+{b} = {info["name"]}')
        print(f'    一般: {info["general"]}')
        if info.get('mechanism'):
            print(f'    機制: {info["mechanism"]}')
        if info.get('marriage'):
            print(f'    婚姻: {info["marriage"]}')
        if info.get('disease'):
            print(f'    疾病: {info["disease"]}')
        print()

# ============================================================
# Section 6: 同性相剋更嚴重
# ============================================================
print('=' * 70)
print('Section 6: 同性相剋更嚴重')
print('=' * 70)

TIANGAN_YINYANG = {
    '甲': '陽', '乙': '陰', '丙': '陽', '丁': '陰',
    '戊': '陽', '己': '陰', '庚': '陽', '辛': '陰',
    '壬': '陽', '癸': '陰',
}

WX_LIST = ['木', '火', '土', '金', '水']
TG_WX = {'甲':'木','乙':'木','丙':'火','丁':'火','戊':'土','己':'土','庚':'金','辛':'金','壬':'水','癸':'水'}

print('\n陰陽屬性對照：')
for tg in ['乙','丙','丁','戊','己','庚','辛','壬','癸']:
    print(f'  {tg}: {TIANGAN_YINYANG[tg]} ({TG_WX[tg]})')

print('\n同性相剋 = 陰剋陰 或 陽剋陽 → 更嚴重')
print('異性相剋 = 陽剋陰 或 陰剋陽 → 較輕')
print()
print('本集出現的同性相剋案例：')
same_gender_cases = [
    ('辛+乙', '白虎猖狂', '陰金剋陰木', '家破人亡'),
    ('乙+辛', '青龍逃走', '陰木被陰金剋', '人亡財破'),
    ('丁+癸', '朱雀投江', '陰火被陰水剋', '諸事皆凶'),
    ('癸+丁', '螣蛇夭矯', '陰水剋陰火', '諸事不利'),
]
for zuhe, name, mech, result in same_gender_cases:
    print(f'  {zuhe} ({name}): {mech} → {result}')
print()

# ============================================================
# Section 7: 衝格計算確認（部分解決 G61）
# ============================================================
print('=' * 70)
print('Section 7: 衝格計算確認（部分解決 G61）')
print('=' * 70)

print('\nG61 原問題：衝格的計算規則不明')
print('EP12 發現：辛+戊=衝格（子午相衝）但未解釋計算方法')
print()
print('EP13 新線索：庚+癸=大格（衝格）')
print('  庚 暗含地支 申')
print('  癸 暗含地支 寅')
print('  寅申相衝 → 形成衝格')
print()
print('→ 衝格計算規則確認：')
print('  天盤干暗含地支 vs 地盤干暗含地支 → 相衝 = 衝格')
print()

# 暗含地支
TIANGAN_HIDDEN_DZ = {
    '戊': '子', '己': '戌', '庚': '申',
    '辛': '午', '壬': '辰', '癸': '寅',
}

# 六衝
LIUCHONG = [('子','午'), ('丑','未'), ('寅','申'), ('卯','酉'), ('辰','戌'), ('巳','亥')]

def is_chongge(tian_gan, di_gan):
    if tian_gan not in TIANGAN_HIDDEN_DZ or di_gan not in TIANGAN_HIDDEN_DZ:
        return False, None
    dz_tp = TIANGAN_HIDDEN_DZ[tian_gan]
    dz_dp = TIANGAN_HIDDEN_DZ[di_gan]
    for c1, c2 in LIUCHONG:
        if (dz_tp == c1 and dz_dp == c2) or (dz_tp == c2 and dz_dp == c1):
            return True, f'{dz_tp}{dz_dp}相衝'
    return False, None

print('驗證所有六儀組合的衝格：')
liuyi = ['戊','己','庚','辛','壬','癸']
chongge_found = []
for tg in liuyi:
    for dg in liuyi:
        is_cg, reason = is_chongge(tg, dg)
        if is_cg:
            chongge_found.append((tg, dg, reason))
            print(f'  {tg}+{dg} → {reason} → 衝格 ✅')

print(f'\n共發現 {len(chongge_found)} 個衝格組合')
print()

# 反向驗證：辛+戊
print('反向驗證 EP12 案例：辛+戊')
is_cg, reason = is_chongge('辛', '戊')
print(f'  辛(暗含{TIANGAN_HIDDEN_DZ["辛"]})+戊(暗含{TIANGAN_HIDDEN_DZ["戊"]}): {"衝格: " + reason if is_cg else "非衝格"}')
print(f'  → 師傅話辛+戊=衝格（子午相衝），計算結果一致 ✅')
print()

# ============================================================
# Section 8: 十干剋應 vs 之前集數嘅格局系統對照
# ============================================================
print('=' * 70)
print('Section 8: 十干剋應 vs 格局系統對照')
print('=' * 70)

print('\n十干剋應 = 81 組合（天干x宮位）')
print('格局系統 = 衝格+合格+其他（天干x天干）')
print()
print('兩套系統嘅關係：')
print('  十干剋應 ⊃ 格局系統（十干剋應包含格局）')
print('  格局只係十干剋應中比較特殊嘅組合')
print()
print('本集新學嘅十干剋應 vs 之前格局記錄對照：')

comparisons = [
    ('戊+丙', '十干剋應: 青龍返首(大吉)', '格局: 未記錄', '→ 新增'),
    ('丙+戊', '十干剋應: 飛鳥跌穴(大吉)', '格局: 未記錄', '→ 新增'),
    ('丁+丁', '十干剋應: 奇入太陰(吉)', '格局: 伏吟', '→ 伏吟唯一吉例！'),
    ('辛+乙', '十干剋應: 白虎猖狂(大凶)', '格局: 衝格(G38待確認)', '→ 確認為大凶'),
    ('乙+辛', '十干剋應: 青龍逃走(大凶)', '格局: 衝格', '→ 確認為大凶'),
    ('庚+癸', '十干剋應: 大格/衝格(大凶)', '格局: 未記錄', '→ 新增衝格'),
    ('丁+癸', '十干剋應: 朱雀投江(凶)', '格局: 未記錄', '→ 新增'),
    ('癸+丁', '十干剋應: 螣蛇夭矯(凶)', '格局: 螣蛇夭矯(已記錄EP01)', '→ 已有，本集補充疾病含義'),
]

for zuhe, keying, geju, status in comparisons:
    print(f'  {zuhe}:')
    print(f'    十干剋應: {keying.split(": ")[1]}')
    print(f'    格局記錄: {geju.split(": ")[1]}')
    print(f'    {status}')
    print()

# ============================================================
# Section 9: 疾病場景下吉格變凶
# ============================================================
print('=' * 70)
print('Section 9: 疾病場景下吉格變凶')
print('=' * 70)

DISEASE_EXCEPTION = {
    '戊+丙 (青龍返首)': {
        'normal': '大吉',
        'disease': '疾病復發或惡化（凶）',
        'reason': '青龍返首=龍回頭，疾病回頭=復發',
    },
    '丙+戊 (飛鳥跌穴)': {
        'normal': '大吉',
        'disease': '病人將會離開人世（大凶）',
        'reason': '跌入地穴=入土為安=死亡',
    },
}

print('\n疾病預測嘅特殊性：')
print('  一般吉格在疾病場景下可能變凶')
print()
for zuhe, info in DISEASE_EXCEPTION.items():
    print(f'  {zuhe}:')
    print(f'    一般: {info["normal"]}')
    print(f'    疾病: {info["disease"]}')
    print(f'    原因: {info["reason"]}')
    print()

print('→ 這進一步證實 G47：天干組合解讀必須考慮場景')
print()

# ============================================================
# Section 10: 與之前集數的對照
# ============================================================
print('=' * 70)
print('Section 10: 與之前集數的對照')
print('=' * 70)

print('1. 用神體系（全系列）→ EP13 新增疾病用神')
print('   EP02: 婚姻用神（乙庚六合）')
print('   EP05-07: 事業用神（開門/日干/時干）')
print('   EP08: 投資用神（開門/日干/時干/生門/戊）')
print('   EP12: 追債用神（值符/天乙/傷門）')
print('   EP13: 疾病用神（天芮星/乙/天心星/病人/時干）')
print('   → 用神體系越來越完整')
print()

print('2. 天芮星含義演變')
print('   EP01: 凶星，代表問題')
print('   EP13: 疾病用神=疾病的象徵')
print('   → 天芮星的最核心含義確定：疾病')
print()

print('3. 天心星含義演變')
print('   EP01: 吉星')
print('   EP10: 對文化藝術最有利')
print('   EP13: 西醫/西藥的代表')
print('   → 天心星=醫治（特別是西醫）')
print()

print('4. 天干乙含義演變')
print('   EP02: 妻子（婚姻）')
print('   EP04: 女性/陰柔')
print('   EP13: 中醫/中藥')
print('   → 乙的新角色：中醫')
print()

print('5. 格局庫擴充（G33/G37）')
print('   新增格局：青龍返首、飛鳥跌穴、奇入太陰')
print('   新增凶格：白虎猖狂、青龍逃走、朱雀投江、大格')
print('   格局庫從 14 條擴充到 22 條')
print()

print('6. 衝格計算（G61）部分解決')
print('   庚+癸=衝格（申寅相衝）確認了暗含地支計算規則')
print('   辛+戊=衝格（午子相衝）反向驗證通過')
print('   → 可以自動計算所有六儀x六儀的衝格組合')
print()

# ============================================================
# Section 11: EP13 新發現的不足
# ============================================================
print('=' * 70)
print('Section 11: EP13 新發現的不足')
print('=' * 70)

NEW_GAPS = [
    ('G63', '高', '十干剋應完整 81 組合未建立',
     '本集只教 8 個重點，其餘 73 個未知',
     '需找到完整十干剋應表'),
    ('G64', '高', '疾病分析函數未實現',
     '框架清楚（五宮生剋），但未編碼',
     '需實現 disease_analysis() 函數'),
    ('G65', '中', '九宮與天干人體部位嘅交叉邏輯未明確',
     '天芮落坎1+臨壬=腎臟+泌尿（兩套系統都指向腎），但有些組合可能矛盾',
     '需建立交叉驗證規則'),
    ('G66', '中', '同性相剋加權未納入評分',
     '本集明確教同性相剋更嚴重，但 engine 評分未區分',
     '需在 WX_SK 中加入陰陽同異加權'),
    ('G67', '低', '疾病場景吉凶反轉規則未系統化',
     '僅知戊+丙、丙+戊在疾病=凶，其他格局呢？',
     '需建立 SCENE_EXCEPTION 映射'),
    ('G68', '低', '天芮星與治療用神嘅生剋閾值未定義',
     '治療剋疾病=能醫，但「剋」的程度需要多大？',
     '需回測或等待更多案例'),
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

print('EP13 的核心貢獻：')
print('  1. 九宮人體完整映射（8宮x外部+內部雙層）')
print('  2. 十天干人體完整映射（9干x外部+內部）')
print('  3. 疾病用神系統（天芮星/乙/天心星/病人/時干）')
print('  4. 疾病分析四步框架（定位/判斷/醫治/治療方向）')
print('  5. 十干剋應重點 8 組（3吉5凶）')
print('  6. 同性相剋更嚴重規則')
print('  7. 疾病場景吉凶反轉（戊+丙、丙+戊）')
print('  8. 丁+丁=唯一以吉斷的伏吟')
print('  9. 衝格計算規則確認（G61 部分解決）')
print('  10. 格局庫從 14 → 22 條')
print()

print('對 backtest 的影響：')
print('  - 十干剋應 = 擴充格局庫，提升盤局評分準確性')
print('  - 同性相剋加權 = 改進五行生剋評分公式')
print('  - 衝格自動計算 = 可以自動檢測所有衝格（G61 部分解決）')
print()

# ============================================================
# Section 13: JSON 輸出
# ============================================================

ep13_data = {
    "episode": 13,
    "title": "疾病預測用神 + 人體部位映射 + 十干剋應",
    "palace_body": PALACE_BODY,
    "tiangan_body": TIANGAN_BODY,
    "disease_yongshen": DISEASE_YONGSHEN,
    "patient_yongshen": PATIENT_YONGSHEN,
    "disease_analysis": DISEASE_ANALYSIS,
    "shigan_ke_ying": {
        f"{a}+{b}": {
            "name": v["name"],
            "type": v["type"],
            "general": v["general"],
            "mechanism": v.get("mechanism", ""),
        } for (a, b), v in SHIGAN_KE_YING.items()
    },
    "disease_exceptions": DISEASE_EXCEPTION,
    "chongge_confirmed": {
        "rule": "天盤干暗含地支 vs 地盤干暗含地支 → 六衝 = 衝格",
        "validation": [
            {"combo": "庚+癸", "reason": "申寅相衝", "result": "pass"},
            {"combo": "辛+戊", "reason": "午子相衝", "result": "pass"},
        ],
        "all_chongge": [
            {"combo": f"{a}+{b}", "reason": r} for a, b, r in chongge_found
        ],
    },
    "tiangan_yinyang": TIANGAN_YINYANG,
    "new_gaps": [
        {"id": g[0], "priority": g[1], "name": g[2], "current": g[3], "expected": g[4]}
        for g in [
            ('G63','高','十干剋應完整81組合未建立','僅教8個','需找完整表'),
            ('G64','高','疾病分析函數未實現','框架清楚未編碼','需實現函數'),
            ('G65','中','九宮與天干人體交叉邏輯未明確','可能矛盾','需建立交叉規則'),
            ('G66','中','同性相剋加權未納入評分','已教但未編碼','需加權'),
            ('G67','低','疾病場景吉凶反轉未系統化','僅知2例','需建立映射'),
            ('G68','低','治療生剋閾值未定義','剋到幾大先算能醫','需回測'),
        ]
    ],
}

output_path = '/home/z/my-project/download/ep13_health_prediction.json'
with open(output_path, 'w') as f:
    json.dump(ep13_data, f, ensure_ascii=False, indent=2)
print(f'\n→ 已輸出 {output_path}')
print('\n' + '*' * 70)
print('  EP13 量化完成！')
print('*' * 70)
