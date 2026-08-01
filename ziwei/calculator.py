# -*- coding: utf-8 -*-
"""
紫微斗數計算引擎 — 星曜排列
================================
確定性算法：輸入出生資料 → 輸出 12 宮星曜分佈
"""
from datetime import datetime
from zhdate import ZhDate
from .constants import (
    BRANCHES, STEMS, BRANCH_IDX, STEM_IDX, PALACE_NAMES,
    NAYIN_TABLE, ELEMENT_TO_JU, WUHU_DUN, SIHUA_TABLE, SIHUA_LABELS,
    ZIWEI_TABLE, ZIWEI_SYSTEM_OFFSETS, TIANFU_SYSTEM_OFFSETS,
    MAIN_STARS, TIANKUI_POS, TIANYUE_POS, HOUR_TO_SHICHEN,
    JU_NAMES, JU_START_AGES,
    LUCUN_POS, TIANMA_POS, HONGLUAN_POS, TIANYI_POS,
    TIANYAO_POS, GUCHEN_POS, GUASU_POS, HUAGAI_POS, XIANCHI_POS,
)


def hour_to_shichen(hour: float) -> int:
    """小時 → 時辰索引 (1-12)"""
    for start, end, idx in HOUR_TO_SHICHEN:
        if start <= hour < end:
            return idx
    return 1  # default 子時


def solar_to_lunar(year: int, month: int, day: int):
    """公曆 → 農曆"""
    dt = datetime(year, month, day)
    ld = ZhDate.from_datetime(dt)
    return ld.lunar_year, ld.lunar_month, ld.lunar_day, ld.leap_month


def get_year_stem_branch(lunar_year: int):
    """年干支索引"""
    return (lunar_year - 4) % 10, (lunar_year - 4) % 12


def get_ming_gong(lunar_month: int, hour_idx: int) -> int:
    """命宮地支索引"""
    return (2 + lunar_month - hour_idx) % 12


def get_shen_gong(lunar_month: int, hour_idx: int) -> int:
    """身宮地支索引"""
    return (lunar_month + hour_idx) % 12


def get_palace_stem(palace_branch: int, year_stem: int) -> int:
    """宮位天干索引 (五虎遁)"""
    yin_stem = WUHU_DUN[year_stem]
    return (yin_stem + (palace_branch - 2) % 12) % 10


def get_wuxing_ju(ming_stem: int, ming_branch: int):
    """命宮干支 → 五行局"""
    idx60 = (ming_stem * 6 + ming_branch * 5) % 60
    row, col = idx60 // 10, idx60 % 10
    nayin = NAYIN_TABLE[row][col]
    for elem, ju in ELEMENT_TO_JU.items():
        if elem in nayin:
            return ju, nayin
    return 5, nayin


def get_ziwei_pos(wuxing_ju: int, lunar_day: int) -> int:
    """紫微星位置"""
    ranges = ZIWEI_TABLE[wuxing_ju]
    for i in range(len(ranges) - 1, -1, -1):
        start_day, start_palace = ranges[i]
        if lunar_day >= start_day:
            return (start_palace + (lunar_day - start_day)) % 12
    return ranges[0][1]


def place_main_stars(ziwei_pos: int) -> dict:
    """安十四主星"""
    stars = {'紫微': ziwei_pos}
    for name, offset in ZIWEI_SYSTEM_OFFSETS:
        stars[name] = (ziwei_pos + offset) % 12
    tianfu_pos = (ziwei_pos + 6) % 12
    stars['天府'] = tianfu_pos
    for name, offset in TIANFU_SYSTEM_OFFSETS:
        stars[name] = (tianfu_pos + offset) % 12
    return stars


def place_auspicious(lunar_month: int, hour_idx: int, year_stem: int) -> dict:
    """安六吉星"""
    return {
        '文昌': (10 - (hour_idx - 1)) % 12,
        '文曲': (4 - (hour_idx - 1)) % 12,
        '左輔': (4 + (lunar_month - 1)) % 12,
        '右弼': (10 + (lunar_month - 1)) % 12,
        '天魁': TIANKUI_POS[year_stem],
        '天鉞': TIANYUE_POS[year_stem],
    }


def place_malefic(year_branch: int, hour_idx: int) -> dict:
    """安六煞星"""
    return {
        '擎羊': (2 + year_branch) % 12,
        '陀羅': (1 + year_branch) % 12,
        '火星': (2 + year_branch + (hour_idx - 1)) % 12,
        '鈴星': (8 + year_branch + (hour_idx - 1)) % 12,
        '地空': (11 - (hour_idx - 1)) % 12,
        '地劫': (5 - (hour_idx - 1)) % 12,
    }


