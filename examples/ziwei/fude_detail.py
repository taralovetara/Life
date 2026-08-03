# -*- coding: utf-8 -*-
"""
騰訊福德宮詳細計分拆解

Usage:
  python -m examples.fude_detail
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ziwei.calculator import build_chart
from ziwei.scorer import score_all_palaces
from ziwei.constants import (
    BRANCHES, STEMS, STAR_BRIGHTNESS, MAIN_STAR_WEIGHTS,
    AUSPICIOUS_WEIGHTS, MALEFIC_WEIGHTS, SIHUA_WEIGHTS,
    B_GRADE_WEIGHTS, BRIGHTNESS_LABELS,
)


def print_fude_detail():
    chart = build_chart(2004, 6, 16, 10, '男')

    # 找福德宮
    fude = None
    for p in chart['palaces']:
        if p['name'] == '福德宮':
            fude = p
            break

    branch_idx = fude['branch_idx']
    branch = fude['branch']
    stem = fude['stem']

    print(f"{'='*60}")
    print(f"  騰訊 福德宮 ({stem}{branch}) 詳細計分拆解")
    print(f"{'='*60}")

    # 1. 主星分數
    print(f"\n【一、甲級主星】")
    print(f"  公式: Σ(亮度 × 權重)")
    print(f"  {'─'*52}")

    main_total = 0
    for star_name in fude['main_stars']:
        brightness = STAR_BRIGHTNESS[star_name][branch_idx]
        b_label = BRIGHTNESS_LABELS[brightness]
        weight = MAIN_STAR_WEIGHTS[star_name]
        score = brightness * weight
        main_total += score
        print(f"  {star_name}: 亮度={brightness}({b_label}) × 權重={weight:.1f} = {score:.1f}")

    print(f"  {'─'*52}")
    print(f"  主星小計: {main_total:.1f}")

    # 2. 吉星分數
    print(f"\n【二、吉星（六吉星）】")
    print(f"  公式: Σ(吉星權重)")
    print(f"  {'─'*52}")

    ausp_total = 0
    if fude['auspicious']:
        for star_name in fude['auspicious']:
            w = AUSPICIOUS_WEIGHTS[star_name]
            ausp_total += w
            print(f"  {star_name}: +{w:.1f}")
    else:
        print(f"  (無吉星)")

    print(f"  {'─'*52}")
    print(f"  吉星小計: +{ausp_total:.1f}")

    # 3. 煞星分數
    print(f"\n【三、煞星（六煞星）】")
    print(f"  公式: -Σ(煞星權重)")
    print(f"  {'─'*52}")

    mal_total = 0
    if fude['malefic']:
        for star_name in fude['malefic']:
            w = MALEFIC_WEIGHTS[star_name]
            mal_total += w
            print(f"  {star_name}: -{w:.1f}")
    else:
        print(f"  (無煞星)")

    print(f"  {'─'*52}")
    print(f"  煞星小計: -{mal_total:.1f}")

    # 4. 乙級星分數
    print(f"\n【四、乙級星】")
    print(f"  公式: Σ(乙級星權重，正負皆有)")
    print(f"  {'─'*52}")

    bg_total = 0
    if fude['b_grade']:
        for star_name in fude['b_grade']:
            w = B_GRADE_WEIGHTS[star_name]
            bg_total += w
            sign = '+' if w > 0 else ''
            print(f"  {star_name}: {sign}{w:.1f}")
    else:
        print(f"  (無乙級星)")

    print(f"  {'─'*52}")
    print(f"  乙級星小計: {bg_total:+.1f}")

    # 5. 四化分數
    print(f"\n【五、四化】")
    print(f"  公式: Σ(四化權重)")
    print(f"  {'─'*52}")

    sihua_total = 0
    if fude['sihua']:
        for label in fude['sihua']:
            for sihua_label, weight in SIHUA_WEIGHTS.items():
                if sihua_label in label:
                    sihua_total += weight
                    sign = '+' if weight > 0 else ''
                    print(f"  {label}: {sign}{weight:.1f}")
                    break
    else:
        print(f"  (無四化)")

    print(f"  {'─'*52}")
    print(f"  四化小計: {sihua_total:+.1f}")

    # 總計
    grand_total = main_total + ausp_total - mal_total + bg_total + sihua_total

    print(f"\n{'='*60}")
    print(f"  【總分計算】")
    print(f"{'='*60}")
    print(f"  主星分數:      {main_total:>8.1f}")
    print(f"  + 吉星分數:     {ausp_total:>8.1f}")
    print(f"  - 煞星分數:     {mal_total:>8.1f}")
    print(f"  + 乙級星分數:   {bg_total:>+8.1f}")
    print(f"  + 四化分數:     {sihua_total:>+8.1f}")
    print(f"  {'─'*40}")
    print(f"  福德宮總分:     {grand_total:>8.1f}")
    print(f"{'='*60}")

    # 全部 12 宮排名
    print(f"\n【全部 12 宮分數排名】")
    palace_scores = score_all_palaces(chart)
    ranked = sorted(palace_scores, key=lambda x: x['total'], reverse=True)
    for i, ps in enumerate(ranked):
        bar = '█' * max(0, int(ps['total'] / 1.5)) if ps['total'] > 0 else ''
        marker = ' ◀ 最高' if ps['palace_name'] == '福德宮' else ''
        print(f"  {i+1:>2}. {ps['palace_name']:4s} ({ps['stem']}{ps['branch']}) {ps['total']:>6.1f}  {bar}{marker}")


if __name__ == '__main__':
    print_fude_detail()
