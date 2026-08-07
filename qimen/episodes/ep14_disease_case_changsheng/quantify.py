#!/usr/bin/env python3
"""
EP14 量化腳本：疾病預測案例方法論 + 十二長生狀態
===================================================================

本集新知識點：
1. 疾病案例分析方法論（天芮星定位+多宮交叉分析）
2. 久病逢衝=大凶（天干暗含地支 vs 落宮地支相衝）
3. 帝旺在老人=迴光反照=大凶
4. 九天+空亡=死亡徵兆組合
5. 坤二宮=母親（家庭角色用神）
6. 天干庚=大凶符號（血光之災/不治之症）
7. 十二長生完整數據表（10干x12狀態x宮位）
8. 陽干順時針/陰干逆時針排列規則
9. 陰陽互為生死位置規律
10. 旺弱判斷標準（3旺9弱）+ 入墓=最差
11. 實際應用策略（帝旺全力進取、衰弱暫時忍耐）
"""

import json

PALACE_WUXING = {1:'水', 2:'土', 3:'木', 4:'木', 5:'土', 6:'金', 7:'金', 8:'土', 9:'火'}
GONG_NAMES = {1:'坎', 2:'坤', 3:'震', 4:'巽', 5:'中', 6:'乾', 7:'兌', 8:'艮', 9:'離'}
WUXING_SHENG = {"金": "水", "水": "木", "木": "火", "火": "土", "土": "金"}
WUXING_KE   = {"金": "木", "木": "土", "土": "水", "水": "火", "火": "金"}

# ============================================================
# Section 1: 疾病案例方法論（老太太心血管案例）
# ============================================================
print('=' * 70)
print('Section 1: 疾病案例方法論')
print('=' * 70)

CASE_STUDY = {
    'background': '老太太長期生病，時好時壞，最近反覆，前兩天緊急入院',
    'question': '母親病情吉凶',
    'yongshen_selected': {
        '病人': '年干戊（問母親=長輩→年干）',
        '疾病': '天芮星',
        '中醫': '天干乙',
        '西醫': '天心星',
    },
}

# 1a. 天芮星落宮定位疾病
TIARUI_ANALYSIS = {
    'palace': 9,
    'palace_name': '離九宮',
    'wuxing': '火',
    'symbols': ['九天', '傷門', '空亡', '丁+壬', '戊+壬'],
    'body_parts_palace': ['頭部', '心臟', '腦部'],
    'tiangan_clues': {
        '丁': ['心臟', '眼睛'],
        '壬': ['血液', '動脈'],
        '戊': ['堵塞', '障礙物'],
    },
    'zuhe_clues': {
        '丁+壬': '合格→數量多、時間長（多種疾病併發）',
        '戊+壬': '堵塞+血液→血管堵塞',
    },
    'men_clue': '傷門=受傷/傷口→已接受手術但效果不理想',
    'diagnosis': '心腦血管疾病為主，腦部血管堵塞，心臟血管栓塞，併發症影響眼睛',
}

print('\n案例背景：', CASE_STUDY['background'])
print('求測問題：', CASE_STUDY['question'])
print()

print('1a. 天芮星落宮定位疾病：')
print(f'  天芮星落{TIARUI_ANALYSIS["palace_name"]}（{TIARUI_ANALYSIS["wuxing"]}）')
print(f'  臨：{"、".join(TIARUI_ANALYSIS["symbols"])}')
print(f'  宮位人體：{"、".join(TIARUI_ANALYSIS["body_parts_palace"])}')
print(f'  天干線索：')
for tg, parts in TIARUI_ANALYSIS['tiangan_clues'].items():
    print(f'    {tg} → {"、".join(parts)}')
print(f'  組合線索：')
for zuhe, meaning in TIARUI_ANALYSIS['zuhe_clues'].items():
    print(f'    {zuhe} → {meaning}')
print(f'  {TIARUI_ANALYSIS["men_clue"]}')
print(f'  → 診斷：{TIARUI_ANALYSIS["diagnosis"]}')
print()

