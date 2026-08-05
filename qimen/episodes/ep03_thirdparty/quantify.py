#!/usr/bin/env python3
"""
EP03: 第三者偵測 + 四維模型結構 量化
====================================
天心堂坤正師傅 第三集
"""

import json, sys
sys.path.insert(0, '/tmp/life-check')

PALACES = {
    1: {"name": "坎", "wuxing": "水"}, 2: {"name": "坤", "wuxing": "土"},
    3: {"name": "震", "wuxing": "木"}, 4: {"name": "巽", "wuxing": "木"},
    5: {"name": "中", "wuxing": "土"}, 6: {"name": "乾", "wuxing": "金"},
    7: {"name": "兌", "wuxing": "金"}, 8: {"name": "艮", "wuxing": "土"},
    9: {"name": "離", "wuxing": "火"},
}
WUXING_SHENG = {"金": "水", "水": "木", "木": "火", "火": "土", "土": "金"}
WUXING_KE   = {"金": "木", "木": "土", "土": "水", "水": "火", "火": "金"}

def main():
    print("\n" + "=" * 65)
    print("  EP03: 第三者偵測 + 四維模型結構 量化")
    print("  資料來源：天心堂坤正師傅 第三集")
    print("=" * 65)

    # 一、四維模型
    print("\n【一】四維立體模型（天地人神）")
    model = [
        ("天盤（九星）", "天時", "每時辰"),
        ("地盤（八卦）", "地利", "每5日"),
        ("人盤（八門）", "人和", "每時辰"),
        ("神盤（八神）", "神助", "每時辰"),
    ]
    print(f"  {'層':<16} {'代表':<8} {'變化週期'}")
    print(f"  {'─'*42}")
    for layer, rep, cycle in model:
        print(f"  {layer:<16} {rep:<8} {cycle}")
    print("\n  紀曉嵐：奇門遁甲是眾多術數中最有理法的一種")

    # 二、第三者偵測算法
    print("\n【二】第三者偵測算法（兩步驗證）")
    print("\n  用神擴展：丙=男性第三者, 丁=女性第三者")
    print("\n  算法（以測先生有無女第三者為例）：")
    print("  Step 1: 先生宮位(庚所在宮)的地盤干 = 丁?")
    print("  Step 2: 第三者宮位(天盤丁所在宮)五行 生 先生宮位五行?")
    print("  兩步都成立 → 確認有第三者（第三者仰慕被測者）")

    # 師傅個案驗證
    print("\n  師傅個案驗證：")
    print("  先生(庚)在乾6宮, 地盤干=丁 → Step 1 ✓")
    print("  天盤丁在艮8宮(土), 先生在乾6宮(金)")
    print("  土生金 → Step 2 ✓ → 確認有第三者 ✓")

    # 三、地盤干修正
    print("\n【三】地盤干重要性修正（G18細化）")
    print("  EP02: 天盤干為主, 地盤干為輔")
    print("  EP03: 地盤干在第三者偵測中是關鍵線索!")
    print("  修正: 地盤干唔係『不重要』, 而是『用途不同』")
    print("    性格分析 → 天盤干為主")
    print("    第三者偵測 → 地盤干是Step 1關鍵")

    # 四、符號解讀規則
    print("\n【四】宮位符號組合 → 性格/狀態解讀")
    rules = [
        ("開門", "開朗、不隱藏、直來直去"),
        ("杜門", "封閉、隱藏心思"),
        ("驚門", "爭執、吵鬧"),
        ("死門", "固執、不開心"),
        ("白虎", "兇猛、脾氣大"),
        ("太陰", "隱秘、暗地裡"),
        ("值符", "高端、有地位"),
        ("天芮星", "問題、隱患"),
        ("天心星", "有心計、善策劃"),
        ("天任星", "有責任心"),
    ]
    print(f"  {'符號':<10} {'含義'}")
    print(f"  {'─'*45}")
    for sym, meaning in rules:
        print(f"  {sym:<10} {meaning}")

    # 五、Back Test 意義
    print("\n【五】對 Back Test 嘅量化意義")
    print("  1. 四層輪盤完全正確（師傅確認天地人神）")
    print("  2. 用神系統持續擴展中")
    print("  3. 地盤干權重需要場景化，不能一刀切")
    print("  4. 奇門=讀取時空點全息信息 → 二元決策")

    # JSON
    ep03 = {
        "episode": 3, "title": "第三者偵測 + 四維模型結構",
        "yongshen_expanded": {"丙": "男性第三者", "丁": "女性第三者"},
        "third_party_algo": {
            "step1": "被測者宮位地盤干 = 第三者天干",
            "step2": "第三者宮位五行 生 被測者宮位五行",
        },
        "symbol_meanings": {r[0]: r[1] for r in rules},
        "dipan_revision": "地盤干用途不同，非權重問題",
    }
    with open("/home/z/my-project/download/ep03_thirdparty.json", "w") as f:
        json.dump(ep03, f, ensure_ascii=False, indent=2)
    print("\n  輸出：ep03_thirdparty.json")
    print("\n" + "*" * 65)

if __name__ == "__main__":
    main()