def get_sihua(year_stem: int) -> dict:
    """年干四化"""
    stars = SIHUA_TABLE[year_stem]
    return dict(zip(SIHUA_LABELS, stars))


def place_b_grade(year_stem: int, year_branch: int) -> dict:
    """安乙級星（9粒）"""
    return {
        '祿存': LUCUN_POS[year_stem],
        '天馬': TIANMA_POS[year_branch],
        '紅鸞': HONGLUAN_POS[year_branch],
        '天喜': TIANYI_POS[year_branch],
        '天姚': TIANYAO_POS[year_branch],
        '孤辰': GUCHEN_POS[year_branch],
        '寡宿': GUASU_POS[year_branch],
        '華蓋': HUAGAI_POS[year_branch],
        '咸池': XIANCHI_POS[year_branch],
    }


def build_chart(solar_year, solar_month, solar_day, hour, gender='男'):
    """
    建構完整命盤
    
    Parameters
    ----------
    solar_year, solar_month, solar_day : int
    hour : float  (e.g. 8.5 for 8:30 AM)
    gender : str  ('男' or '女')
    
    Returns
    -------
    dict with keys: palaces, ming_gong, shen_gong, wuxing_ju, etc.
    """
    # 農曆轉換
    ly, lm, ld, leap = solar_to_lunar(solar_year, solar_month, solar_day)
    year_stem, year_branch = get_year_stem_branch(ly)
    hour_idx = hour_to_shichen(hour)
    
    # 命宮 / 身宮
    ming_gong = get_ming_gong(lm, hour_idx)
    shen_gong = get_shen_gong(lm, hour_idx)
    ming_stem = get_palace_stem(ming_gong, year_stem)
    
    # 五行局
    wuxing_ju, nayin = get_wuxing_ju(ming_stem, ming_gong)
    
    # 紫微 + 十四主星
    ziwei_pos = get_ziwei_pos(wuxing_ju, ld)
    main_stars = place_main_stars(ziwei_pos)
    
    # 吉星 / 煞星
    auspicious = place_auspicious(lm, hour_idx, year_stem)
    malefic = place_malefic(year_branch, hour_idx)
    
    # 乙級星
    b_grade = place_b_grade(year_stem, year_branch)
    
    # 四化
    sihua = get_sihua(year_stem)
    
    # 組裝 12 宮
    palaces = []
    for i in range(12):
        branch = (ming_gong - i) % 12
        stem = get_palace_stem(branch, year_stem)
        palaces.append({
            'name': PALACE_NAMES[i],
            'branch_idx': branch,
            'branch': BRANCHES[branch],
            'stem_idx': stem,
            'stem': STEMS[stem],
            'main_stars': [],
            'auspicious': [],
            'malefic': [],
            'b_grade': [],
            'sihua': [],
            'has_shen': (branch == shen_gong),
        })
    
    def place(star_name, branch_idx, category):
        for p in palaces:
            if p['branch_idx'] == branch_idx:
                p[category].append(star_name)
                break
    
    for sname, bidx in main_stars.items():
        place(sname, bidx, 'main_stars')
    for sname, bidx in auspicious.items():
        place(sname, bidx, 'auspicious')
    for sname, bidx in malefic.items():
        place(sname, bidx, 'malefic')
    for sname, bidx in b_grade.items():
        place(sname, bidx, 'b_grade')
    
    # 四化標記
    for label, star_name in sihua.items():
        if star_name in main_stars:
            bidx = main_stars[star_name]
            for p in palaces:
                if p['branch_idx'] == bidx:
                    p['sihua'].append(f'{star_name}{label}')
                    break
    
    # 大限方向
    yang = (year_stem % 2 == 0)
    dajun_forward = (yang and gender == '男') or (not yang and gender == '女')
    
    return {
        'palaces': palaces,
        'ming_gong': ming_gong,
        'shen_gong': shen_gong,
        'wuxing_ju': wuxing_ju,
        'nayin': nayin,
        'ziwei_pos': ziwei_pos,
        'lunar_year': ly,
        'lunar_month': lm,
        'lunar_day': ld,
        'leap_month': leap,
        'year_stem': year_stem,
        'year_branch': year_branch,
        'sihua': sihua,
        'gender': gender,
        'dajun_forward': dajun_forward,
        'dajun_start_age': JU_START_AGES[wuxing_ju],
        'dajun_span': wuxing_ju,
        'main_stars_pos': main_stars,
        'auspicious_pos': auspicious,
        'malefic_pos': malefic,
        'b_grade_pos': b_grade,
    }
