#!/usr/bin/env python3
"""
EP17 量化腳本：官司訴訟預測 + 常用凶格
===================================================================

本集新知識點：
1. 官司訴訟六用神（值符/天乙/開門/六合/景門/驚門）
2. 官司分析框架（入稟狀→法院→原告vs被告→證據→律師→日時驗證）
3. 飛干格（日干+庚）和伏干格（庚+日干）
4. 刑格（庚+己）
5. 六儀擊刑（6個固定組合，地支相刑驗證）
6. 五不遇時（10組日時組合，同性相剋驗證）
7. 門迫（八門剋宮位，13個固定組合驗證）
8. 反吟局在官司=會上訴
"""

import json

PALACE_WUXING = {1:'水', 2:'土', 3:'木', 4:'木', 5:'土', 6:'金', 7:'金', 8:'土', 9:'火'}
GONG_NAMES = {1:'坎', 2:'坤', 3:'震', 4:'巽', 5:'中', 6:'乾', 7:'兌', 8:'艮', 9:'離'}
WUXING_SHENG = {"金": "水", "水": "木", "木": "火", "火": "土", "土": "金"}
WUXING_KE   = {"金": "木", "木": "土", "土": "水", "水": "火", "火": "金"}
TIANGAN_WUXING = {
    '甲':'木','乙':'木','丙':'火','丁':'火','戊':'土',
    '己':'土','庚':'金','辛':'金','壬':'水','癸':'水',
}
TIANGAN_YINYANG = {
    '甲':'陽','乙':'陰','丙':'陽','丁':'陰','戊':'陽',
    '己':'陰','庚':'陽','辛':'陰','壬':'陽','癸':'陰',
}

print('=' * 70)
print('Section 1: 官司訴訟六用神')
print('=' * 70)

LAWSUIT_YONGSHEN = {
    '值符': {'role': '原告', 'meaning': '個人或者公司', 'note': '求測人一方'},
    '天乙': {'role': '被告', 'meaning': '值符落宮原地盤天星', 'note': '個人或者公司'},
    '開門': {'role': '法庭/法院/法官', 'meaning': '也代表仲裁機構', 'note': '開放/公開=司法機構'},
    '六合': {'role': '證人/證據', 'meaning': '案件證人和證據', 'note': '合/聚集=證據'},
    '景門': {'role': '入稟狀/訴狀', 'meaning': '法律文件', 'note': '文書/光明=法律文件'},
    '驚門': {'role': '律師', 'meaning': '雙方律師', 'note': '口舌=辯護'},
}

for name, info in LAWSUIT_YONGSHEN.items():
    print(f'  {name} = {info["role"]}')
    print(f'    含義: {info["meaning"]}')
    print()

# ============================================================
print('=' * 70)
print('Section 2: 官司分析框架')
print('=' * 70)

def wx_rel(a_wx, b_wx):
    if a_wx == b_wx: return '比和'
    if WUXING_SHENG.get(a_wx) == b_wx: return f'{a_wx}生{b_wx}'
    if WUXING_KE.get(a_wx) == b_wx: return f'{a_wx}剋{b_wx}'
    if WUXING_SHENG.get(b_wx) == a_wx: return f'{b_wx}生{a_wx}(被生)'
    if WUXING_KE.get(b_wx) == a_wx: return f'{b_wx}剋{a_wx}(被剋)'
    return '?'

print('案例五行分析驗證：')
print('  景門(坎1/水)→開門(巽4/木): 水生木=遞送法院已接納')
print('  值符(乾6/金) vs 天乙(離9/火): 火剋金=原告輸')
print('  六合(離9/火)→值符(乾6/金): 火剋金=證據不利原告')
print('  驚門(震3/木)→值符(乾6/金): 金剋木=律師對原告不利')
print('  驚門(震3/木)→天乙(離9/火): 木生火=律師幫被告')
print('  開門(巽4/木)→天乙(離9/火): 木生火=法院傾向被告')
print('  時干(離9/火)→日干(乾6/金): 火剋金=事情剋求測人')
print('  → 全部指向原告輸 + 反吟局=會上訴')
print()

# ============================================================
print('=' * 70)
print('Section 3: 飛干格/伏干格/刑格')
print('=' * 70)

