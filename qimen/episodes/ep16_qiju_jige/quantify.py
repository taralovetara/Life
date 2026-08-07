#!/usr/bin/env python3
"""
EP16 量化腳本：起局時間原則 + 常用吉格
===================================================================

本集新知識點：
1. 無事不占（必須有真實渴求想知道嘅事）
2. 不動不占（必須在起念或外應出現時起局）
3. 起念 vs 事情發生嘅時間區別（用起念時間，唔係事情發生時間）
4. 不使用出生盤（除咗問終身情況）
5. 玉女守門（值使門+地盤丁同宮）
6. 三奇貴人升殿（乙落震3 / 丙落離9 / 丁落兌7）
7. 奇遊祿位（三奇落各自臨官位：乙震3 / 丙巽4 / 丁離9）
8. 天輔吉時（五合日+特定甲X時）
9. 三詐五假（真詐/重詐/休詐 + 天假/地假/人假/神假/鬼假）
10. 局部吉凶受全盤影響原則
"""

import json

GONG_NAMES = {1:'坎', 2:'坤', 3:'震', 4:'巽', 5:'中', 6:'乾', 7:'兌', 8:'艮', 9:'離'}
PALACE_WUXING = {1:'水', 2:'土', 3:'木', 4:'木', 5:'土', 6:'金', 7:'金', 8:'土', 9:'火'}

# ============================================================
# Section 1: 起局時間原則
# ============================================================
print('=' * 70)
print('Section 1: 起局時間原則')
print('=' * 70)

QIJU_PRINCIPLES = {
    'P01_無事不占': {
        'rule': '求測人必須有一件真實存在、非常想知道的事',
        'detail': [
            '必須是真實存在的事，不是臆想的',
            '必須是求測人渴求想知道的',
            '隨便找雞毛蒜皮的小事來求測 → 結果一定不準',
            '為了證明奇門不準而故意問 → 結果一定不準',
        ],
        'reason': '沒有真實的求知慾 → 立極點無法建立 → 沒有起局基礎',
        'metaphor': '好像蓋房子，地基沒打好，房子肯定建不好',
    },
    'P02_不動不占': {
        'rule': '必須在起念或外應出現時才可以起局',
        'detail': [
            '起念 = 突然心血來潮、靈光一閃、頭頂燈泡亮了',
            '外應 = 外在環境突然出現意料之外的變化',
            '外應例子：突然電話響、摔爛杯子、停電等',
            '外應原理：環境平衡被打破 → 必然有事情要發生',
        ],
        'reason': '宇宙狀態與求測人意念同步時，分析才準確',
    },
    'P03_起念時間優先': {
        'rule': '用求測人突然想問測的時間點起局，不是事情發生的時間',
        'detail': [
            '事情發生時求測人只是知道了，未必想問測',
            '過了若干時間後突然想問 → 用突然想問的時間',
            '除非事情發生的瞬間馬上想問 → 兩個時間點重疊',
        ],
        'reason': '起念才是求測人與宇宙產生連接的時刻',
    },
    'P04_不用出生盤': {
        'rule': '問測特定事情必須按當時時間起局，絕對不可用出生盤',
        'detail': [
            '唯一例外：求測人要問自己的終身情況',
            '其他所有情況：用起念時間起局',
            '這是奇門遁甲優勝於生辰八字術數的原因之一',
        ],
        'reason': '奇門遁甲可以輕鬆預測不同時間點發生的事情',
    },
}

for pid, info in QIJU_PRINCIPLES.items():
    print(f'\n{pid}:')
    print(f'  規則: {info["rule"]}')
    for d in info['detail']:
        print(f'  - {d}')
    print(f'  原理: {info["reason"]}')

print('\n⚠️ 關鍵提醒：用錯起局時間 → 預測結果差天同地（差之毫釐，謬以千里）')
print()

