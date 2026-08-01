# -*- coding: utf-8 -*-
"""
紫微斗數量化引擎 — 宮位計分系統
==================================
將傳統星曜組合轉化為數值分數。

計分公式:
  宮位分數 = Σ(主星亮度 × 主星權重)
             + Σ(吉星權重)
             - Σ(煞星權重)
             + Σ(四化權重)

分數範圍大約 -10 ~ +30，空宮約 0 分
"""
from .constants import (
    STAR_BRIGHTNESS, MAIN_STAR_WEIGHTS,
    AUSPICIOUS_WEIGHTS, MALEFIC_WEIGHTS, SIHUA_WEIGHTS,
    B_GRADE_WEIGHTS,
    LIFE_ASPECT_WEIGHTS, BRIGHTNESS_LABELS,
)


def score_palace(palace: dict) -> dict:
    """
    計算單一宮位分數

    Returns
    -------
    dict with: total, main_score, auspicious_score, malefic_score, sihua_score, breakdown
    """
    main_score = 0.0
    main_breakdown = []
    
    for star_name in palace['main_stars']:
        # 去除四化標記，取純星名
        pure_name = star_name
        for label in ['化祿', '化權', '化科', '化忌']:
            pure_name = pure_name.replace(label, '')
        
        brightness = STAR_BRIGHTNESS.get(pure_name, [3]*12)[palace['branch_idx']]
        weight = MAIN_STAR_WEIGHTS.get(pure_name, 1.0)
        contribution = brightness * weight
        main_score += contribution
        main_breakdown.append({
            'star': pure_name,
            'brightness': brightness,
            'brightness_label': BRIGHTNESS_LABELS.get(brightness, '?'),
            'weight': weight,
            'score': contribution,
        })
    
    # 吉星加分
    auspicious_score = 0.0
    for star_name in palace['auspicious']:
        auspicious_score += AUSPICIOUS_WEIGHTS.get(star_name, 0.8)
    
    # 煞星扣分
    malefic_score = 0.0
    for star_name in palace['malefic']:
        malefic_score += MALEFIC_WEIGHTS.get(star_name, 1.0)
    
    # 乙級星加減分 (權重有正有負)
    b_grade_score = 0.0
    b_grade_breakdown = []
    for star_name in palace['b_grade']:
        w = B_GRADE_WEIGHTS.get(star_name, 0)
        b_grade_score += w
        b_grade_breakdown.append({'star': star_name, 'weight': w, 'score': w})
    
    # 四化加減分
    sihua_score = 0.0
    sihua_breakdown = []
    for label in palace['sihua']:
        for sihua_label, weight in SIHUA_WEIGHTS.items():
            if sihua_label in label:
                sihua_score += weight
                sihua_breakdown.append({'label': label, 'score': weight})
                break
    
    total = main_score + auspicious_score - malefic_score + b_grade_score + sihua_score
    
    return {
        'total': round(total, 2),
        'main_score': round(main_score, 2),
        'auspicious_score': round(auspicious_score, 2),
        'malefic_score': round(malefic_score, 2),
        'b_grade_score': round(b_grade_score, 2),
        'sihua_score': round(sihua_score, 2),
        'main_breakdown': main_breakdown,
        'b_grade_breakdown': b_grade_breakdown,
        'sihua_breakdown': sihua_breakdown,
    }


def score_all_palaces(chart: dict) -> list:
    """計算全部 12 宮分數"""
    results = []
    for palace in chart['palaces']:
        s = score_palace(palace)
        results.append({
            'palace_name': palace['name'],
            'branch': palace['branch'],
            'stem': palace['stem'],
            'has_shen': palace['has_shen'],
            'b_grade_breakdown': s['b_grade_breakdown'],
            **s,
        })
    return results


def score_life_aspects(palace_scores: list) -> dict:
    """
    計算人生各面向分數
    
    Parameters
    ----------
    palace_scores : list of dict
        score_all_palaces() 的輸出
    
    Returns
    -------
    dict : {面向名稱: {score, breakdown}}
    """
    # 建立宮位名稱 → 分數的映射
    palace_map = {ps['palace_name']: ps['total'] for ps in palace_scores}
    
    aspects = {}
    for aspect_name, weights in LIFE_ASPECT_WEIGHTS.items():
        score = 0.0
        breakdown = []
        for palace_name, w in weights.items():
            s = palace_map.get(palace_name, 0)
            score += s * w
            breakdown.append({'palace': palace_name, 'weight': w, 'score': s, 'contribution': round(s * w, 2)})
        aspects[aspect_name] = {
            'score': round(score, 2),
            'breakdown': breakdown,
        }
    return aspects


def normalize_score(score: float, min_val: float = -5, max_val: float = 25) -> float:
    """將原始分數歸一化到 0-100"""
    return max(0, min(100, (score - min_val) / (max_val - min_val) * 100))


def score_life_aspects_normalized(palace_scores: list) -> dict:
    """計算人生各面向分數 (歸一化到 0-100)"""
    raw = score_life_aspects(palace_scores)
    result = {}
    for name, data in raw.items():
        result[name] = {
            'score_raw': data['score'],
            'score_normalized': round(normalize_score(data['score']), 1),
            'breakdown': data['breakdown'],
        }
    return result
