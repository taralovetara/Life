#!/usr/bin/env python3
"""
EP02: 婚姻感情預測 + 流派辨析 量化
====================================
天心堂坤正師傅 第二集

本集新知識：
1. 轉盤 vs 飛盤 — 兩大流派
2. 時家奇門最重要（每2小時一變）
3. 用神系統：乙=妻、庚=夫、六合=婚姻
4. 天盤干為主、地盤干為輔
5. 通關機制（A剋B時，C可化解）
6. 運籌方法（方位擺設等）
"""

import json, sys

# 基礎數據（避免 import 問題）
PALACES = {
    1: {"name": "坎", "wuxing": "水"}, 2: {"name": "坤", "wuxing": "土"},
    3: {"name": "震", "wuxing": "木"}, 4: {"name": "巽", "wuxing": "木"},
    5: {"name": "中", "wuxing": "土"}, 6: {"name": "乾", "wuxing": "金"},
    7: {"name": "兌", "wuxing": "金"}, 8: {"name": "艮", "wuxing": "土"},
    9: {"name": "離", "wuxing": "火"},
}
WUXING_SHENG = {"金": "水", "水": "木", "木": "火", "火": "土", "土": "金"}
WUXING_KE   = {"金": "木", "木": "土", "土": "水", "水": "火", "火": "金"}
GONG_BAGUA = {1:'坎',2:'坤',3:'震',4:'巽',5:'中',6:'乾',7:'兌',8:'艮',9:'離'}

# ============================================================
# 一、轉盤 vs 飛盤 對照量化
# ============================================================

def section1_schools():
    print("=" * 65)
    print("  【一】轉盤 vs 飛盤 — 兩大流派對照")
    print("=" * 65)

    comparison = [
        ("起源", "東晉（抱樸子葛洪）", "清朝年間"),
        ("排布方式", "順/逆時針旋轉", "按九宮數字順序飛跳"),
        ("中五宮", "不用，宮空", "使用"),
        ("模擬對象", "星體自轉/公轉", "—"),
        ("學習資源", "較多", "較少"),
        ("坤正師傅選擇", "主修 ◄", "輔助"),
        ("現有引擎 engine.py", "✗ 非轉盤", "✓ 飛盤 ← 現行"),
    ]
    print(f"\n  {'維度':<12} {'轉盤奇門':<20} {'飛盤奇門':<20}")
    print(f"  {'─'*54}")
    for dim, zhuan, fei in comparison:
        print(f"  {dim:<12} {zhuan:<20} {fei:<20}")

    print("\n  ⚠️  關鍵發現：現有 engine.py 是飛盤邏輯！")
    print("      坤正師傅教的是轉盤奇門")
    print("      需要決定：繼續飛盤 or 改建轉盤引擎？")

    return {
        "zhuanpan": {
            "origin": "東晉", "reference": "抱樸子", "zhong5_usage": False,
            "method": "rotation", "master_choice": "primary"
        },
        "feipan": {
            "origin": "清朝", "zhong5_usage": True,
            "method": "flying", "master_choice": "secondary"
        }
    }


# ============================================================
# 二、時間分類量化
# ============================================================

def section2_time_types():
    print("\n" + "=" * 65)
    print("  【二】奇門時間分類")
    print("=" * 65)

    time_types = [
        ("年家奇門", "年", "看一年大趨勢", "低", "年運、國運"),
        ("月家奇門", "月", "看一個月趨勢", "中", "月運"),
        ("日家奇門", "日", "看一日趨勢", "中高", "日運"),
        ("時家奇門", "時辰(2h)", "看具體事件", "最高 ◄", "求測問事（本頻道主修）"),
    ]
    print(f"\n  {'類型':<12} {'粒度':<12} {'用途':<18} {'精準度':<8} {'適用場景'}")
    print(f"  {'─'*70}")
    for name, grain, use, prec, scene in time_types:
        print(f"  {name:<12} {grain:<12} {use:<18} {prec:<8} {scene}")

    print("\n  Back Test 影響：時家奇門 = 每個交易日1個局（開盤時辰）")
    return time_types