# 李某某案例時間對比
print('李某某案例時間對照：')
print('  事件發生時間: 不明確（何時被捕）')
print('  新聞發佈時間: 10月21日晚上9:07分（人民日報微博）')
print('  起念時間: 求測人突然想問測此事的時間（未知）')
print('  → 按新聞時間起局 vs 按起念時間起局 = 完全不同的盤局')
print('  → 師傅留了功課：大家可以嘗試用新聞時間起局對比分析')
print()

# ============================================================
# Section 2: 格局定義確認
# ============================================================
print('=' * 70)
print('Section 2: 格局定義確認')
print('=' * 70)

print('\n格局的定義（本集明確給出）：')
print('  八神、九星、八門、十天干')
print('  落在九宮裡面所組成的組合 = 格局')
print()
print('格局分類：')
print('  吉格 → 應吉的格局（本集重點）')
print('  凶格 → 應凶的格局（之前集數已教：衝格、螣蛇夭矯等）')
print('  數量：很多，本集只介紹常用吉格')
print()

# ============================================================
# Section 3: 玉女守門
# ============================================================
print('=' * 70)
print('Section 3: 玉女守門')
print('=' * 70)

YUNV_SHOUMEN = {
    'name': '玉女守門',
    'type': '吉格',
    'condition': '同一宮位有值使門 + 地盤丁',
    'critical': '丁必須在地盤（天盤不算）',
    'general_meaning': '對很多事情都應吉，特別適合男女嫁娶',
    'also_represents': ['女領導', '女強人', '女性當家'],
    'male_marriage': {
        'meaning': '不太好',
        'detail': [
            '男仕在家沒有地位',
            '婚姻會有第三者出現',
            '特別是太太一方容易出問題',
        ],
        'caveat': '必須綜合分析整個盤局，不能只看一個格局就斷定',
    },
    'engine_note': '需檢查每宮：值使門所在宮位的地盤天干是否為丁',
}

print(f'\n{YUNV_SHOUMEN["name"]}（{YUNV_SHOUMEN["type"]}）')
print(f'  條件: {YUNV_SHOUMEN["condition"]}')
print(f'  ⚠️ 關鍵: {YUNV_SHOUMEN["critical"]}')
print(f'  一般含義: {YUNV_SHOUMEN["general_meaning"]}')
print(f'  也代表: {"、".join(YUNV_SHOUMEN["also_represents"])}')
print(f'  男士問婚姻: {YUNV_SHOUMEN["male_marriage"]["meaning"]}')
for d in YUNV_SHOUMEN['male_marriage']['detail']:
    print(f'    - {d}')
print(f'  注意: {YUNV_SHOUMEN["male_marriage"]["caveat"]}')
print()

# ============================================================
# Section 4: 三奇貴人升殿
# ============================================================
print('=' * 70)
print('Section 4: 三奇貴人升殿')
print('=' * 70)

SANQI_GUIREN = {
    'name': '三奇貴人升殿',
    'type': '吉格',
    'conditions': [
        {'tiangan': '乙', 'target_palace': 3, 'palace_name': '震三宮', 'note': '天盤乙落震三宮'},
        {'tiangan': '丙', 'target_palace': 9, 'palace_name': '離九宮', 'note': '天盤丙落離九宮'},
        {'tiangan': '丁', 'target_palace': 7, 'palace_name': '兌七宮', 'note': '天盤丁落兌七宮'},
    ],
    'trigger': '只要其中一個出現即可',
    'enhanced': '宮裡還有吉門 → 吉上加吉',
    'general': '對絕大部分事情應吉',
    'especially': ['新官上任', '拜見領導', '才能得到認可', '人才得到重用'],
}

print(f'\n{SANQI_GUIREN["name"]}（{SANQI_GUIREN["type"]}）')
print(f'  條件（任一）：')
for c in SANQI_GUIREN['conditions']:
    print(f'    {c["note"]}')
