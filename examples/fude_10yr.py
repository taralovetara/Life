# -*- coding: utf-8 -*-
"""
騰訊福德宮 10 年流動影響分析
本命 9.7 分唔變，但流年四化每年疊加唔同

Usage:
  python -m examples.fude_10yr
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ziwei.calculator import build_chart
from ziwei.timeline import get_liunian_sihua
from ziwei.constants import BRANCHES, STEMS, SIHUA_WEIGHTS


def print_fude_10yr():
    chart = build_chart(2004, 6, 16, 10, '男')

    # 找福德宮嘅地支
    fude_branch = None
    for p in chart['palaces']:
        if p['name'] == '福德宮':
            fude_branch = p['branch_idx']
            break

    print(f"{'='*70}")
    print(f"  騰訊福德宮 ({BRANCHES[fude_branch]}宮) 本命基底: 9.7 分")
    print(f"  本命星曜: 廉貞+巨門, 祿存+天馬, 廉貞化祿")
    print(f"  以下展示 2024-2036 每年流年四化對福德宮嘅疊加影響")
    print(f"  流年四化邏輯: 該年天干嘅4粒化星，若本命位置恰好在福德宮就疊加")
    print(f"{'='*70}")

    print(f"\n  {'年份':>4s}  {'天干':>2s}  {'命中福德宮?':14s}  {'疊加項':22s}  {'疊加分':>6s}  {'有效分'}")
    print(f"  {'─'*68}")

    for year in range(2024, 2037):
        ln = get_liunian_sihua(year)
        year_stem = (year - 4) % 10
        stem_name = STEMS[year_stem]

        hit_details = []
        flow_score = 0

        for sihua_label, star_name in ln['sihua'].items():
            star_pos = chart['main_stars_pos'].get(star_name)
            if star_pos == fude_branch:
                weight = SIHUA_WEIGHTS.get(sihua_label, 0)
                flow_score += weight
                hit_details.append(f'{star_name}{sihua_label}({weight:+.1f})')

        effective = 9.7 + flow_score

        if hit_details:
            hits_str = ', '.join(hit_details)
            print(f"  {year:>4d}  {stem_name:>2s}  {'✅ 命中':>8s}      {hits_str:<22s}  {flow_score:>+6.1f}  {effective:>6.1f}")
        else:
            all_s = '  '.join([f'{v}{k}' for k, v in ln['sihua'].items()])
            print(f"  {year:>4d}  {stem_name:>2s}  {'─':>8s}      {all_s:<22s}  {flow_score:>+6.1f}  {effective:>6.1f}")

    print(f"\n{'='*70}")
    print(f"  結論: 本命 9.7 永遠唔變，但有效分數因流年四化而波動")
    print(f"  10 年後(2034 甲寅)福德宮有效分可能高達 12.7 或低至 5.7")
    print(f"  ⚠️ 目前只計流年四化，大限四化/流年命盤疊加尚未實現")
    print(f"{'='*70}")


if __name__ == '__main__':
    print_fude_10yr()