# ============================================================
# 三、用神系統量化（對 back test 最重要）
# ============================================================

def section3_yongshen():
    print("\n" + "=" * 65)
    print("  【三】用神系統 — 婚姻感情")
    print("=" * 65)

    # 用神映射
    yongshen_marriage = {
        "乙": {
            "role": "太太（天盤乙）",
            "wuxing": "木",
            "source": "天干",
            "note": "陰木，柔順之象"
        },
        "庚": {
            "role": "先生（天盤庚）",
            "wuxing": "金",
            "source": "天干",
            "note": "陽金，剛健之象"
        },
        "六合": {
            "role": "婚姻關係",
            "wuxing": None,
            "source": "八神",
            "note": "合作、合夥、婚姻"
        },
    }

    print("\n  核心用神：")
    for k, v in yongshen_marriage.items():
        print(f"    {k} → {v['role']}（{v['wuxing'] or '無五行'}）")

    # 乙庚關係
    print("\n  乙（木）vs 庚（金）的五行關係：")
    print("    金剋木 → 庚剋乙 → 先生剋太太（一般情況）")
    print("    但師傅例子中：天盤乙在巽4（木），天盤庚在艮8（土）")
    print("    木剋土 → 乙剋庚 → 太太剋先生（此例）")
    print("")
    print("    關鍵：不看天干本身的五行，看天干落宮的五行！")
    print("    判斷邏輯：天干落宮五行 → 宮位之間的生剋關係")

    # 量化規則
    print("\n  量化規則（用於 back test feature）：")
    rules = [
        ("天盤乙落宮五行 vs 天盤庚落宮五行", "夫妻力量對比"),
        ("乙庚關係：生/剋/同類", "誰主導婚姻"),
        ("六合落宮的吉凶", "婚姻整體狀態"),
        ("六合能否通關（乙生六合，六合生庚）", "婚姻能否維持"),
    ]
    for i, (rule, meaning) in enumerate(rules, 1):
        print(f"    R{i}. {rule}")
        print(f"        → {meaning}")

    return yongshen_marriage, rules


# ============================================================
# 四、通關機制量化
# ============================================================

def section4_tongguan():
    print("\n" + "=" * 65)
    print("  【四】通關機制量化")
    print("=" * 65)

    print("\n  通關定義：")
    print("    當 A 剋 B 時，如果存在 C 使得 A生C 且 C生B")
    print("    則 C 成為橋樑，將剋的關係轉化為相生")

    print("\n  師傅例子：")
    print("    太太（乙/木）剋 先生（庚/土）→ 婚姻有危機")
    print("    六合在離9宮（火）")
    print("    木生火（太太生六合）且 火生土（六合生先生）")
    print("    六合 = 通關者 → 婚姻不會出大問題")

    # 通關算法
    WUXING_SHENG = {"金": "水", "水": "木", "木": "火", "火": "土", "土": "金"}
    WUXING_KE   = {"金": "木", "木": "土", "土": "水", "水": "火", "火": "金"}

    def find_tongguan(wx_a, wx_b):
        """找出能通關 A→B 剋關係的五行"""
        bridges = []
        if WUXING_KE.get(wx_a) == wx_b:  # A 剋 B
            for c in ["金", "木", "水", "火", "土"]:
                if c != wx_a and c != wx_b:
                    if WUXING_SHENG.get(wx_a) == c and WUXING_SHENG.get(c) == wx_b:
                        bridges.append(c)
        return bridges

    print("\n  通關查找算法 — 全部 10 組剋關係的通關者：")
    tested = set()
    for a in ["金", "木", "水", "火", "土"]:
        for b in ["金", "木", "水", "火", "土"]:
            if a == b: continue
            key = (a, b)
            if key in tested: continue
            tested.add(key)
            bridges = find_tongguan(a, b)
            if WUXING_KE.get(a) == b and bridges:
                print(f"    {a}剋{b} → 通關者：{', '.join(bridges)}")
            elif WUXING_KE.get(a) == b and not bridges:
                print(f"    {a}剋{b} → 無通關者（直接剋，無緩衝）")

    return find_tongguan