print(f'  觸發: {SANQI_GUIREN["trigger"]}')
print(f'  加強: {SANQI_GUIREN["enhanced"]}')
print(f'  一般: {SANQI_GUIREN["general"]}')
print(f'  特別有利: {"、".join(SANQI_GUIREN["especially"])}')
print()

# ============================================================
# Section 5: 奇遊祿位
# ============================================================
print('=' * 70)
print('Section 5: 奇遊祿位')
print('=' * 70)

# 驗證：三奇嘅臨官位
DIZHI = ['子','丑','寅','卯','辰','巳','午','未','申','酉','戌','亥']
DIZHI_IDX = {d: i for i, d in enumerate(DIZHI)}
STAGES = ['長生','沐浴','冠帶','臨官','帝旺','衰','病','死','墓','絕','胎','養']
YANG_CS = {'甲':'亥','丙':'寅','戊':'寅','庚':'巳','壬':'申'}
YIN_CS  = {'乙':'午','丁':'酉','己':'酉','辛':'子','癸':'卯'}
DIZHI_PALACE = {
    '子':1,'丑':8,'寅':8,'卯':3,'辰':4,'巳':4,
    '午':9,'未':2,'申':2,'酉':7,'戌':6,'亥':6,
}

def compute_changsheng(tg):
    if tg in YANG_CS: start, d = YANG_CS[tg], 1
    else: start, d = YIN_CS[tg], -1
    si = DIZHI_IDX[start]
    return {s: DIZHI[(si + d*i) % 12] for i, s in enumerate(STAGES)}

QIYOU_LUWEI = {
    'name': '奇遊祿位',
    'type': '吉格',
    'conditions': [
        {'tiangan': '乙', 'target_palace': 3, 'palace_name': '震三宮', 'stage': '臨官'},
        {'tiangan': '丙', 'target_palace': 4, 'palace_name': '巽四宮', 'stage': '臨官'},
        {'tiangan': '丁', 'target_palace': 9, 'palace_name': '離九宮', 'stage': '臨官'},
    ],
    'trigger': '只要其中一個出現即可',
    'enhanced': '有吉門同宮 → 更加好',
    'essence': '乙丙丁三奇分別落在它們十二長生的臨官位置',
    'general': '跟三奇貴人升殿差不多，人才得到重用',
}

print(f'\n{QIYOU_LUWEI["name"]}（{QIYOU_LUWEI["type"]}）')
print(f'  本質: {QIYOU_LUWEI["essence"]}')
print(f'  條件（任一）：')
for c in QIYOU_LUWEI['conditions']:
    cs = compute_changsheng(c['tiangan'])
    linguan_dz = cs['臨官']
    linguan_palace = DIZHI_PALACE[linguan_dz]
    match = '✅' if linguan_palace == c['target_palace'] else '❌'
    print(f'    {c["tiangan"]}落{c["palace_name"]} → {c["tiangan"]}臨官在{linguan_dz}({GONG_NAMES[linguan_palace]}{linguan_palace}宮) {match}')
print(f'  觸發: {QIYOU_LUWEI["trigger"]}')
print(f'  加強: {QIYOU_LUWEI["enhanced"]}')
print(f'  一般: {QIYOU_LUWEI["general"]}')
print()

# 三奇貴人升殿 vs 奇遊祿位對照
print('三奇貴人升殿 vs 奇遊祿位 對照：')
print(f'  {"天干":<4} {"貴人升殿":<15} {"遊祿位":<15} {"相同?"}')
print('  ' + '-' * 45)
for qi in ['乙','丙','丁']:
    gr = next((c['palace_name'] for c in SANQI_GUIREN['conditions'] if c['tiangan']==qi), '-')
    ly = next((c['palace_name'] for c in QIYOU_LUWEI['conditions'] if c['tiangan']==qi), '-')
    same = '✅' if gr == ly else '❌ 不同' if gr != '-' and ly != '-' else '-'
    print(f'  {qi:<4} {gr:<15} {ly:<15} {same}')
