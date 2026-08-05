#!/usr/bin/env python3
"""
奇門遁甲基礎框架量化 — 基於天心堂坤正師傅第一集
=============================================
將九宮八卦、五行生剋、天干地支等基礎結構
全部轉化為可計算的數學矩陣和評分系統
"""

import numpy as np
import json
from collections import OrderedDict

# ============================================================
# 一、洛書九宮基礎結構
# ============================================================

# 洛書九宮格（標準排列）
# 巽4  離9  坤2
# 震3  中5  兌7
# 艮8  坎1  乾6

LUOSHU_GRID = np.array([
    [4, 9, 2],
    [3, 5, 7],
    [8, 1, 6]
])

PALACES = OrderedDict([
    (1, {"name": "坎", "wuxing": "水", "direction": "北"}),
    (2, {"name": "坤", "wuxing": "土", "direction": "西南"}),
    (3, {"name": "震", "wuxing": "木", "direction": "東"}),
    (4, {"name": "巽", "wuxing": "木", "direction": "東南"}),
    (5, {"name": "中", "wuxing": "土", "direction": "中"}),
    (6, {"name": "乾", "wuxing": "金", "direction": "西北"}),
    (7, {"name": "兌", "wuxing": "金", "direction": "西"}),
    (8, {"name": "艮", "wuxing": "土", "direction": "東北"}),
    (9, {"name": "離", "wuxing": "火", "direction": "南"}),
])

# ============================================================
# 二、五行系統
# ============================================================

WUXING_LIST = ["金", "木", "水", "火", "土"]

WUXING_SHENG = {"金": "水", "水": "木", "木": "火", "火": "土", "土": "金"}
WUXING_KE   = {"金": "木", "木": "土", "土": "水", "水": "火", "火": "金"}

# ============================================================
# 三、天干系統
# ============================================================

TIANGAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
TIANGAN_WUXING = {
    "甲": "木", "乙": "木", "丙": "火", "丁": "火",
    "戊": "土", "己": "土", "庚": "金", "辛": "金",
    "壬": "水", "癸": "水",
}
TIANGAN_YINYANG = {
    "甲": "陽", "乙": "陰", "丙": "陽", "丁": "陰",
    "戊": "陽", "己": "陰", "庚": "陽", "辛": "陰",
    "壬": "陽", "癸": "陰",
}
SANQI = ["乙", "丙", "丁"]       # 三奇
LIUYI = ["戊", "己", "庚", "辛", "壬", "癸"]  # 六儀
JIA_HIDDEN = {"甲子": "戊", "甲戌": "己", "甲申": "庚",
             "甲午": "辛", "甲辰": "壬", "甲寅": "癸"}

# ============================================================
# 四、地支系統
# ============================================================

DIZHI = ["子", "丑", "寅", "卯", "辰", "巳",
         "午", "未", "申", "酉", "戌", "亥"]
DIZHI_WUXING = {
    "子": "水", "丑": "土", "寅": "木", "卯": "木",
    "辰": "土", "巳": "火", "午": "火", "未": "土",
    "申": "金", "酉": "金", "戌": "土", "亥": "水",
}

# ============================================================
# 五、八門（人盤）
# ============================================================

BAMEN = OrderedDict([
    ("開門", {"wuxing": "金", "natal": 6, "nature": "吉", "desc": "開創、開始、開放"}),
    ("休門", {"wuxing": "水", "natal": 1, "nature": "吉", "desc": "休養、休息、和諧"}),
    ("生門", {"wuxing": "土", "natal": 8, "nature": "吉", "desc": "生機、生長、財利"}),
    ("傷門", {"wuxing": "木", "natal": 3, "nature": "凶", "desc": "傷害、破損、爭執"}),
    ("杜門", {"wuxing": "木", "natal": 4, "nature": "凶", "desc": "阻塞、隱藏、拒絕"}),
    ("景門", {"wuxing": "火", "natal": 9, "nature": "中平", "desc": "景象、文書、血光"}),
    ("死門", {"wuxing": "土", "natal": 2, "nature": "凶", "desc": "死亡、終結、阻塞"}),
    ("驚門", {"wuxing": "金", "natal": 7, "nature": "凶", "desc": "驚恐、官非、爭訟"}),
])

# ============================================================
# 六、九星（天盤）
# ============================================================

