# -*- coding: utf-8 -*-
"""
紫微斗數量化系統 — CLI 入口
==================================

Usage:
  python -m ziwei.cli 1974 8 10 8.5 男
  python -m ziwei.cli 1974 8 10 8.5 男 --timeline 40 60
"""
import sys
import argparse
from .calculator import build_chart, hour_to_shichen
from .scorer import score_all_palaces, score_life_aspects_normalized
from .timeline import get_dajun_sequence, generate_timeline
from .constants import (
    BRANCHES, STEMS, JU_NAMES, BRIGHTNESS_LABELS,
    SIHUA_LABELS, LIFE_ASPECT_WEIGHTS,
)


def print_chart(chart: dict):
    """印出命盤"""
    ystem = STEMS[chart['year_stem']]
    ybranch = BRANCHES[chart['year_branch']]
    gender = chart['gender']
    direction = '順行' if chart['dajun_forward'] else '逆行'
    
    print(f"\n{'='*60}")
    print(f"  紫微斗數量化命盤")
    print(f"{'='*60}")
    print(f"  農曆: {chart['lunar_year']}年{chart['lunar_month']}月{chart['lunar_day']}日")
    print(f"  年干支: {ystem}{ybranch}  |  五行局: {JU_NAMES[chart['wuxing_ju']]}")
    print(f"  性別: {gender}  |  大限: {direction}  |  {chart['dajun_start_age']}歲起運")
    print(f"  命宮: {chart['palaces'][0]['stem']}{chart['palaces'][0]['branch']}  |  身宮: {BRANCHES[chart['shen_gong']]}")
    
    sihua = chart['sihua']
    print(f"\n  四化: ", end='')
    parts = [f"{v}{k}" for k, v in sihua.items()]
    print('  '.join(parts))
    
    # 12 宮
    print(f"\n{'─'*60}")
    for palace in chart['palaces']:
        shen = ' 【身】' if palace['has_shen'] else ''
        stars = palace['main_stars'] + palace['auspicious'] + palace['b_grade'] + palace['malefic'] + palace['sihua']
        star_str = ', '.join(stars) if stars else '(空宮)'
        print(f"  {palace['stem']}{palace['branch']:2s} {palace['name']:4s}{shen} | {star_str}")


def print_scores(palace_scores: list, aspects: dict):
    """印出量化分數"""
    print(f"\n{'='*60}")
    print(f"  宮位分數 (原始分)  |  範圍約 -10 ~ +30")
    print(f"{'='*60}")
    print('  宮位    分數    主星分    吉星    乙級    煞星    四化')
    print('  ' + '─'*50)
    for ps in palace_scores:
        shen = ' *' if ps['has_shen'] else '  '
        print(f"  {ps['palace_name']:4s}{shen} {ps['total']:>6.1f}  {ps['main_score']:>8.1f}  {ps['auspicious_score']:>6.1f}  {ps['b_grade_score']:>+6.1f}  {ps['malefic_score']:>6.1f}  {ps['sihua_score']:>+7.1f}")
    
    print(f"\n{'='*60}")
    print(f"  人生面向分數 (歸一化 0-100)")
    print(f"{'='*60}")
    for name, data in aspects.items():
        bar_len = int(data['score_normalized'] / 5)
        bar = '█' * bar_len + '░' * (20 - bar_len)
        print(f"  {name:6s}  {data['score_normalized']:>5.1f}  {bar}")


def print_timeline(timeline: list):
    """印出時間線"""
    print(f"\n{'='*60}")
    print(f"  大限時間線 (年齡 / 年份 / 大限宮 / 分數)")
    print(f"{'='*60}")
    print(f"  {'年齡':>4s}  {'年份':>5s}  {'大限宮':6s}  {'大限分':>5s}  {'流年分':>5s}  {'綜合分':>5s}  {'趨勢'}")
    print(f"  {'─'*52}")
    
    prev = None
    for t in timeline:
        if prev is not None:
            diff = t['combined_normalized'] - prev
            if diff > 3:
                trend = '▲▲'
            elif diff > 1:
                trend = '▲'
            elif diff < -3:
                trend = '▼▼'
            elif diff < -1:
                trend = '▼'
            else:
                trend = '─'
        else:
            trend = '·'
        
        dj = t['dajun_palace'][:3] if t['dajun_palace'] else '??'
        print(f"  {t['age']:>4d}  {t['solar_year']:>5d}  {dj:6s}  {t['dajun_normalized']:>5.1f}  {t.get('liunian_impact', 0):>+5.1f}  {t['combined_normalized']:>5.1f}  {trend}")
        prev = t['combined_normalized']


def print_dajun_overview(chart: dict):
    """印出大限總覽"""
    seq = get_dajun_sequence(chart, count=10)
    print(f"\n{'='*60}")
    print(f"  大限總覽 ({JU_NAMES[chart['wuxing_ju']]}, {chart['dajun_start_age']}歲起運)")
    print(f"{'='*60}")
    for dj in seq:
        # 找該宮嘅主星
        stars = []
        for p in chart['palaces']:
            if p['branch_idx'] == dj['branch_idx']:
                stars = p['main_stars'] + p['sihua']
                break
        star_str = ', '.join(stars[:3]) if stars else '(空宮)'
        print(f"  {dj['index']+1:>2d}. {dj['age_start']:>2d}-{dj['age_end']:<2d}歲  {dj['branch']:2s}宮({dj['palace_name']:4s})  {star_str}")


def main():
    parser = argparse.ArgumentParser(description='紫微斗數量化系統')
    parser.add_argument('year', type=int, help='出生年 (公曆)')
    parser.add_argument('month', type=int, help='出生月 (公曆)')
    parser.add_argument('day', type=int, help='出生日 (公曆)')
    parser.add_argument('hour', type=float, help='出生時間 (24h, e.g. 8.5)')
    parser.add_argument('gender', choices=['男', '女'], help='性別')
    parser.add_argument('--timeline', nargs=2, type=int, metavar=('START_AGE', 'END_AGE'),
                        help='顯示時間線 (年齡範圍)')
    parser.add_argument('--dajun', action='store_true', help='顯示大限總覽')
    parser.add_argument('--scores-only', action='store_true', help='只顯示分數')
    args = parser.parse_args()
    
    # 排盤
    chart = build_chart(args.year, args.month, args.day, args.hour, args.gender)
    
    if not args.scores_only:
        print_chart(chart)
    
    # 計分
    palace_scores = score_all_palaces(chart)
    aspects = score_life_aspects_normalized(palace_scores)
    
    print_scores(palace_scores, aspects)
    
    if args.dajun:
        print_dajun_overview(chart)
    
    if args.timeline:
        start_age, end_age = args.timeline
        tl = generate_timeline(chart, start_age, end_age)
        print_timeline(tl)


if __name__ == '__main__':
    main()