# ============================================================
# 五、天盤干 vs 地盤干 的量化意義
# ============================================================

def section5_tian_vs_di():
    print("\n" + "=" * 65)
    print("  【五】天盤干 vs 地盤干 — 量化意義")
    print("=" * 65)

    print("\n  師傅明確：天盤干是主角，地盤干是配角（輔助）")
    print("")
    print("  量化影響：")
    print("    1. 計算用神時只用天盤干的位置和五行")
    print("    2. 地盤干可用作輔助判斷（如：天干入墓等）")
    print("    3. Back test feature 應以天盤干為主")

    print("\n  現有引擎對照：")
    print("    engine.py palace_score() 用天盤干(t_gan)和地盤干(d_gan)")
    print("    評分中 WX_SK 是天干vs地盤干的生剋 → 需要權重調整")
    print("    建議：天盤干權重 1.0，地盤干權重 0.3")

    return {"tianpan_weight": 1.0, "dipan_weight": 0.3}


# ============================================================
# 六、運籌方法量化
# ============================================================

def section6_yunchou():
    print("\n" + "=" * 65)
    print("  【六】運籌方法量化（婚姻感情）")
    print("=" * 65)

    print("\n  師傅提供的運籌建議：")
    print("    1. 行為層面：加強溝通、改變相處模式")
    print("    2. 環境層面（催旺婚姻）：")
    print("       - 正南位（離9宮/火）擺放：和合二仙 / 粉色水晶球 / 新鮮鮮花")
    print("       - 鮮花必須及時更換，凋謝會有反效果")

    print("\n  量化意義：")
    print("    - 運籌是「改變結果」的行動，不是「預測結果」的計算")
    print("    - Back test 只能測試「預測」部分，不能測試「運籌」效果")
    print("    - 但運籌概念印證了奇門 = 運籌學（做/唔做 + 點樣做）")

    yunchou_data = {
        "marriage": {
            "principle": "勸和勸合",
            "proverb": "寧教人打仔，莫教人分妻",
            "behavior": ["加強溝通", "雙方調整", "坦誠表達"],
            "fengshui": {
                "direction": "正南（離9宮）",
                "items": ["和合二仙", "粉色水晶球", "新鮮鮮花"],
                "note": "選一種即可，鮮花需及時更換"
            }
        }
    }
    return yunchou_data


# ============================================================
# 七、師傅例子的完整量化重現
# ============================================================