print('  → 乙嘅宮位相同，丙和丁嘅宮位不同')
print()

# ============================================================
# Section 6: 天輔吉時
# ============================================================
print('=' * 70)
print('Section 6: 天輔吉時')
print('=' * 70)

TIANFU_JISHI = {
    'name': '天輔吉時',
    'type': '吉格（擇時用）',
    'combinations': [
        {'day_gan': ['甲','己'], 'hour': '甲戌時'},
        {'day_gan': ['乙','庚'], 'hour': '甲申時'},
        {'day_gan': ['丙','辛'], 'hour': '甲午時'},
        {'day_gan': ['丁','壬'], 'hour': '甲辰時'},
        {'day_gan': ['戊','癸'], 'hour': '甲寅時'},
    ],
    'usage': ['出門遠行', '求職求官', '婚姻嫁娶', '擇時做事'],
    'important': '天輔吉時出現時一定是伏吟局',
    'caveat': '伏吟局一般不好，所以預測時不能馬上以吉斷，要全盤分析',
    'distinction': '擇時=應吉 / 預測=需全盤分析',
}

print(f'\n{TIANFU_JISHI["name"]}（{TIANFU_JISHI["type"]}）')
print(f'  組合：')
for c in TIANFU_JISHI['combinations']:
    print(f'    {"/".join(c["day_gan"])}日 + {c["hour"]}')
print(f'  適合: {"、".join(TIANFU_JISHI["usage"])}')
print(f'  ⚠️ 重要: {TIANFU_JISHI["important"]}')
print(f'  注意: {TIANFU_JISHI["caveat"]}')
print(f'  區分: {TIANFU_JISHI["distinction"]}')
print()

# 五合日規律
print('天輔吉時的規律分析：')
print('  日干對 = 五合：甲己合土、乙庚合金、丙辛合水、丁壬合木、戊癸合火')
print('  時干 = 甲 + 地支：甲戌→甲申→甲午→甲辰→甲寅')
print('  地支規律：戌(11)→申(9)→午(7)→辰(5)→寅(3)，每次減2')
print()

# 甲X時的對應關係
print('甲X時 → 實際時辰對照：')
print('  甲戌時 = 第11個時辰（19:00-21:00）')
print('  甲申時 = 第9個時辰（15:00-17:00）')
print('  甲午時 = 第7個時辰（11:00-13:00）')
print('  甲辰時 = 第5個時辰（07:00-09:00）')
print('  甲寅時 = 第3個時辰（03:00-05:00）')
print()

# ============================================================
# Section 7: 三詐五假
# ============================================================
print('=' * 70)
print('Section 7: 三詐五假')
print('=' * 70)

SANZHA_WUJIA = {
    'name': '三詐五假',
    'type': '吉格（運籌用）',
    'definition': {
        '詐': '選擇最佳的運籌時機和時空',
        '假': '借取天地之氣來配合行事',
    },
    'three_zha': ['真詐', '重詐', '休詐'],
    'five_jia': ['天假', '地假', '人假', '神假', '鬼假'],
    'note': '師傅未逐一講解具體組合，只給了匯總表概念',
    'application': '現代生意場：製定和運用計謀，出奇制勝',
    'engine_note': '需等待師傅講解具體組合條件才能量化',
}

print(f'\n{SANZHA_WUJIA["name"]}（{SANZHA_WUJIA["type"]}）')
print(f'  詐的含義: {SANZHA_WUJIA["definition"]["詐"]}')
print(f'  假的含義: {SANZHA_WUJIA["definition"]["假"]}')
print(f'  三詐: {"、".join(SANZHA_WUJIA["three_zha"])}')
print(f'  五假: {"、".join(SANZHA_WUJIA["five_jia"])}')
print(f'  應用: {SANZHA_WUJIA["application"]}')
print(f'  ⚠️ {SANZHA_WUJIA["note"]}')
print()

