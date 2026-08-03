# -*- coding: utf-8 -*-
"""
騰訊控股 (0700.HK) 紫微斗數命盤 — 12宮詳細星曜顯示
IPO 日期: 2004-06-16 10:00  性別: 男

Usage:
  python -m examples.tencent_chart
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ziwei.calculator import build_chart
from ziwei.constants import BRANCHES, STEMS, JU_NAMES


def print_tencent_chart():
    chart = build_chart(2004, 6, 16, 10, '男')

    ystem = STEMS[chart['year_stem']]
    ybranch = BRANCHES[chart['year_branch']]

    print(f"{'='*70}")
    print(f"  騰訊控股 (0700.HK) 紫微斗數命盤")
    print(f"  IPO 日期: 2004-06-16 10:00 (巳時)")
    print(f"{'='*70}")
    print(f"  農曆: {chart['lunar_year']}年{chart['lunar_month']}月{chart['lunar_day']}日")
    print(f"  年干支: {ystem}{ybranch}  |  五行局: {JU_NAMES[chart['wuxing_ju']]} ({chart['wuxing_ju']}局)")
    print(f"  納音: {chart['nayin']}")
    direction = '順行' if chart['dajun_forward'] else '逆行'
    print(f"  性別: 男  |  大限: {direction}  |  {chart['dajun_start_age']}歲起運")
    print(f"  命宮: {chart['palaces'][0]['stem']}{chart['palaces'][0]['branch']}  |  身宮: {BRANCHES[chart['shen_gong']]}")

    # 四化
    sihua = chart['sihua']
    print(f"\n  【本命四化】")
    for label, star_name in sihua.items():
        pos = chart['main_stars_pos'].get(star_name)
        branch_name = BRANCHES[pos] if pos is not None else '?'
        print(f"    {star_name}{label} → 落 {branch_name}宮")

    print(f"\n  【紫微星位置】{BRANCHES[chart['ziwei_pos']]}宮")

    print(f"\n{'='*70}")
    print(f"  十二宮詳細星曜")
    print(f"{'='*70}")

    for i, palace in enumerate(chart['palaces']):
        shen_mark = ' ★身宮' if palace['has_shen'] else ''
        line = f"{palace['stem']}{palace['branch']}  {palace['name']}{shen_mark}"
        print(f"\n  ┌{'─'*66}┐")
        print(f"  │ {line:<66}│")
        print(f"  ├{'─'*66}┤")

        if palace['main_stars']:
            s = '  '.join(palace['main_stars'])
            print(f"  │ 甲級主星: {s:<56}│")
        else:
            print(f"  │ 甲級主星: (空宮)                                        │")

        if palace['b_grade']:
            s = '  '.join(palace['b_grade'])
            print(f"  │ 乙級星:   {s:<56}│")
        else:
            print(f"  │ 乙級星:   ─                                               │")

        if palace['auspicious']:
            s = '  '.join(palace['auspicious'])
            print(f"  │ 吉星:     {s:<56}│")
        else:
            print(f"  │ 吉星:     ─                                               │")

        if palace['malefic']:
            s = '  '.join(palace['malefic'])
            print(f"  │ 煞星:     {s:<56}│")
        else:
            print(f"  │ 煞星:     ─                                               │")

        if palace['sihua']:
            s = '  '.join(palace['sihua'])
            print(f"  │ 四化:     {s:<56}│")
        else:
            print(f"  │ 四化:     ─                                               │")

        print(f"  └{'─'*66}┘")

    # 統計
    total_main = sum(len(p['main_stars']) for p in chart['palaces'])
    total_ausp = sum(len(p['auspicious']) for p in chart['palaces'])
    total_mal = sum(len(p['malefic']) for p in chart['palaces'])
    total_bg = sum(len(p['b_grade']) for p in chart['palaces'])
    total_sihua = sum(len(p['sihua']) for p in chart['palaces'])
    empty = sum(1 for p in chart['palaces'] if not p['main_stars'])

    print(f"\n{'='*70}")
    print(f"  星曜統計")
    print(f"{'='*70}")
    print(f"  甲級主星: {total_main} 顆 (空宮: {empty}/12)")
    print(f"  吉星: {total_ausp} 顆  |  煞星: {total_mal} 顆")
    print(f"  乙級星: {total_bg} 顆  |  四化: {total_sihua} 個")
    print(f"  總計: {total_main + total_ausp + total_mal + total_bg + total_sihua} 顆星曜")


if __name__ == '__main__':
    print_tencent_chart()