JIUXING = OrderedDict([
    ("天蓬星", {"wuxing": "水", "natal": 1, "nature": "凶", "desc": "盜賊、暗昧、智謀"}),
    ("天任星", {"wuxing": "土", "natal": 8, "nature": "吉", "desc": "忠厚、穩重、農業"}),
    ("天衝星", {"wuxing": "木", "natal": 3, "nature": "吉", "desc": "衝動、行動、武職"}),
    ("天輔星", {"wuxing": "木", "natal": 4, "nature": "吉", "desc": "輔助、文教、溫和"}),
    ("天英星", {"wuxing": "火", "natal": 9, "nature": "凶", "desc": "文明、血光、急躁"}),
    ("天芮星", {"wuxing": "土", "natal": 2, "nature": "凶", "desc": "疾病、問題、隱患"}),
    ("天柱星", {"wuxing": "金", "natal": 7, "nature": "凶", "desc": "驚恐、破敗、武將"}),
    ("天心星", {"wuxing": "金", "natal": 6, "nature": "吉", "desc": "醫藥、心計、統帥"}),
])

# ============================================================
# 七、八神（神盤）
# ============================================================

BASHEN = OrderedDict([
    ("值符",  {"nature": "吉", "desc": "貴人、領導、高端"}),
    ("騰蛇",  {"nature": "凶", "desc": "纏繞、虛驚、怪異"}),
    ("太陰",  {"nature": "吉", "desc": "陰暗、隱秘、策劃"}),
    ("六合",  {"nature": "吉", "desc": "合作、婚姻、合夥"}),
    ("白虎",  {"nature": "凶", "desc": "血光、兇猛、道路"}),
    ("玄武",  {"nature": "凶", "desc": "盜竊、欺騙、暗昧"}),
    ("九地",  {"nature": "吉", "desc": "柔順、守成、防禦"}),
    ("九天",  {"nature": "吉", "desc": "剛健、進取、高遠"}),
])

# ============================================================
# 量化分析函數
# ============================================================

def section1_luoshu():
    print("=" * 65)
    print("  【一】洛書九宮 — 數學性質驗證")
    print("=" * 65)
    print("\n洛書九宮格排列：")
    print("  巽4   離9   坤2")
    print("  震3   中5   兌7")
    print("  艮8   坎1   乾6")
    print()

    # 橫行和
    for i, row in enumerate(LUOSHU_GRID):
        print(f"  橫行{i+1}：{' + '.join(str(v) for v in row)} = {sum(row)}")
    # 直列和
    for j in range(3):
        col = LUOSHU_GRID[:, j]
        print(f"  直列{j+1}：{' + '.join(str(v) for v in col)} = {sum(col)}")
    # 對角線
    print(f"  主對角：{' + '.join(str(v) for v in np.diag(LUOSHU_GRID))} = {np.trace(LUOSHU_GRID)}")
    print(f"  副對角：{' + '.join(str(v) for v in np.diag(LUOSHU_GRID[::-1]))} = {np.trace(LUOSHU_GRID[::-1])}")

    print("\n對宮相加驗證（坤正師傅重點）：")
    for p1, p2 in [(1,9),(2,8),(3,7),(4,6)]:
        print(f"  {PALACES[p1]['name']}{p1} + {PALACES[p2]['name']}{p2} = {p1}+{p2} = {p1+p2}  {'✓' if p1+p2==10 else '✗'}")
    print(f"  中五宮：獨立，無對宮")

    print("\n五行宮位分佈：")
    from collections import Counter
    wx_cnt = Counter(v["wuxing"] for v in PALACES.values())
    for wx in WUXING_LIST:
        pal_list = [f"{PALACES[k]['name']}{k}" for k,v in PALACES.items() if v["wuxing"]==wx]
        print(f"  {wx}（{wx_cnt[wx]}宮）：{', '.join(pal_list)}")
    print("\n  坤正師傅解釋：火水各1宮（太多成災），金木各2宮，土3宮（萬物之母）")