# 1b. 年干確認生病狀態
print('1b. 年干確認生病狀態：')
print('  年干戊 落離九宮 → 與天芮星同宮')
print('  → 確認老太太正處於生病狀態')
print()

# 1c. 帝旺在老人=迴光反照
print('1c. 帝旺在老人 = 迴光反照（重大新規則）：')
print('  天干戊在離九宮屬於帝旺')
print('  帝旺 = 狀態非常旺盛，已達最高點')
print('  ⚠️ 老人處於極旺狀態不是好事')
print('  原因：極旺之後很快變差，而且會越來越差')
print('  → 迴光反照的徵兆')
print('  → 病情發展極為不樂觀')
print()

# 1d. 久病逢衝=大凶
TIANGAN_HIDDEN_DZ = {
    '戊': '子', '己': '戌', '庚': '申',
    '辛': '午', '壬': '辰', '癸': '寅',
}
PALACE_DIZHI = {
    1: ['子'], 2: ['未','申'], 3: ['卯'], 4: ['辰','巳'],
    5: [], 6: ['戌','亥'], 7: ['酉'], 8: ['丑','寅'], 9: ['午'],
}
LIUCHONG = [('子','午'), ('丑','未'), ('寅','申'), ('卯','酉'), ('辰','戌'), ('巳','亥')]

def check_palace_chong(tiangan, palace):
    """檢查天干暗含地支是否與落宮地支相衝"""
    if tiangan not in TIANGAN_HIDDEN_DZ:
        return False, None
    tg_dz = TIANGAN_HIDDEN_DZ[tiangan]
    for pdz in PALACE_DIZHI.get(palace, []):
        for c1, c2 in LIUCHONG:
            if (tg_dz == c1 and pdz == c2) or (tg_dz == c2 and pdz == c1):
                return True, f'{tg_dz}{pdz}相衝'
    return False, None

print('1d. 久病逢衝 = 大凶（重大新規則）：')
is_chong, reason = check_palace_chong('戊', 9)
print(f'  天干戊 暗含地支 {TIANGAN_HIDDEN_DZ["戊"]}')
print(f'  離九宮 包含地支 {"、".join(PALACE_DIZHI[9])}')
print(f'  → {reason if is_chong else "非衝"} → {"逢衝必動，久病逢衝容易出大問題，以大凶斷" if is_chong else "-"}')
print()

# 1e. 九天+空亡 = 死亡徵兆
print('1e. 九天 + 空亡 = 死亡徵兆組合：')
DEATH_OMENS = {
    '九天': '飛上天、升天 → 死亡隱喻',
    '空亡': '缺失、不存在 → 消失隱喻',
    'combination': '九天+空亡同宮 → 時間不多了',
}
for sym, meaning in DEATH_OMENS.items():
    print(f'  {sym}: {meaning}')
print()

# 1f. 坤二宮也代表母親
print('1f. 坤二宮 = 母親（家庭角色用神新規則）：')
print('  問母親病情 → 除了看年干，還要看坤二宮')
print('  坤二宮臨值符 → 本來相當好')
print('  但宮裡有天干庚 → 非常不好')
print('    庚 = 大凶符號')
print('    不是血光之災，就是不治之症')
print('  坤二宮也臨空亡 → 缺失/不存在')
print('  → 綜合判斷：很難跨過這道坎，最多不超過半年')
print()

# 1g. 治療判斷
print('1g. 治療效果判斷（驗證 EP13 框架）：')
print('  乙(中醫)落震三宮(木)，生天芮離九宮(火)')
print('    → 木生火 → 中醫生疾病 → 無法抑制')
print('  天心星(西醫)落兌七宮(金)，被天芮離九宮(火)剋')
print('    → 火剋金 → 疾病剋西醫 → 完全無效')
print('  → 無論中醫西醫都沒辦法醫治')
print()

# ============================================================
# Section 2: 疾病案例總結的規則
# ============================================================
print('=' * 70)
print('Section 2: 疾病案例總結的規則')
print('=' * 70)