print('飛干格: 日干+庚同宮 → 遭遇不測、災難、困境')
print('伏干格: 庚+日干同宮 → 同上+失去行動自由')
print('  經商: 對方不可靠，不要交易，小心被暗算')
print('刑格: 庚+己同宮 → 阻滯、困難、進展緩慢')
print('  也代表: 官司、破財、患病')
print('  經商: 必須盡快放棄抽身')
print()

# ============================================================
print('=' * 70)
print('Section 4: 六儀擊刑')
print('=' * 70)

TIANGAN_HIDDEN_DZ = {'戊':'子','己':'戌','庚':'申','辛':'午','壬':'辰','癸':'寅'}
PALACE_DIZHI = {1:['子'],2:['未','申'],3:['卯'],4:['辰','巳'],5:[],6:['戌','亥'],7:['酉'],8:['丑','寅'],9:['午']}

SANXING = [
    ('寅','巳','申'),('巳','申','寅'),('申','寅','巳'),
    ('丑','未','戌'),('未','戌','丑'),('戌','丑','未'),
    ('子','卯'),('卯','子'),
    ('辰','辰'),('午','午'),('酉','酉'),('亥','亥'),
]

def is_xing(dz1, dz2):
    for group in SANXING:
        if dz1 in group and dz2 in group and dz1 != dz2:
            return True, f'{dz1}{dz2}相刑'
        if dz1 == dz2 and dz1 in ['辰','午','酉','亥']:
            return True, f'{dz1}{dz2}自刑'
    return False, None

LIUYI_XING = [
    {'tiangan':'壬','hidden':'辰','palace':4,'palace_dz':'辰','type':'辰辰自刑'},
    {'tiangan':'癸','hidden':'寅','palace':4,'palace_dz':'巳','type':'寅巳相刑'},
    {'tiangan':'辛','hidden':'午','palace':9,'palace_dz':'午','type':'午午自刑'},
    {'tiangan':'己','hidden':'戌','palace':2,'palace_dz':'未','type':'戌未相刑'},
    {'tiangan':'戊','hidden':'子','palace':3,'palace_dz':'卯','type':'子卯相刑'},
    {'tiangan':'庚','hidden':'申','palace':8,'palace_dz':'寅','type':'申寅相刑'},
]

print(f'  {"天干":<4} {"暗含":<4} {"落宮":<10} {"宮地支":<6} {"相刑類型":<10} {"驗證"}')
print('  ' + '-' * 50)
for item in LIUYI_XING:
    is_x, _ = is_xing(item['hidden'], item['palace_dz'])
    match = '✅' if is_x else '❌'
    p_name = GONG_NAMES[item['palace']] + str(item['palace']) + '宮'
    print(f'  {item["tiangan"]:<4} {item["hidden"]:<4} {p_name:<10} {item["palace_dz"]:<6} {item["type"]:<10} {match}')

print(f'  含義: 屋漏兼逢連夜雨（禍不單行）')
print(f'  測事: 困難、金錢損失')
print(f'  測人: 身體受傷、精神摧殘、自我矛盾')
print(f'  測婚姻: 性情暴躁、家庭暴力')
print()

# ============================================================
print('=' * 70)
print('Section 5: 五不遇時')
print('=' * 70)

WUBUYUSHI = [
    ('甲','庚'),('乙','辛'),('丙','壬'),('丁','癸'),
    ('戊','甲'),('己','乙'),('庚','丙'),('辛','丁'),
    ('壬','戊'),('癸','己'),
]

print(f'  {"日干":<4} {"時干":<4} {"日干五行":<8} {"時干五行":<8} {"關係":<10} {"同性?":<6} {"驗證"}')
print('  ' + '-' * 55)
for day_gan, hour_gan in WUBUYUSHI:
    d_wx = TIANGAN_WUXING[day_gan]
    h_wx = TIANGAN_WUXING[hour_gan]
    d_yy = TIANGAN_YINYANG[day_gan]
    h_yy = TIANGAN_YINYANG[hour_gan]
    ke = WUXING_KE.get(h_wx) == d_wx
    same = d_yy == h_yy
    rel = f'{h_wx}剋{d_wx}' if ke else '?'
    gender = '✅同' if same else '❌異'
    match = '✅' if ke and same else '❌'
    print(f'  {day_gan:<4} {hour_gan:<4} {d_wx:<8} {h_wx:<8} {rel:<10} {gender:<6} {match}')