def section2_wuxing_matrix():
    print("\n" + "=" * 65)
    print("  【二】五行生剋關係矩陣（5×5）")
    print("=" * 65)

    n = len(WUXING_LIST)
    # +2=我生(洩) +1=我剋(耗) 0=同類 -1=剋我 -2=生我(得生)
    M = np.zeros((n, n), dtype=int)
    for i, a in enumerate(WUXING_LIST):
        for j, b in enumerate(WUXING_LIST):
            if a == b: M[i][j] = 0
            elif WUXING_SHENG.get(a) == b: M[i][j] = 2   # 我生
            elif WUXING_KE.get(a) == b:   M[i][j] = 1   # 我剋
            elif WUXING_SHENG.get(b) == a: M[i][j] = -2  # 生我
            elif WUXING_KE.get(b) == a:   M[i][j] = -1  # 剋我

    print("\n  +2=我生(洩氣)  +1=我剋(耗氣)  0=同類  -1=剋我(受制)  -2=生我(得生)")
    header = "        " + "  ".join(f"{wx:>5}" for wx in WUXING_LIST)
    print(header)
    for i, wx in enumerate(WUXING_LIST):
        row = "  " + "  ".join(f"{M[i][j]:+5d}" for j in range(n))
        print(f"  {wx:>5} {row}")

    # 輸出 JSON 供後續使用
    data = {"wuxing_list": WUXING_LIST, "matrix": M.tolist()}
    with open("/home/z/my-project/download/wuxing_matrix.json", "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("\n  → 已輸出 wuxing_matrix.json")
    return M


def section3_palace_matrix(wx_matrix):
    print("\n" + "=" * 65)
    print("  【三】宮位間五行生剋矩陣（9×9）")
    print("=" * 65)

    palace_wx = [PALACES[i]["wuxing"] for i in range(1, 10)]
    palace_nm = [f"{PALACES[i]['name']}{i}" for i in range(1, 10)]
    wx_idx = {wx: i for i, wx in enumerate(WUXING_LIST)}

    PM = np.zeros((9, 9), dtype=int)
    for i in range(9):
        for j in range(9):
            if i != j:
                PM[i][j] = wx_matrix[wx_idx[palace_wx[i]]][wx_idx[palace_wx[j]]]

    header = "          " + "  ".join(f"{nm:>6}" for nm in palace_nm)
    print(header)
    for i in range(9):
        row = "  " + "  ".join(f"{PM[i][j]:+6d}" for j in range(9))
        print(f"  {palace_nm[i]:>6} {row}")

    # 重點：離9宮嘅關係
    print("\n  重點分析：離9宮（火）與其他宮位的關係：")
    li_row = PM[8, :]  # index 8 = 離9
    for j in range(9):
        rel = li_row[j]
        if rel == 0: continue
        tag = {2: "我生(洩)", 1: "我剋(耗)", -1: "剋我(受制)", -2: "生我(得生)"}.get(rel, "")
        print(f"    離9 → {palace_nm[j]}：{rel:+d}  {tag}")

    return PM


def section4_four_layers():
    print("\n" + "=" * 65)
    print("  【四】奇門四層輪盤結構總覽")
    print("=" * 65)

    layers = [
        ("天盤（九星）", JIUXING, "wuxing", "natal"),
        ("地盤（宮位）", {k: v for k, v in PALACES.items()}, "wuxing", None),
        ("人盤（八門）", BAMEN, "wuxing", "natal"),
        ("神盤（八神）", BASHEN, "nature", None),
    ]

    for layer_name, items, wx_key, natal_key in layers:
        print(f"\n  {layer_name}：")
        print(f"  {'名稱':>10}  {'五行/性質':>8}  {'本宮':>4}  {'吉凶':>4}  說明")
        print(f"  {'─'*60}")
        for name, info in items.items():
            wx_val = info.get(wx_key, "-")
            natal = info.get(natal_key, "-" if natal_key else "-")
            nature = info.get("nature", "-")
            desc = info.get("desc", "-")
            print(f"  {name:>10}  {str(wx_val):>8}  {str(natal):>4}  {str(nature):>4}  {desc}")


def section5_tiangan():
    print("\n" + "=" * 65)
    print("  【五】天干結構量化（三奇六儀）")
    print("=" * 65)

    print(f"\n  {'天干':>4}  {'五行':>4}  {'陰陽':>4}  {'奇門角色':>10}  {'甲遁':>6}")
    print(f"  {'─'*45}")
    for tg in TIANGAN:
        role = "三奇" if tg in SANQI else ("六儀(遁甲)" if tg in LIUYI else "隱藏")
        jia_hide = ""
        for jk, jv in JIA_HIDDEN.items():
            if jv == tg:
                jia_hide = f"遁{jk}"
                break
        print(f"  {tg:>4}  {TIANGAN_WUXING[tg]:>4}  {TIANGAN_YINYANG[tg]:>4}  {role:>10}  {jia_hide:>6}")

    # 天干五行分佈
    from collections import Counter
    print("\n  天干五行分佈：")
    tg_cnt = Counter(TIANGAN_WUXING[tg] for tg in TIANGAN)
    for wx in WUXING_LIST:
        tgs = [tg for tg in TIANGAN if TIANGAN_WUXING[tg] == wx]
        print(f"    {wx}（{tg_cnt[wx]}個）：{', '.join(tgs)}")


def section6_scoring_system():
    print("\n" + "=" * 65)
    print("  【六】量化評分系統設計")
    print("=" * 65)

    # 五行稀缺性權重
    wuxing_count = {}
    for v in PALACES.values():
        wuxing_count[v["wuxing"]] = wuxing_count.get(v["wuxing"], 0) + 1
    wuxing_weight = {}
    for wx in WUXING_LIST:
        cnt = wuxing_count.get(wx, 0)
        wuxing_weight[wx] = round(3.0 / cnt, 2)  # 反比

    print("\n  五行稀缺性權重（宮位數量反比）：")
    for wx in WUXING_LIST:
        print(f"    {wx}：{wuxing_count[wx]}宮 → 權重 {wuxing_weight[wx]}")

    # 八門吉凶評分
    print("\n  八門吉凶評分：")
    men_score = {"吉": +1, "凶": -1, "中平": 0}
    for name, info in BAMEN.items():
        s = men_score[info["nature"]]
        wx_match = ""  # 得地/失地留空，需要具體宮位才知道
        print(f"    {name}（{info['wuxing']}，本宮{info['natal']}）：{info['nature']} → 基礎分 {s:+d}")

    # 九星吉凶評分
    print("\n  九星吉凶評分：")
    for name, info in JIUXING.items():
        s = men_score[info["nature"]]
        print(f"    {name}（{info['wuxing']}，本宮{info['natal']}）：{info['nature']} → 基礎分 {s:+d}")

    # 八神吉凶評分
    print("\n  八神吉凶評分：")
    for name, info in BASHEN.items():
        s = men_score[info["nature"]]
        print(f"    {name}：{info['nature']} → 基礎分 {s:+d}")

    # 完整 JSON 輸出
    framework = {
        "palaces": {str(k): v for k, v in PALACES.items()},
        "wuxing_sheng": WUXING_SHENG,
        "wuxing_ke": WUXING_KE,
        "wuxing_weight": wuxing_weight,
        "bamen_score": {name: men_score[info["nature"]] for name, info in BAMEN.items()},
        "jiuxing_score": {name: men_score[info["nature"]] for name, info in JIUXING.items()},
        "bashen_score": {name: men_score[info["nature"]] for name, info in BASHEN.items()},
        "tiangan_wuxing": TIANGAN_WUXING,
        "tiangan_yinyang": TIANGAN_YINYANG,
        "sanqi": SANQI,
        "liuyi": LIUYI,
        "jia_hidden": JIA_HIDDEN,
        "dizhi_wuxing": DIZHI_WUXING,
    }
    with open("/home/z/my-project/download/qimen_framework.json", "w") as f:
        json.dump(framework, f, ensure_ascii=False, indent=2)
    print("\n  → 完整框架已輸出 qimen_framework.json")

    return framework


def section7_dediding_summary():
    print("\n" + "=" * 65)
    print("  【七】坤正師傅第一集要點 → 量化映射總結")
    print("=" * 65)

    mapping = [
        ("奇門 = 運籌學", "二元決策工具（做/唔做），唔係連續預測工具",
         "後續實驗應設計為分類問題（如：做/不做投資），非回歸問題（預測漲跌幅）"),
        ("用問事時間起局，唔需要八字", "事件驅動，每兩小時一變",
         "回測時需要定義『問事時間』的規則（如：每個交易日開盤時辰）"),
        ("九宮八卦 + 五行生剋", "宮位之間有明確的生剋量化關係",
         "已建構 9x9 宮位關係矩陣，可作為 feature engineering 基礎"),
        ("五行宮位數量不平衡", "火水各1、金木各2、土有3",
         "稀缺性權重：火=水=3.0, 金=木=1.5, 土=1.0，可用於加權評分"),
        ("天干為主，地支為輔", "天干決定三奇六儀的排列",
         "甲隱藏於六儀之下，實際操作中只有9個符號在八宮中飛布"),
    ]

    for i, (concept, meaning, quant_implication) in enumerate(mapping, 1):
        print(f"\n  {i}. {concept}")
        print(f"     含義：{meaning}")
        print(f"     量化意義：{quant_implication}")


# ============================================================
# 主程式
# ============================================================

if __name__ == "__main__":
    print()
    print("*" * 65)
    print("  奇門遁甲基礎框架量化分析")
    print("  資料來源：天心堂坤正師傅 第一集（入門基礎）")
    print("*" * 65)

    section1_luoshu()          # 洛書數學驗證
    wx_m = section2_wuxing_matrix()    # 五行生剋矩陣
    section3_palace_matrix(wx_m)       # 宮位關係矩陣
    section4_four_layers()             # 四層輪盤結構
    section5_tiangan()                 # 天干結構
    section6_scoring_system()          # 評分系統
    section7_dediding_summary()        # 總結

    print("\n" + "*" * 65)
    print("  分析完成！")
    print("  輸出文件：")
    print("    - /home/z/my-project/download/wuxing_matrix.json")
    print("    - /home/z/my-project/download/qimen_framework.json")
    print("*" * 65)