DISEASE_RULES = {
    'R01': {
        'name': '多天干同宮=多種疾病併發',
        'condition': '天芮星宮有多個天干',
        'judgment': '每個天干對應不同器官/疾病',
        'source': 'EP14 案例（丁+壬+戊同宮）',
    },
    'R02': {
        'name': '合格(丁+壬)在疾病=數量多時間長',
        'condition': '天芮宮臨合格',
        'judgment': '疾病種類多、持續時間長',
        'source': 'EP14 案例',
    },
    'R03': {
        'name': '傷門在手術場景=已接受手術',
        'condition': '天芮宮或病人宮臨傷門',
        'judgment': '已接受過手術/有傷口',
        'source': 'EP14 案例',
    },
    'R04': {
        'name': '帝旺+老人=迴光反照=大凶',
        'condition': '病人用神處於帝旺狀態',
        'judgment': '極旺之後快變差，病情極不樂觀',
        'source': 'EP14 案例（年干戊帝旺）',
    },
    'R05': {
        'name': '久病逢衝=大凶',
        'condition': '病人用神暗含地支與落宮地支相衝',
        'judgment': '逢衝必動，久病逢衝容易出大問題',
        'source': 'EP14 案例（戊子落離九午→子午相衝）',
    },
    'R06': {
        'name': '九天+空亡=死亡徵兆',
        'condition': '天芮宮或病人宮同時臨九天和空亡',
        'judgment': '時間不多了，飛升+消失',
        'source': 'EP14 案例',
    },
    'R07': {
        'name': '坤二宮=母親',
        'condition': '問母親/女性長輩',
        'judgment': '除了年干外，也要看坤二宮',
        'source': 'EP14 案例',
    },
    'R08': {
        'name': '天干庚=大凶符號',
        'condition': '病人宮或母親宮臨庚',
        'judgment': '血光之災或不治之症',
        'source': 'EP14 案例（坤二宮臨庚）',
    },
    'R09': {
        'name': '治療生剋判斷',
        'condition': '分析乙宮/天心宮與天芮宮的五行關係',
        'judgment': '治療剋疾病=能醫、被剋=無效、生疾病=加重',
        'source': 'EP14 案例（乙生天芮=無法抑制、天心被天芮剋=完全無效）',
    },
}

print('\nEP14 新增疾病預測規則：')
for rid, rule in DISEASE_RULES.items():
    print(f'  {rid}: {rule["name"]}')
    print(f'       條件: {rule["condition"]}')
    print(f'       判斷: {rule["judgment"]}')
    print()

# ============================================================
# Section 3: 十二長生狀態完整數據
# ============================================================
print('=' * 70)
print('Section 3: 十二長生狀態')
print('=' * 70)

STAGES = ['長生', '沐浴', '冠帶', '臨官', '帝旺', '衰', '病', '死', '墓', '絕', '胎', '養']
STAGE_MEANINGS = {
    '長生': '出生、生長、來源、起點',
    '沐浴': '洗澡、入水、裸體、暴露',
    '冠帶': '穿著、打扮、包裝、榮譽',
    '臨官': '自力更生、成長、當官、公務員',
    '帝旺': '輝煌、極限、頂點、強大',
    '衰': '衰弱、敗落、退縮、不敢反抗',
    '病': '疾病、缺點、毛病、問題',
    '死': '死亡、不動變通、不景氣、沒有活路',
    '墓': '埋藏、受控制、沒有自由、昏昏沉沉',
    '絕': '絕境、分手、死心、消失',
    '胎': '懷胎、醞釀、計劃、與生俱來',
    '養': '休養、依靠、扶助、養育',
}

DIZHI = ['子','丑','寅','卯','辰','巳','午','未','申','酉','戌','亥']
DIZHI_IDX = {d: i for i, d in enumerate(DIZHI)}

# 地支→宮位映射
DIZHI_PALACE = {
    '子': 1, '丑': 8, '寅': 8, '卯': 3,
    '辰': 4, '巳': 4, '午': 9, '未': 2,
    '申': 2, '酉': 7, '戌': 6, '亥': 6,
}