def section7_example_replay():
    print("\n" + "=" * 65)
    print("  【七】師傅例子量化重現（2021-06-30 14:30）")
    print("=" * 65)

    from datetime import datetime
    sys.path.insert(0, '/tmp/life-check')
    from qimen.engine import qiju
    try:
        r = qiju(datetime(2021, 6, 30, 14, 30))
    except Exception as e:
        print(f"    ⚠️ 引擎不支援跨年日期（G04: 節氣近似值問題）: {e}")
        print("    用 2026-06-30 14:30 替代展示：")
        r = qiju(datetime(2026, 6, 30, 14, 30))

    print(f"\n  起局：{r['dgz']} {r['sgz']}")
    print(f"  {'陽遁' if r['yang'] else '陰遁'}{r['ju']}局 {r['yuan']}")

    # 找天盤乙和天盤庚
    print("\n  天盤干分佈：")
    yi_palace = None
    geng_palace = None
    for p in range(1, 10):
        tg = r['tg'].get(p, '')
        if tg == '乙':
            yi_palace = p
            print(f"    天盤乙 → {GONG_BAGUA[p]}{p}宮（{r['tp'].get(p,'')} / {r['rp'].get(p,'')} / {r['sp'].get(p,'')}）")
        if tg == '庚':
            geng_palace = p
            print(f"    天盤庚 → {GONG_BAGUA[p]}{p}宮（{r['tp'].get(p,'')} / {r['rp'].get(p,'')} / {r['sp'].get(p,'')}）")

    # 找六合
    liuhe_palace = None
    for p in range(1, 10):
        if r['sp'].get(p) == '六合':
            liuhe_palace = p
            print(f"    六合   → {GONG_BAGUA[p]}{p}宮（{r['tp'].get(p,'')} / {r['rp'].get(p,'')}）")

    # 量化判斷
    print("\n  量化判斷：")
    if yi_palace and geng_palace:
        yi_wx = PALACES[yi_palace]["wuxing"]
        geng_wx = PALACES[geng_palace]["wuxing"]
        print(f"    太太（乙）落{GONG_BAGUA[yi_palace]}{yi_palace}宮 → 五行={yi_wx}")
        print(f"    先生（庚）落{GONG_BAGUA[geng_palace]}{geng_palace}宮 → 五行={geng_wx}")

        # 生剋判斷
        if WUXING_KE.get(yi_wx) == geng_wx:
            print(f"    {yi_wx}剋{geng_wx} → 太太剋先生（太太主導）")
        elif WUXING_SHENG.get(yi_wx) == geng_wx:
            print(f"    {yi_wx}生{geng_wx} → 太太生先生（太太付出）")
        elif yi_wx == geng_wx:
            print(f"    同屬{yi_wx} → 平等關係")
        else:
            print(f"    {geng_wx}剋{yi_wx} → 先生剋太太（先生主導）")

    # 通關判斷
    if liuhe_palace and yi_palace and geng_palace:
        lh_wx = PALACES[liuhe_palace]["wuxing"]
        yi_wx = PALACES[yi_palace]["wuxing"]
        geng_wx = PALACES[geng_palace]["wuxing"]
        tongguan = (WUXING_SHENG.get(yi_wx) == lh_wx and
                    WUXING_SHENG.get(lh_wx) == geng_wx)
        print(f"\n    六合在{GONG_BAGUA[liuhe_palace]}{liuhe_palace}宮 → 五行={lh_wx}")
        if tongguan:
            print(f"    通關成立！{yi_wx}生{lh_wx}生{geng_wx} → 婚姻有緩衝")
        else:
            print(f"    通關不成立 → 無緩衝")

    return r


# ============================================================
# 主程式
# ============================================================

if __name__ == "__main__":
    print()
    print("*" * 65)
    print("  EP02: 婚姻感情預測 + 流派辨析 量化")
    print("  資料來源：天心堂坤正師傅 第二集")
    print("*" * 65)

    schools = section1_schools()
    time_types = section2_time_types()
    yongshen, rules = section3_yongshen()
    tongguan_fn = section4_tongguan()
    weights = section5_tian_vs_di()
    yunchou = section6_yunchou()
    example = section7_example_replay()

    # 輸出 JSON
    ep02_data = {
        "episode": 2,
        "title": "婚姻感情預測 + 流派辨析",
        "schools": schools,
        "time_types": [{"name":t[0],"grain":t[1],"use":t[2],"precision":t[3],"scene":t[4]} for t in time_types],
        "yongshen_marriage": yongshen,
        "yongshen_rules": rules,
        "tian_vs_di_weights": weights,
        "yunchou": yunchou,
    }
    with open("/home/z/my-project/download/ep02_marriage.json", "w") as f:
        json.dump(ep02_data, f, ensure_ascii=False, indent=2)

    print("\n" + "*" * 65)
    print("  分析完成！")
    print("  輸出：/home/z/my-project/download/ep02_marriage.json")
    print("*" * 65)
