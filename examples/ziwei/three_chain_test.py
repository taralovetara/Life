# -*- coding: utf-8 -*-
"""
三鏈測試：福德宮有效分 ↔ 保守程度 ↔ 股價回報

Chain 1: 福德宮有效分 ↔ 保守程度指數
Chain 2: 保守程度指數 ↔ 股價年度回報
Chain 3: 排除替代解釋（反壟斷政策等外部因素）

保守程度指數 = 標準化(回購金額) + 標準化(1/投資數量)
回購金額↑ = 保守；投資數量↓ = 保守
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
try:
    import yfinance as yf
    HAS_YF = True
except ImportError:
    HAS_YF = False

from ziwei.calculator import build_chart
from ziwei.timeline import get_liunian_sihua
from ziwei.scorer import score_palace
from ziwei.constants import STEMS, SIHUA_WEIGHTS, BRANCHES

# ============================================================
# 數據定義
# ============================================================

# 騰訊對外投資事件數量 (來源: IT桔子, 廣發證券研報, 21世紀經濟報導, 鳳凰網等交叉驗證)
# 注意: IT桔子有不同統計口徑 (全量 vs 公開披露), 以下取各報導最常引用嘅數字
INVESTMENT_COUNTS = {
    2005: 3,    2006: 5,    2007: 8,    2008: 6,
    2009: 12,   2010: 15,   2011: 22,   2012: 18,
    2013: 28,   2014: 36,   2015: 124,  2016: 73,
    2017: 140,  2018: 165,  2019: 122,  2020: 179,
    2021: 268,  2022: 92,   2023: 35,   2024: 50,
}

# 騰訊股份回購金額 (億港元, 來源: Wind, 騰訊年報, 財聯社)
# 2021年前騰訊基本無系統性回購, 記為0
BUYBACK_HKD = {
    2005: 0,    2006: 0,    2007: 0,    2008: 0,
    2009: 0,    2010: 0,    2011: 0,    2012: 0,
    2013: 0,    2014: 0,    2015: 0,    2016: 0,
    2017: 0,    2018: 0,    2019: 0,    2020: 0,
    2021: 26,   2022: 338,  2023: 490,  2024: 1120,
}

# 反壟斷政策虛擬變量 (1 = 政策收緊年, 0 = 正常年)
# 2020年底: 阿里螞蟻暫停IPO, 平台經濟反壟斷啟動
# 2021年: 騰訊被罰50萬, 音樂版塊被要求放棄獨家版權
# 2022年: 反壟斷持續, 騰訊減持京東/Sea等
# 2023年: 監管開始放鬆, 平台經濟常態化監管
# 2024年: 監管環境明顯好轉
ANTITRUST_DUMMY = {
    2005: 0, 2006: 0, 2007: 0, 2008: 0,
    2009: 0, 2010: 0, 2011: 0, 2012: 0,
    2013: 0, 2014: 0, 2015: 0, 2016: 0,
    2017: 0, 2018: 0, 2019: 0, 2020: 0.5,
    2021: 1, 2022: 1, 2023: 0.3, 2024: 0,
}


def get_fude_scores(years):
    """計算指定年份範圍嘅福德宮有效分數"""
    chart = build_chart(2004, 6, 16, 10, '男')
    fude_branch = None
    fude_palace = None
    for p in chart['palaces']:
        if p['name'] == '福德宮':
            fude_branch = p['branch_idx']
            fude_palace = p
            break
    base_score = score_palace(fude_palace)['total']

    scores = {}
    for year in years:
        ln = get_liunian_sihua(year)
        flow = 0.0
        for sihua_label, star_name in ln['sihua'].items():
            if chart['main_stars_pos'].get(star_name) == fude_branch:
                flow += SIHUA_WEIGHTS.get(sihua_label, 0)
        scores[year] = base_score + flow
    return scores


def get_stock_returns(years):
    """獲取騰訊年度股價回報 (0700.HK)"""
    if not HAS_YF:
        print("  ⚠️ yfinance 未安裝, 使用估計回報數據")
        # 備用: 手動輸入嘅年度回報%
        MANUAL = {
            2005: 30, 2006: 125, 2007: 155, 2008: -40,
            2009: 190, 2010: 22, 2011: -8, 2012: 32,
            2013: 15, 2014: 10, 2015: 22, 2016: 2,
            2017: 115, 2018: -25, 2019: 20, 2020: 50,
            2021: -19, 2022: -24, 2023: -2, 2024: 45,
        }
        return {y: MANUAL.get(y) for y in years}

    try:
        ticker = yf.Ticker("0700.HK")
        data = ticker.history(start="2004-12-31", end="2025-01-15", auto_adjust=True)
        returns = {}
        for year in years:
            y1 = f"{year-1}-12-31"
            y2 = f"{year}-12-31"
            p1 = data.loc[data.index <= y1, 'Close']
            p2 = data.loc[data.index <= y2, 'Close']
            if len(p1) > 0 and len(p2) > 0 and p1.iloc[-1] > 0:
                ret = (p2.iloc[-1] / p1.iloc[-1] - 1) * 100
                returns[year] = ret
        return returns
    except Exception as e:
        print(f"  ⚠️ yfinance 獲取失敗: {e}, 使用估計數據")
        MANUAL = {
            2005: 30, 2006: 125, 2007: 155, 2008: -40,
            2009: 190, 2010: 22, 2011: -8, 2012: 32,
            2013: 15, 2014: 10, 2015: 22, 2016: 2,
            2017: 115, 2018: -25, 2019: 20, 2020: 50,
            2021: -19, 2022: -24, 2023: -2, 2024: 45,
        }
        return {y: MANUAL.get(y) for y in years}


def pearson_r(x, y):
    """計算 Pearson r 和 p-value"""
    n = len(x)
    if n < 3:
        return 0, 1
    r = np.corrcoef(x, y)[0, 1]
    if abs(r) >= 1:
        return r, 0
    t = r * np.sqrt((n - 2) / (1 - r**2))
    # 兩尾 p-value (近似)
    from math import sqrt
    # 簡化 p-value 估計 (雙尾, t 分佈近似)
    import scipy.stats as stats
    p = 2 * (1 - stats.t.cdf(abs(t), df=n - 2))
    return r, p


def partial_corr(x, y, z):
    """計算偏相關: 控制 z 之後, x 同 y 嘅相關性"""
    n = len(x)
    if n < 5:
        return 0, 1
    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)
    z = np.array(z, dtype=float)
    # 偏相關公式
    rxz, _ = pearson_r(x, z)
    ryz, _ = pearson_r(y, z)
    rxy, _ = pearson_r(x, y)
    from math import sqrt
    denom = sqrt(max(0, (1 - rxz**2) * (1 - ryz**2)))
    if denom < 1e-10:
        return 0, 1
    pr = (rxy - rxz * ryz) / denom
    # 近似 p-value
    t = pr * sqrt((n - 3) / max(1 - pr**2, 1e-10))
    import scipy.stats as stats
    p = 2 * (1 - stats.t.cdf(abs(t), df=n - 3))
    return pr, p


def main():
    years = list(range(2005, 2025))  # 20年數據

    print(f"\n{'='*110}")
    print(f"  騰訊三鏈測試：福德宮有效分 ↔ 保守程度指數 ↔ 股價回報")
    print(f"  假說: 福德宮高分 → 保守操作(回購↑+投資↓) → 股價跌")
    print(f"  數據範圍: {years[0]}-{years[-1]} (共{len(years)}年)")
    print(f"{'='*110}")

    # --- Step 1: 計算福德宮有效分 ---
    print(f"\n  Step 1: 計算福德宮有效分...")
    fude_scores = get_fude_scores(years)

    # --- Step 2: 獲取股價回報 ---
    print(f"  Step 2: 獲取股價年度回報...")
    stock_returns = get_stock_returns(years)

    # --- Step 3: 構建保守程度指數 ---
    # 只用有回購數據嘅年份 (2021-2024) + 投資數據完整嘅年份
    # 為擴大樣本, 我哋用全部20年, 回購2021前為0
    print(f"  Step 3: 構建保守程度指數...")

    # 保守程度指數 = z(回購金額) + z(1/投資數量)
    # z = (x - mean) / std, 但如果 std=0 則 z=0
    inv_vals = np.array([INVESTMENT_COUNTS.get(y, np.nan) for y in years], dtype=float)
    bb_vals = np.array([BUYBACK_HKD.get(y, 0) for y in years], dtype=float)

    # 1/投資數量 (投資越少越保守)
    inv_inverse = np.where(inv_vals > 0, 1.0 / inv_vals, 0)

    # 標準化
    def zscore(arr):
        m, s = np.nanmean(arr), np.nanstd(arr)
        if s < 1e-10:
            return np.zeros_like(arr)
        return (arr - m) / s

    z_bb = zscore(bb_vals)
    z_inv = zscore(inv_inverse)
    conservatism = z_bb + z_inv  # 保守程度指數, 越高越保守

    # --- 顯示完整數據表 ---
    print(f"\n{'='*110}")
    print(f"  完整數據表")
    print(f"{'='*110}")
    print(f"  {'年份':>4s}  {'天干':>2s}  {'福德分':>6s}  {'投資數':>6s}  {'回購(億HKD)':>12s}  {'z(回購)':>7s}  {'z(1/投資)':>9s}  {'保守指數':>8s}  {'股價回報%':>10s}  {'反壟斷':>6s}")
    print(f"  {'-'*100}")

    data_rows = []
    for i, year in enumerate(years):
        sc = fude_scores[year]
        stem = STEMS[(year - 4) % 10]
        inv = INVESTMENT_COUNTS.get(year, np.nan)
        bb = BUYBACK_HKD.get(year, 0)
        ret = stock_returns.get(year, np.nan)
        at = ANTITRUST_DUMMY.get(year, 0)

        inv_s = f"{inv:>6.0f}" if not np.isnan(inv) else "  N/A"
        bb_s = f"{bb:>10.0f}" if bb > 0 else "       0"
        ret_s = f"{ret:>+9.1f}%" if not np.isnan(ret) else "     N/A"
        at_s = f"{at:>5.1f}" if at > 0 else "   0"

        print(f"  {year:>4d}  {stem:>2s}  {sc:>6.1f}  {inv_s}  {bb_s}  {z_bb[i]:>+7.2f}  {z_inv[i]:>+9.2f}  {conservatism[i]:>+8.2f}  {ret_s}  {at_s}")

        if not np.isnan(inv) and not np.isnan(ret):
            data_rows.append({
                'year': year, 'fude': sc, 'inv': inv,
                'bb': bb, 'conservatism': conservatism[i],
                'return': ret, 'antitrust': at
            })

    n_valid = len(data_rows)
    print(f"\n  有效數據點: {n_valid} 年")

    # ============================================================
    # CHAIN 1: 福德宮有效分 ↔ 保守程度指數
    # ============================================================
    print(f"\n{'='*110}")
    print(f"  ══ CHAIN 1: 福德宮有效分 ↔ 保守程度指數 ══")
    print(f"  假說: 福德宮有效分越高 → 保守程度越高")
    print(f"  預期: r > 0 (正相關)")
    print(f"{'='*110}")

    fude_arr = np.array([r['fude'] for r in data_rows])
    cons_arr = np.array([r['conservatism'] for r in data_rows])
    inv_arr = np.array([r['inv'] for r in data_rows])
    bb_arr = np.array([r['bb'] for r in data_rows])
    ret_arr = np.array([r['return'] for r in data_rows])
    at_arr = np.array([r['antitrust'] for r in data_rows])

    # 1a: 福德宮 vs 保守程度總指數
    r1, p1 = pearson_r(fude_arr, cons_arr)
    print(f"\n  1a. 福德宮有效分 vs 保守程度指數 (全20年)")
    print(f"      r = {r1:>+5.3f}, p = {p1:.4f}, n = {n_valid}")
    sig1 = '✅ 顯著' if p1 < 0.05 else '❌ 不顯著'
    dir1 = '正相關 ✅' if r1 > 0 else '負相關 ❌'
    print(f"      方向: {dir1}, 顯著性: {sig1}")

    # 1b: 福德宮 vs 投資數量 (負相關 = 支持)
    r1b, p1b = pearson_r(fude_arr, inv_arr)
    print(f"\n  1b. 福德宮有效分 vs 投資數量 (預期 r < 0)")
    print(f"      r = {r1b:>+5.3f}, p = {p1b:.4f}")
    sig1b = '✅ 顯著' if p1b < 0.05 else '❌ 不顯著'
    dir1b = '負相關 ✅ (投資少=保守)' if r1b < 0 else '正相關 ❌'
    print(f"      方向: {dir1b}, 顯著性: {sig1b}")

    # 1c: 福德宮 vs 回購金額 (正相關 = 支持, 但只2021-2024有數據)
    # 用全部年份 (2021前回購=0)
    r1c, p1c = pearson_r(fude_arr, bb_arr)
    print(f"\n  1c. 福德宮有效分 vs 回購金額 (預期 r > 0, 2021前=0)")
    print(f"      r = {r1c:>+5.3f}, p = {p1c:.4f}")
    sig1c = '✅ 顯著' if p1c < 0.05 else '❌ 不顯著'
    dir1c = '正相關 ✅ (回購多=保守)' if r1c > 0 else '負相關 ❌'
    print(f"      方向: {dir1c}, 顯著性: {sig1c}")

    # ============================================================
    # CHAIN 2: 保守程度指數 ↔ 股價年度回報
    # ============================================================
    print(f"\n{'='*110}")
    print(f"  ══ CHAIN 2: 保守程度指數 ↔ 股價年度回報 ══")
    print(f"  假說: 保守程度越高 → 股價回報越低")
    print(f"  預期: r < 0 (負相關)")
    print(f"{'='*110}")

    r2, p2 = pearson_r(cons_arr, ret_arr)
    print(f"\n  2a. 保守程度指數 vs 股價年度回報")
    print(f"      r = {r2:>+5.3f}, p = {p2:.4f}, n = {n_valid}")
    sig2 = '✅ 顯著' if p2 < 0.05 else '❌ 不顯著'
    dir2 = '負相關 ✅ (保守→股價跌)' if r2 < 0 else '正相關 ❌'
    print(f"      方向: {dir2}, 顯著性: {sig2}")

    # 2b: 回購金額 vs 股價回報 (正相關? 反而?)
    r2b, p2b = pearson_r(bb_arr, ret_arr)
    print(f"\n  2b. 回購金額 vs 股價年度回報 (回購多→股價?)")
    print(f"      r = {r2b:>+5.3f}, p = {p2b:.4f}")

    # 2c: 投資數量 vs 股價回報
    r2c, p2c = pearson_r(inv_arr, ret_arr)
    print(f"\n  2c. 投資數量 vs 股價年度回報 (投資多→股價?)")
    print(f"      r = {r2c:>+5.3f}, p = {p2c:.4f}")

    # HIGH/LOW 分組對比
    med_cons = np.median(cons_arr)
    hi_idx = cons_arr >= med_cons
    lo_idx = ~hi_idx
    hi_ret = ret_arr[hi_idx]
    lo_ret = ret_arr[lo_idx]
    print(f"\n  2d. 分組對比 (以保守程度中位數 {med_cons:.2f} 分界)")
    print(f"      HIGH保守組 ({int(hi_idx.sum())}年): 平均回報 {np.mean(hi_ret):>+7.1f}%")
    print(f"      LOW 保守組 ({int(lo_idx.sum())}年): 平均回報 {np.mean(lo_ret):>+7.1f}%")
    print(f"      差異: {np.mean(hi_ret) - np.mean(lo_ret):>+7.1f}%")
    diff_dir = '✅ 支持' if np.mean(hi_ret) < np.mean(lo_ret) else '❌ 反駁'
    print(f"      {diff_dir}假說 (HIGH保守→回報低)")

    # ============================================================
    # CHAIN 3: 排除替代解釋
    # ============================================================
    print(f"\n{'='*110}")
    print(f"  ══ CHAIN 3: 排除替代解釋（反壟斷政策等外部因素） ══")
    print(f"  方法: 偏相關分析, 控制反壟斷虛擬變量之後")
    print(f"  如果偏相關仍然顯著 → 紫微斗數效應獨立於政策因素")
    print(f"{'='*110}")

    # 3a: 控制反壟斷後, 福德宮 vs 保守程度
    pr3a, pp3a = partial_corr(fude_arr, cons_arr, at_arr)
    print(f"\n  3a. 福德宮 vs 保守程度 (控制反壟斷後)")
    print(f"      原始 r = {r1:>+5.3f}")
    print(f"      偏相關 r = {pr3a:>+5.3f}, p = {pp3a:.4f}")
    drop3a = abs(r1) - abs(pr3a)
    print(f"      相關下降: {drop3a:.3f} ({'大幅下降→政策係主因' if drop3a > 0.2 else '輕微下降→政策非主因'})")

    # 3b: 控制反壟斷後, 保守程度 vs 股價
    pr3b, pp3b = partial_corr(cons_arr, ret_arr, at_arr)
    print(f"\n  3b. 保守程度 vs 股價回報 (控制反壟斷後)")
    print(f"      原始 r = {r2:>+5.3f}")
    print(f"      偏相關 r = {pr3b:>+5.3f}, p = {pp3b:.4f}")
    drop3b = abs(r2) - abs(pr3b)
    print(f"      相關下降: {drop3b:.3f} ({'大幅下降→政策係主因' if drop3b > 0.2 else '輕微下降→政策非主因'})")

    # 3c: 控制反壟斷後, 福德宮 vs 股價 (直接路徑)
    r_direct, p_direct = pearson_r(fude_arr, ret_arr)
    pr3c, pp3c = partial_corr(fude_arr, ret_arr, at_arr)
    print(f"\n  3c. 福德宮 vs 股價回報 (直接, 控制反壟斷後)")
    print(f"      原始 r = {r_direct:>+5.3f}, p = {p_direct:.4f}")
    print(f"      偏相關 r = {pr3c:>+5.3f}, p = {pp3c:.4f}")

    # 3d: 反壟斷 vs 各變量嘅相關性
    r_at_cons, _ = pearson_r(at_arr, cons_arr)
    r_at_inv, _ = pearson_r(at_arr, inv_arr)
    r_at_bb, _ = pearson_r(at_arr, bb_arr)
    r_at_ret, _ = pearson_r(at_arr, ret_arr)
    r_at_fude, _ = pearson_r(at_arr, fude_arr)
    print(f"\n  3d. 反壟斷虛擬變量 vs 各變量:")
    print(f"      反壟斷 vs 福德宮:  r = {r_at_fude:>+5.3f}")
    print(f"      反壟斷 vs 保守程度: r = {r_at_cons:>+5.3f}")
    print(f"      反壟斷 vs 投資數量: r = {r_at_inv:>+5.3f}")
    print(f"      反壟斷 vs 回購金額: r = {r_at_bb:>+5.3f}")
    print(f"      反壟斷 vs 股價回報: r = {r_at_ret:>+5.3f}")

    # ============================================================
    # 綜合結論
    # ============================================================
    print(f"\n{'='*110}")
    print(f"  ══ 綜合結論 ══")
    print(f"{'='*110}")

    # Chain 1 判定
    c1_pass = r1 > 0
    c1_note = f"r={r1:+.3f}, {'正相關✅' if c1_pass else '負相關❌'}"
    if p1 < 0.05:
        c1_note += " 顯著"
    else:
        c1_note += " 不顯著"

    # Chain 2 判定
    c2_pass = r2 < 0
    c2_note = f"r={r2:+.3f}, {'負相關✅' if c2_pass else '正相關❌'}"
    if p2 < 0.05:
        c2_note += " 顯著"
    else:
        c2_note += " 不顯著"

    # Chain 3 判定
    c3_pass = abs(pr3a) > 0.1 and abs(pr3b) > 0.1
    c3_note = f"偏相關: 福德↔保守 r={pr3a:+.3f}, 保守↔股價 r={pr3b:+.3f}"

    print(f"\n  Chain 1 (福德宮→保守程度): {c1_note}")
    print(f"  Chain 2 (保守程度→股價跌): {c2_note}")
    print(f"  Chain 3 (排除反壟斷):      {c3_note}")

    all_pass = c1_pass and c2_pass and c3_pass
    print(f"\n  {'✅ 三條鏈全部支持假說！理論初步成立。' if all_pass else '❌ 部分鏈條唔支持，理論需要修正。'}")

    # 關鍵發現
    print(f"\n  關鍵發現:")
    if r_at_cons > 0.3:
        print(f"    ⚠️ 反壟斷 vs 保守程度 r={r_at_cons:+.3f} — 反壟斷政策本身推高咗保守程度")
        print(f"       呢個意味住 2021-2023 嘅保守可能主要係政策迫使, 而唔係福德宮驅動")
    if r_at_fude < 0.1 and r_at_fude > -0.1:
        print(f"    ℹ️ 反壟斷 vs 福德宮 r={r_at_fude:+.3f} — 福德宮同政策週期無關 (好事, 證明獨立性)")
    if abs(pr3a) < abs(r1) - 0.15:
        print(f"    ⚠️ 控制反壟斷後 Chain1 相關大幅下降 ({r1:+.3f}→{pr3a:+.3f}), 政策可能係混淆變量")

    # 路徑分析摘要
    print(f"\n  路徑分析摘要 (Sobel 精神):")
    indirect = r1 * r2
    direct = r_direct
    print(f"    福德宮→保守→股價 (間接效應): r1×r2 = {r1:+.3f} × {r2:+.3f} = {indirect:+.3f}")
    print(f"    福德宮→股價 (直接效應):    r = {direct:+.3f}")
    if abs(indirect) > abs(direct):
        print(f"    間接效應 > 直接效應 → 保守程度作為中介變量有解釋力")
    else:
        print(f"    直接效應 > 間接效應 → 保守程度中介作用有限")

    print(f"{'='*110}\n")


if __name__ == '__main__':
    main()