# 陽干長生位置
YANG_CS = {'甲': '亥', '丙': '寅', '戊': '寅', '庚': '巳', '壬': '申'}
# 陰干長生位置（陰陽互為生死）
YIN_CS = {'乙': '午', '丁': '酉', '己': '酉', '辛': '子', '癸': '卯'}

TIANGAN_YINYANG = {
    '甲': '陽', '乙': '陰', '丙': '陽', '丁': '陰',
    '戊': '陽', '己': '陰', '庚': '陽', '辛': '陰',
    '壬': '陽', '癸': '陰',
}

TIANGAN_WUXING = {
    '甲': '木', '乙': '木', '丙': '火', '丁': '火',
    '戊': '土', '己': '土', '庚': '金', '辛': '金',
    '壬': '水', '癸': '水',
}

def compute_changsheng(tiangan):
    """計算天干的十二長生：返回 {stage: dizhi}"""
    if tiangan in YANG_CS:
        start = YANG_CS[tiangan]
        direction = 1  # 陽干順時針
    else:
        start = YIN_CS[tiangan]
        direction = -1  # 陰干逆時針

    start_idx = DIZHI_IDX[start]
    result = {}
    for i, stage in enumerate(STAGES):
        dz_idx = (start_idx + direction * i) % 12
        dz = DIZHI[dz_idx]
        result[stage] = dz
    return result

def get_stage_in_palace(tiangan, palace):
    """查詢天干在某宮的十二長生狀態
    返回 list of (dizhi, stage)，因為一宮可能含兩個地支"""
    cs = compute_changsheng(tiangan)
    palace_dzs = PALACE_DIZHI.get(palace, [])
    results = []
    for dz in palace_dzs:
        for stage, stage_dz in cs.items():
            if stage_dz == dz:
                results.append((dz, stage))
    return results

# 3a. 驗證陰陽互為生死
print('\n3a. 驗證「陰陽互為生死」規律：')
pairs = [('甲','乙'), ('丙','丁'), ('戊','己'), ('庚','辛'), ('壬','癸')]
for yang, yin in pairs:
    yang_cs = compute_changsheng(yang)
    yin_cs = compute_changsheng(yin)
    yang_death_dz = yang_cs['死']
    yin_birth_dz = yin_cs['長生']
    match = '✅' if yang_death_dz == yin_birth_dz else '❌'
    print(f'  {yang}死於{yang_death_dz} = {yin}長生於{yin_birth_dz} {match}')
print()

# 3b. 完整十二長生表
print('3b. 十天干十二長生完整表：')
print(f'\n{"天干":<4} {"陰陽":<4} {"五行":<4}', end='')
for s in STAGES:
    print(f' {s:<4}', end='')
print()
print('-' * 72)

CHANGSHENG_TABLE = {}
for tg in ['甲','乙','丙','丁','戊','己','庚','辛','壬','癸']:
    cs = compute_changsheng(tg)
    CHANGSHENG_TABLE[tg] = cs
    print(f'{tg:<4} {TIANGAN_YINYANG[tg]:<4} {TIANGAN_WUXING[tg]:<4}', end='')
    for s in STAGES:
        print(f' {cs[s]:<4}', end='')
    print()
print()

# 3c. 十二長生含義
print('3c. 十二長生各狀態含義：')
for stage, meaning in STAGE_MEANINGS.items():
    print(f'  {stage:<4}: {meaning}')
print()

# 3d. 旺弱分類
WANG_STAGES = ['長生', '臨官', '帝旺']
RUO_STAGES = ['沐浴', '冠帶', '衰', '病', '死', '墓', '絕', '胎', '養']
WORST_STAGE = '墓'