# ============================================================
# Section 8: 局部吉凶受全盤影響
# ============================================================
print('=' * 70)
print('Section 8: 局部吉凶受全盤影響')
print('=' * 70)

print('\n本集反覆強調的核心原則：')
print('  「局部的吉凶永遠都會受到全盤形勢的影響」')
print('  「全盤的吉凶才是最終的結果」')
print()
print('具體表現：')
print('  1. 天輔吉時 = 伏吟局（一般不好），不能只看吉時就斷吉')
print('  2. 玉女守門 = 男士婚姻未必好，不能只看格局就斷第三者')
print('  3. 三奇貴人升殿/奇遊祿位 = 雖然大吉，也要看全盤')
print('  → G47 第三次確認：任何符號/格局嘅解讀必須考慮場景和全盤')
print()

# ============================================================
# Section 9: 與之前集數的對照
# ============================================================
print('=' * 70)
print('Section 9: 與之前集數的對照')
print('=' * 70)

print('1. 起念/外應概念演變')
print('   EP14(李某某): 起念和外應的基本概念（簡述）')
print('   EP16(本集): 無事不占+不動不占兩大原則（完整講解）')
print('   → EP14→EP16 形成完整嘅起局時間原則體系')
print()

print('2. 起局時間 vs 出生盤')
print('   之前: 未明確講過此區別')
print('   EP16: 明確規定問特定事情=用起念時間，不用出生盤')
print('   → 這解釋了為何奇門可以預測不同時間點的事')
print()

print('3. 格局系統擴充')
print('   之前: 衝格、合格、伏吟、反吟、十干剋應(8組)等')
print('   EP16 新增: 玉女守門、三奇貴人升殿、奇遊祿位、天輔吉時、三詐五假')
print('   格局庫進一步擴充')
print()

print('4. 十二長生(EP14/EP15)與奇遊祿位的連接')
print('   EP14/EP15: 建立了完整嘅十二長生表')
print('   EP16: 奇遊祿位直接使用了臨官位置 → 驗證通過 ✅')
print('   → 十二長生數據已開始被其他格局引用')
print()

print('5. 伏吟局(EP12)與天輔吉時的關係')
print('   EP12: 伏吟=利主不利客、被動慢')
print('   EP16: 天輔吉時一定是伏吟局')
print('   → 伏吟在擇時場景下反而有好嘅一面')
print()

# ============================================================
# Section 10: EP16 新發現的不足
# ============================================================
print('=' * 70)
print('Section 10: EP16 新發現的不足')
print('=' * 70)

NEW_GAPS = [
    ('G80', '高', '三詐五假具體組合條件未知',
     '師傅只給了名稱和概念，未講解具體觸發條件',
     '需等待後續集數或自行研究匯總表'),
    ('G81', '高', '玉女守門嘅值使門確定方法',
     '值使門隨時辰變化，engine 需要計算值使門所在宮位',
     '需在 engine 中實現值使門計算'),
    ('G82', '中', '天輔吉時的甲X時計算',
     '需要從日干推算當日各時辰的天干',
     '需實現時辰天干計算函數'),
    ('G83', '中', '格局檢測函數未系統化',
     '目前格局散落在各集數，未有統一嘅檢測框架',
     '需建立 geju_detect(palace_data) 統一函數'),
    ('G84', '低', '吉格在疾病/婚姻等特殊場景的含義',
     '本集教玉女守門在男士婚姻=不好，其他吉格呢？',
     '需建立 SCENE_EXCEPTION 擴充映射'),
    ('G85', 'low', '全盤吉凶的量化方法',
     '「全盤分析」是定性描述，如何量化為評分？',
     '需設計全盤綜合評分算法'),
]

for gid, priority, name, current, expected in NEW_GAPS:
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

