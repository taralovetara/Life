# -*- coding: utf-8 -*-
"""
紫微斗數時間軸 — 大限 / 流年分數追蹤
==========================================
"""
from .constants import (
    BRANCHES, STEMS, BRANCH_IDX, STEM_IDX, PALACE_NAMES,
    WUHU_DUN, SIHUA_TABLE, SIHUA_LABELS,
    STAR_BRIGHTNESS, MAIN_STAR_WEIGHTS,
    AUSPICIOUS_WEIGHTS, MALEFIC_WEIGHTS, SIHUA_WEIGHTS,
    BRIGHTNESS_LABELS, JU_NAMES,
)
from .scorer import score_palace, normalize_score


def get_dajun_sequence(chart: dict, count: int = 10) -> list:
    """
    計算大限序列
    
    Returns
    -------
    list of dict: [{age_start, age_end, branch_idx, branch, palace_name, ...}]
    """
    ming = chart['ming_gong']
    forward = chart['dajun_forward']
    start_age = chart['dajun_start_age']
    span = chart['dajun_span']
    
    # 建立地支 → 宮位名稱映射
    branch_to_palace = {}
    for p in chart['palaces']:
        branch_to_palace[p['branch_idx']] = p['name']
    
    sequence = []
    current_branch = ming
    for i in range(count):
        if i == 0:
            branch = ming
        else:
            branch = (current_branch + (1 if forward else -1)) % 12
            current_branch = branch
        
        age_start = start_age + i * span
        age_end = age_start + span - 1
        
        sequence.append({
            'index': i,
            'age_start': age_start,
            'age_end': age_end,
            'branch_idx': branch,
            'branch': BRANCHES[branch],
            'palace_name': branch_to_palace.get(branch, '?'),
        })
    
    return sequence


def get_dajun_stars(chart: dict, dajun_branch: int) -> dict:
    """
    計算大限宮內嘅星曜 (本命星 + 大限四化)
    大限宮直接使用本命盤該宮位嘅星曜
    """
    for p in chart['palaces']:
        if p['branch_idx'] == dajun_branch:
            return p
    return None


def get_liunian_sihua(year: int) -> dict:
    """流年四化"""
    year_stem = (year - 4) % 10
    stars = SIHUA_TABLE[year_stem]
    return {
        'year_stem': year_stem,
        'stem': STEMS[year_stem],
        'sihua': dict(zip(SIHUA_LABELS, stars)),
    }


def score_dajun(chart: dict, dajun_branch: int) -> dict:
    """
    計算大限分數 (使用本命盤該宮位嘅星曜)
    """
    palace = get_dajun_stars(chart, dajun_branch)
    if palace is None:
        return {'total': 0, 'detail': 'empty'}
    
    base = score_palace(palace)
    
    # 大限宮名稱
    branch_to_palace = {}
    for p in chart['palaces']:
        branch_to_palace[p['branch_idx']] = p['name']
    
    return {
        'total': base['total'],
        'normalized': round(normalize_score(base['total']), 1),
        'palace_name': branch_to_palace.get(dajun_branch, '?'),
        'branch': BRANCHES[dajun_branch],
        'detail': base,
    }


def score_dajun_with_liunian(chart: dict, dajun_branch: int, year: int) -> dict:
    """
    計算大限 + 流年四化嘅綜合分數
    """
    base = score_dajun(chart, dajun_branch)
    ln = get_liunian_sihua(year)
    
    # 檢查流年四化有冇打中本命主星
    liunian_impact = 0.0
    liunian_detail = []
    for label, star_name in ln['sihua'].items():
        weight = SIHUA_WEIGHTS.get(label, 0)
        # 檢查呢粒星喺邊個宮
        star_branch = chart['main_stars_pos'].get(star_name)
        if star_branch is not None:
            if star_branch == dajun_branch:
                liunian_impact += weight
                liunian_detail.append({
                    'star': star_name,
                    'label': label,
                    'hits': '大限宮',
                    'impact': weight,
                })
    
    combined = base['total'] + liunian_impact
    return {
        'year': year,
        'dajun_score': base['total'],
        'dajun_normalized': base['normalized'],
        'liunian_sihua': ln['sihua'],
        'liunian_impact': liunian_impact,
        'liunian_detail': liunian_detail,
        'combined_score': round(combined, 2),
        'combined_normalized': round(normalize_score(combined), 1),
    }


def generate_timeline(chart: dict, start_age: int, end_age: int) -> list:
    """
    產生時間線分數序列
    
    Parameters
    ----------
    chart : dict
    start_age : int  (e.g. 40)
    end_age : int    (e.g. 60)
    
    Returns
    -------
    list of dict: 每年一筆
    """
    dajun_seq = get_dajun_sequence(chart, count=20)
    
    # 建立年齡 → 大限映射
    age_to_dajun = {}
    for dj in dajun_seq:
        for age in range(dj['age_start'], dj['age_end'] + 1):
            age_to_dajun[age] = dj
    
    birth_year = chart['lunar_year']
    timeline = []
    
    for age in range(start_age, end_age + 1):
        solar_year = birth_year + age
        dj = age_to_dajun.get(age)
        if dj is None:
            continue
        
        yearly = score_dajun_with_liunian(chart, dj['branch_idx'], solar_year)
        yearly['age'] = age
        yearly['solar_year'] = solar_year
        yearly['dajun_palace'] = dj['palace_name']
        yearly['dajun_branch'] = dj['branch']
        timeline.append(yearly)
    
    return timeline