print('3d. 旺弱分類：')
print(f'  旺（3種）: {"、".join(WANG_STAGES)}')
print(f'    → 得地利，有能力，做事容易成功')
print(f'  弱（9種）: {"、".join(RUO_STAGES)}')
print(f'    → 不得地利，一般以凶斷')
print(f'  最差: {WORST_STAGE}')
print(f'    → 手腳被綁，能量無法發揮，混混噩噩，一事無成')
print()

# 3e. 驗證案例：戊在離九宮=帝旺
print('3e. 驗證案例：天干戊在離九宮的狀態：')
result = get_stage_in_palace('戊', 9)
for dz, stage in result:
    print(f'  戊在離九宮({dz}) → {stage}')
print(f'  → 帝旺 ✅ （與師傅案例分析一致）')
print()

# 3f. 天干×宮位→狀態 完整映射
print('3f. 天干×宮位→十二長生狀態 完整映射：')
TG_PALACE_STAGE = {}
print(f'\n{"天干":<4}', end='')
for p in [1,2,3,4,5,6,7,8,9]:
    print(f' {GONG_NAMES[p]}{p:<3}', end='')
print()
print('-' * 50)
for tg in ['甲','乙','丙','丁','戊','己','庚','辛','壬','癸']:
    print(f'{tg:<4}', end='')
    TG_PALACE_STAGE[tg] = {}
    for p in [1,2,3,4,5,6,7,8,9]:
        stages = get_stage_in_palace(tg, p)
        if stages:
            stage_names = '/'.join([s for _, s in stages])
            TG_PALACE_STAGE[tg][p] = stage_names
            # 標記旺/弱
            is_wang = any(s in WANG_STAGES for _, s in stages)
            marker = '*' if is_wang else ''
            print(f' {stage_names:<4}{marker}', end='')
        else:
            TG_PALACE_STAGE[tg][p] = None
            print(f' {"-":<4}', end='')
    print()
print('\n  * = 旺狀態（長生/臨官/帝旺）')
print()

# ============================================================
# Section 4: 實際應用策略
# ============================================================
print('=' * 70)
print('Section 4: 十二長生實際應用策略')
print('=' * 70)

STRATEGIES = {
    '帝旺': {
        'action': '全力進取',
        'reason': '能量最強大，很快會由盛轉衰',
        'advice': '爭取在最短時間取得最大收益',
    },
    '長生': {
        'action': '積極發展',
        'reason': '處於上升期，潛力大',
        'advice': '適合開始新事物、學習、成長',
    },
    '臨官': {
        'action': '穩步前進',
        'reason': '自力更生，有成長空間',
        'advice': '適合求職、升遷、建立事業',
    },
    '衰': {
        'action': '防禦為主',
        'reason': '開始走下坡',
        'advice': '不宜冒險，鞏固現有成果',
    },
    '病': {
        'action': '暫停休息',
        'reason': '出現問題和毛病',
        'advice': '先解決問題，不要強行推進',
    },
    '死': {
        'action': '避免行動',
        'reason': '沒有活路，不動變通',
        'advice': '等待時機轉變',
    },
    '墓': {
        'action': '忍耐等待',
        'reason': '能量被壓制，無法發揮',
        'advice': '最差狀態，絕不輕舉妄動',
    },
    '絕': {
        'action': '放棄或轉向',
        'reason': '絕境、死心',
        'advice': '考慮完全放棄或徹底改變方向',
    },
    '胎': {
        'action': '醞釀計劃',
        'reason': '懷胎、計劃階段',
        'advice': '適合策劃但不適合行動',
    },
    '養': {
        'action': '休養生息',
        'reason': '需要依靠和扶助',
        'advice': '適合學習、積累、等待',
    },
    '沐浴': {
        'action': '謹慎暴露',
        'reason': '裸體、暴露、入水',
        'advice': '容易被看穿，注意隱私和保密',
    },
    '冠帶': {
        'action': '包裝展示',
        'reason': '穿著打扮、榮譽',
        'advice': '適合展示自己、建立形象',
    },
}