print('EP16 的核心貢獻：')
print('  1. 起局時間兩大原則（無事不占+不動不占）')
print('  2. 起念時間 > 事情發生時間')
print('  3. 不用出生盤（除終身問測）')
print('  4. 格局正式定義（八神九星八門十天干的宮位組合）')
print('  5. 玉女守門（值使門+地盤丁）')
print('  6. 三奇貴人升殿（乙震3/丙離9/丁兌7）')
print('  7. 奇遊祿位（三奇臨官位，與EP14/EP15十二長生銜接）')
print('  8. 天輔吉時（五合日+甲X時，必為伏吟局）')
print('  9. 三詐五假（名稱+概念，具體組合待補）')
print(' 10. 局部吉凶受全盤影響（G47 第三次確認）')
print()

print('對 backtest 的影響：')
print('  - 起局原則 = 確保預測時間準確性的基礎')
print('  - 吉格檢測 = 可以自動識別盤局中的吉格局')
print('  - 奇遊祿位 = 連接十二長生數據的第一個格局應用')
print('  - 累計 Gap: G01-G85')
print()

# ============================================================
# Section 12: JSON 輸出
# ============================================================

ep16_data = {
    "episode": 16,
    "title": "起局時間原則 + 常用吉格",
    "qiju_principles": {
        pid: {"rule": p["rule"], "reason": p["reason"]}
        for pid, p in QIJU_PRINCIPLES.items()
    },
    "jige": {
        "玉女守門": {
            "condition": YUNV_SHOUMEN['condition'],
            "critical": YUNV_SHOUMEN['critical'],
            "general": YUNV_SHOUMEN['general_meaning'],
            "male_marriage": YUNV_SHOUMEN['male_marriage']['meaning'],
        },
        "三奇貴人升殿": {
            "conditions": [
                {"tiangan": c['tiangan'], "palace": c['target_palace'], "name": c['palace_name']}
                for c in SANQI_GUIREN['conditions']
            ],
            "trigger": SANQI_GUIREN['trigger'],
            "general": SANQI_GUIREN['general'],
        },
        "奇遊祿位": {
            "conditions": [
                {"tiangan": c['tiangan'], "palace": c['target_palace'], "name": c['palace_name'],
                 "stage": c['stage'], "verified": True}
                for c in QIYOU_LUWEI['conditions']
            ],
            "essence": QIYOU_LUWEI['essence'],
        },
        "天輔吉時": {
            "combinations": [
                {"day_gan": c['day_gan'], "hour": c['hour']}
                for c in TIANFU_JISHI['combinations']
            ],
            "always_fuyin": True,
            "usage": TIANFU_JISHI['usage'],
        },
        "三詐五假": {
            "three_zha": SANZHA_WUJIA['three_zha'],
            "five_jia": SANZHA_WUJIA['five_jia'],
            "definition": SANZHA_WUJIA['definition'],
            "combinations_unknown": True,
        },
    },
    "new_gaps": [
        {"id": g[0], "priority": g[1], "name": g[2], "current": g[3], "expected": g[4]}
        for g in [
            ('G80','高','三詐五假具體組合未知','只有名稱','需等待或研究'),
            ('G81','高','值使門確定方法','隨時辰變化','需實現計算'),
            ('G82','中','天輔吉時甲X時計算','需推算時辰天干','需實現函數'),
            ('G83','中','格局檢測未系統化','散落各集數','需統一框架'),
            ('G84','low','吉格場景含義不完整','僅知玉女守門','需擴充'),
            ('G85','low','全盤吉凶量化方法','定性描述','需設計算法'),
        ]
    ],
}

output_path = '/home/z/my-project/download/ep16_qiju_jige.json'
with open(output_path, 'w') as f:
    json.dump(ep16_data, f, ensure_ascii=False, indent=2)
print(f'→ 已輸出 {output_path}')
print('\n' + '*' * 70)
print('  EP16 量化完成！')
print('*' * 70)