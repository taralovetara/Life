# -*- coding: utf-8 -*-
"""
騰訊福德宮有效分數 vs 「保守程度」指標對比
三個指標: 營收增長率, CAPEX/營收比, 對外投資宗數
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
from ziwei.constants import STEMS, SIHUA_WEIGHTS

# 騰訊歷年對外投資宗數 (來源: IT桔子/廣發證券/公開報導)
INVESTMENT_COUNTS = {
    2005: 3,   2006: 5,   2007: 8,   2008: 6,
    2009: 12,  2010: 15,  2011: 22,  2012: 18,
    2013: 28,  2014: 36,  2015: 55,  2016: 48,
    2017: 65,  2018: 72,  2019: 45,  2020: 38,
    2021: 30,  2022: 12,  2023: 10,  2024: 8,
}

# 騰訊歷年營收增長率% (來源: 年報)
REVENUE_GROWTH = {
    2005: 25, 2006: 96, 2007: 36, 2008: 87,
    2009: 73, 2010: 58, 2011: 45, 2012: 54,
    2013: 38, 2014: 31, 2015: 30, 2016: 48,
    2017: 56, 2018: 32, 2019: 21, 2020: 28,
    2021: 10, 2022: -1, 2023: 10, 2024: 9,
}

# CAPEX/營收比% (來源: 年報現金流量表)
CAPEX_RATIO = {
    2005: 8, 2006: 10, 2007: 12, 2008: 9,
    2009: 8, 2010: 10, 2011: 14, 2012: 13,
    2013: 11, 2014: 14, 2015: 18, 2016: 16,
    2017: 20, 2018: 22, 2019: 18, 2020: 16,
    2021: 15, 2022: 12, 2023: 10, 2024: 9,
}


def main():
    chart = build_chart(2004, 6, 16, 10, '男')

    fude_branch = fude_palace = None
    for p in chart['palaces']:
        if p['name'] == '福德宮':
            fude_branch = p['branch_idx']
            fude_palace = p
            break
    base_score = score_palace(fude_palace)['total']

    years = list(range(2005, 2025))

    # 福德宮有效分數
    fude_scores = {}
    for year in years:
        ln = get_liunian_sihua(year)
        flow = 0.0
        for sihua_label, star_name in ln['sihua'].items():
            if chart['main_stars_pos'].get(star_name) == fude_branch:
                flow += SIHUA_WEIGHTS.get(sihua_label, 0)
        fude_scores[year] = base_score + flow

    # === 顯示結果 ===
    print(f"\n{'='*100}")
    print(f"  騰訊福德宮有效分數 vs 保守程度指標")
    print(f"  假說: 福德宮高分 → 保守 → 營收增長低, CAPEX低, 投資少")
    print(f"{'='*100}")
    print(f"  {'年份':>4s}  {'天干':>2s}  {'福德分':>6s}  {'標記':>4s}  {'營收增長':>8s}  {'CAPEX%':>7s}  {'投資宗數':>8s}")
    print(f"  {'-'*60}")

    data = {'rev': [], 'capex': [], 'inv': []}

    for year in years:
        sc = fude_scores[year]
        mark = 'HIGH' if sc >= 11.7 else ('LOW ' if sc <= 5.7 else '    ')
        rg = REVENUE_GROWTH.get(year)
        cr = CAPEX_RATIO.get(year)
        iv = INVESTMENT_COUNTS.get(year)

        rg_s = f'{rg:>+7.1f}%' if rg is not None else '    N/A'
        cr_s = f'{cr:>6.1f}%' if cr is not None else '   N/A'
        iv_s = f'{iv:>6d}' if iv is not None else '  N/A'

        print(f"  {year:>4d}  {STEMS[(year-4)%10]:>2s}  {sc:>6.1f}  {mark}  {rg_s}  {cr_s}  {iv_s}")

        if rg is not None:
            data['rev'].append((sc, rg, year))
        if cr is not None:
            data['capex'].append((sc, cr, year))
        if iv is not None:
            data['inv'].append((sc, iv, year))

    # 統計
    print(f"\n{'='*100}")
    print(f"  相關性分析 (福德宮有效分 vs 各指標)")
    print(f"{'='*100}")

    labels = {'rev': '營收增長率', 'capex': 'CAPEX/營收比', 'inv': '對外投資宗數'}

    for key, label in labels.items():
        pairs = data[key]
        if len(pairs) < 5:
            continue
        sc_arr = np.array([p[0] for p in pairs])
        val_arr = np.array([p[1] for p in pairs])
        r = np.corrcoef(sc_arr, val_arr)[0, 1]
        n = len(pairs)
        r2 = r**2
        t = r * np.sqrt((n-2)/(1-r2+1e-10)) if abs(r) < 1 else 0

        med = np.median(sc_arr)
        hi = val_arr[sc_arr >= med]
        lo = val_arr[sc_arr < med]

        sig = '*' if abs(t) > 2.093 else ''
        direction = '正相關' if r > 0 else '負相關'
        print(f"\n  {label}:")
        print(f"    Pearson r = {r:>+5.3f} ({direction}) {sig}")
        print(f"    R-squared = {r2:.1%}, t = {t:>+5.2f}, n = {n}")
        print(f"    HIGH福德宮年均: {np.mean(hi):>7.1f}  vs  LOW年均: {np.mean(lo):>7.1f}  差異: {np.mean(hi)-np.mean(lo):>+7.1f}")

    # HIGH vs LOW 分組對比
    print(f"\n{'='*100}")
    fude_high = [y for y in years if fude_scores[y] >= 11.7]
    fude_low = [y for y in years if fude_scores[y] <= 5.7]
    print(f"  分組對比: HIGH年份({', '.join(str(y) for y in fude_high)})")
    print(f"            LOW年份({', '.join(str(y) for y in fude_low)})")
    print(f"{'='*100}")
    print(f"  {'指標':>10s}  {'HIGH平均':>10s}  {'LOW平均':>10s}  {'差異':>10s}  {'支持假說?'}")
    print(f"  {'-'*55}")

    for key, label in labels.items():
        hi_vals = [data[key][i][1] for i in range(len(data[key])) if data[key][i][0] >= 11.7]
        lo_vals = [data[key][i][1] for i in range(len(data[key])) if data[key][i][0] <= 5.7]
        if hi_vals and lo_vals:
            hi_m, lo_m = np.mean(hi_vals), np.mean(lo_vals)
            diff = hi_m - lo_m
            support = '✅' if diff < 0 else '❌'
            print(f"  {label:>10s}  {hi_m:>10.1f}  {lo_m:>10.1f}  {diff:>+10.1f}  {support}")

    print(f"\n  假說: 福德宮HIGH → 保守 → 三個指標都應該LOW")
    print(f"  ✅ = 數據支持假說, ❌ = 數據反駁假說")
    print(f"{'='*100}")


if __name__ == '__main__':
    main()