print('\n各狀態的應對策略：')
for stage, info in STRATEGIES.items():
    is_wang = stage in WANG_STAGES
    marker = '[旺]' if is_wang else '[弱]'
    print(f'  {marker} {stage}:')
    print(f'    行動: {info["action"]}')
    print(f'    原因: {info["reason"]}')
    print(f'    建議: {info["advice"]}')
    print()

# ============================================================
# Section 5: 帝旺在疾病場景的特殊含義
# ============================================================
print('=' * 70)
print('Section 5: 帝旺在疾病場景的特殊含義')
print('=' * 70)

print('\n一般場景 vs 疾病場景：')
print(f'  {"狀態":<8} {"一般含義":<25} {"疾病含義(老人)"}')
print('  ' + '-' * 60)
print(f'  {"帝旺":<8} {"最強大、全力進取":<25} {"迴光反照、極不樂觀"}')
print(f'  {"長生":<8} {"積極發展、潛力大":<25} {"疾病剛開始、尚可控制"}')
print(f'  {"墓":<8} {"最差、不動":<25} {"慢性病、長期困擾"}')
print()
print('⚠️ 關鍵原則：帝旺 = 物極必反')
print('  年輕人帝旺 → 好事，正值巔峰')
print('  老人帝旺 → 壞事，迴光反照，之後只會越來越差')
print('  → 判斷時必須考慮年齡因素')
print()

# ============================================================
# Section 6: 與之前集數的對照
# ============================================================
print('=' * 70)
print('Section 6: 與之前集數的對照')
print('=' * 70)

print('1. EP13 疾病框架在 EP14 案例中全面驗證')
print('   天芮星定位疾病 ✅')
print('   乙=中醫、天心=西醫 ✅')
print('   年干=長輩（母親） ✅')
print('   九宮人體映射（離9=頭/心/腦） ✅')
print('   天干人體映射（丁=心/眼、壬=血液、戊=堵塞） ✅')
print()

print('2. 天干暗含地支概念（EP13 G61）在 EP14 再確認')
print('   EP13: 庚(申)+癸(寅)=衝格')
print('   EP14: 戊(子)落離九(午)=子午相衝=久病逢衝')
print('   → 暗含地支概念從天干組合擴展到天干vs宮位')
print()

print('3. 逢衝必動（EP12）在 EP14 疾病案例的應用')
print('   EP12: 逢衝必動、逢衝必散（一般場景）')
print('   EP14: 久病逢衝=大凶（疾病場景）')
print('   → 逢衝的具體含義取決於場景')
print()

print('4. 用神含義繼續擴充')
print('   傷門: EP12=追債人 → EP14=手術傷口')
print('   九天: EP12=科技/雲端 → EP14=飛上天(死亡)')
print('   空亡: 多集=缺失 → EP14=不存在(死亡)')
print('   庚: EP13=大腸/筋骨 → EP14=大凶符號(血光/不治)')
print()

print('5. 十二長生 = 用神狀態評估的新維度')
print('   之前: 用神評分主要看五行生剋+吉凶格局')
print('   現在: 加入十二長生狀態，判斷用神本身的旺弱')
print('   → 這是一個全新的評分維度')
print()

# ============================================================
# Section 7: EP14 新發現的不足
# ============================================================
print('=' * 70)
print('Section 7: EP14 新發現的不足')
print('=' * 70)

NEW_GAPS = [
    ('G74', '高', '十二長生尚未納入 engine.py 評分',
     '本集完整講解了十二長生，但引擎無此計算',
     '需實現 compute_changsheng() 並整合入評分'),
    ('G75', '高', '疾病場景用神狀態解讀規則不完整',
     '僅知帝旺(老人)=凶，其他狀態在疾病的含義未知',
     '需更多案例或師傅後續講解'),
    ('G76', '中', '天干庚的「大凶」含義邊界不明確',
     '庚=血光之災或不治之症，但何時是血光何時是不治？',
     '需更多案例驗證'),
    ('G77', '中', '坤二宮=母親的規則適用範圍',
     '是否所有女性長輩都看坤二宮？父親看哪宮？',
     '需確認家庭角色與宮位的完整映射'),
    ('G78', '低', '十二長生在非疾病場景的應用',
     '本集主要講疾病案例，十二長生在其他場景(事業/投資)的應用待探索',
     '需在後續集數中留意'),
    ('G79', '低', '中五宮無地支的處理',
     '中五宮不包含地支，十二長生在此宮無狀態',
     '需確認中五宮的特殊處理方式'),
]