print(f'  含義: 時干(事情)剋日干(求測人)=不順利')
print(f'  注意: 只代表不順利，不代表一定做不成')
print(f'  擇時: 最好避開五不遇時')
print()

# ============================================================
print('=' * 70)
print('Section 6: 門迫')
print('=' * 70)

BAMEN_WUXING = {'休門':'水','生門':'土','傷門':'木','杜門':'木','景門':'火','死門':'土','驚門':'金','開門':'金'}

MENPO_LIST = [
    ('休門','水','離9宮','火'),('開門','金','震3宮','木'),('開門','金','巽4宮','木'),
    ('驚門','金','震3宮','木'),('驚門','金','巽4宮','木'),('生門','土','坎1宮','水'),
    ('死門','土','坎1宮','水'),('傷門','木','坤2宮','土'),('傷門','木','艮8宮','土'),
    ('杜門','木','坤2宮','土'),('杜門','木','艮8宮','土'),('景門','火','乾6宮','金'),
    ('景門','火','兌7宮','金'),
]

print(f'  {"門":<6} {"門五行":<6} {"落宮":<8} {"宮五行":<6} {"驗證"}')
print('  ' + '-' * 40)
for men, men_wx, palace_name, palace_wx in MENPO_LIST:
    ke = WUXING_KE.get(men_wx) == palace_wx
    match = '✅' if ke else '❌'
    print(f'  {men:<6} {men_wx:<6} {palace_name:<8} {palace_wx:<6} {match}')

print(f'  含義: 不願繼續做、口不對心、行動受限')
print()

# ============================================================
print('=' * 70)
print('Section 7: 與之前集數對照 + 結論')
print('=' * 70)

print('1. 天乙定義: EP12追債=EP17官司 完全一致 ✅')
print('2. 用神體系: 官司6個用神=最多場景')
print('3. 格局庫: +飛干格+伏干格+刑格+六儀擊刑+五不遇時+門迫')
print('4. 庚: 最常見凶性符號（人體/大凶/飛伏干/刑格）')
print('5. 門場景化: 景門=訴狀、驚門=律師、開門=法院')
print('6. 反吟局官司=會上訴')
print()

NEW_GAPS = [
    ('G86','高','六儀擊刑僅6個原因','師傅未解釋','需研究'),
    ('G87','高','門迫影響程度','未知','需加權規則'),
    ('G88','中','飛干/伏干日干確定','測他人時替換?','需確認'),
    ('G89','中','五不遇時精確計算','需推算日時天干','需實現'),
    ('G90','low','門迫反義含義','宮剋門','需分類'),
    ('G91','low','反吟局場景含義','官司=上訴','需映射'),
]
for gid, priority, name, current, expected in NEW_GAPS:
    print(f'  [{priority}] {gid}: {name}')

print(f'\nEP17 核心貢獻:')
print(f'  1. 官司六用神+七步分析框架')
print(f'  2. 飛干格/伏干格/刑格')
print(f'  3. 六儀擊刑6個(全驗證✅)')
print(f'  4. 五不遇時10個(全驗證✅同性相剋)')
print(f'  5. 門迫13個(全驗證✅)')
print(f'  6. 反吟局官司=上訴')
print(f'  累計Gap: G01-G91')

# JSON
ep17_data = {
    "episode": 17, "title": "官司訴訟預測 + 常用凶格",
    "lawsuit_yongshen": {n: {"role": i["role"], "meaning": i["meaning"]} for n, i in LAWSUIT_YONGSHEN.items()},
    "liuyi_xing": LIUYI_XING,
    "wubuyushi": [{"day": d, "hour": h} for d, h in WUBUYUSHI],
    "menpo": [{"men": m, "men_wx": mw, "palace": pn, "palace_wx": pw} for m, mw, pn, pw in MENPO_LIST],
    "new_gaps": [{"id": g[0],"priority": g[1],"name": g[2]} for g in NEW_GAPS],
}
with open('/home/z/my-project/download/ep17_lawsuit_xiongge.json', 'w') as f:
    json.dump(ep17_data, f, ensure_ascii=False, indent=2)
print(f'\n→ 已輸出 /home/z/my-project/download/ep17_lawsuit_xiongge.json')
print('*' * 70)
print('  EP17 量化完成！')
print('*' * 70)