for gid, priority, name, current, expected in NEW_GAPS:
    print(f'  [{priority}] {gid}: {name}')
    print(f'       現狀: {current}')
    print(f'       期望: {expected}')
    print()

# ============================================================
# Section 8: 結論
# ============================================================
print('=' * 70)
print('Section 8: 結論')
print('=' * 70)

print('EP14 的核心貢獻：')
print('  1. 疾病案例方法論（9條新規則 R01-R09）')
print('  2. 帝旺+老人=迴光反照=大凶')
print('  3. 久病逢衝=大凶（天干地支vs宮位地支）')
print('  4. 九天+空亡=死亡徵兆組合')
print('  5. 坤二宮=母親（家庭角色用神）')
print('  6. 天干庚=大凶符號')
print('  7. 十二長生完整數據表（10干x12狀態）')
print('  8. 陽干順時針/陰干逆時針排列規則')
print('  9. 陰陽互為生死位置（程序驗證通過）')
print(' 10. 旺弱分類（3旺9弱）+ 入墓=最差')
print(' 11. 各狀態應對策略')
print()

print('對 backtest 的影響：')
print('  - 十二長生 = 用神狀態評估新維度（影響所有場景的評分）')
print('  - 疾病規則 = 疾病預測場景的評分更精確')
print('  - 久病逢衝 = 新的凶險信號指標')
print('  - 累計 Gap: G01-G79')
print()

# ============================================================
# Section 9: JSON 輸出
# ============================================================

ep14_data = {
    "episode": 14,
    "title": "疾病預測案例方法論 + 十二長生狀態",
    "disease_rules": {
        rid: {"name": r["name"], "condition": r["condition"], "judgment": r["judgment"]}
        for rid, r in DISEASE_RULES.items()
    },
    "changsheng_table": CHANGSHENG_TABLE,
    "changsheng_palace_map": TG_PALACE_STAGE,
    "stage_meanings": STAGE_MEANINGS,
    "wang_stages": WANG_STAGES,
    "ruo_stages": RUO_STAGES,
    "worst_stage": WORST_STAGE,
    "strategies": STRATEGIES,
    "case_study": {
        "background": CASE_STUDY['background'],
        "tiarui_palace": 9,
        "nian_gan_palace": 9,
        "nian_gan_stage": "帝旺",
        "nian_gan_chong": reason,
        "yi_treatment": "無效（木生火，中醫生疾病）",
        "tianxin_treatment": "無效（火剋金，疾病剋西醫）",
        "verdict": "很難跨過這道坎，最多不超過半年",
    },
    "yinyang_life_death_verified": True,
    "new_gaps": [
        {"id": g[0], "priority": g[1], "name": g[2], "current": g[3], "expected": g[4]}
        for g in [
            ('G74','高','十二長生尚未納入引擎','無此計算','需整合'),
            ('G75','高','疾病場景用神狀態解讀不完整','僅知帝旺=凶','需更多案例'),
            ('G76','中','庚大凶含義邊界不明確','血光或不治','需驗證'),
            ('G77','中','坤二宮=母親適用範圍','未確認','需確認映射'),
            ('G78','低','十二長生非疾病應用','主要講疾病','需探索'),
            ('G79','低','中五宮無地支處理','無狀態','需確認'),
        ]
    ],
}

output_path = '/home/z/my-project/download/ep14_disease_changsheng.json'
with open(output_path, 'w') as f:
    json.dump(ep14_data, f, ensure_ascii=False, indent=2)
print(f'→ 已輸出 {output_path}')
print('\n' + '*' * 70)
print('  EP14 量化完成！')
print('*' * 70)