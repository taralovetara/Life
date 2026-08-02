# -*- coding: utf-8 *-
"""
紫微斗數 x 股票篩選引擎
===========================
將公司 IPO 日期視為「出生時間」，
用紫微斗數排盤計分，輸出股票篩選報告。

宮位映射:
  事業宮 → 營收增長潛力
  財帛宮 → 盈利能力
  疾厄宮 → 風險（反向指標）
  福德宮 → 品牌價值/護城河
  遷移宮 → 國際化/海外業務
  命宮   → 核心競爭力

Usage:
  from ziwei.stock_screener import stock_score, batch_screen

  report = stock_score('騰訊', 2004, 6, 16, 10, 'M')
  results = batch_screen(stock_list)
"""
import warnings
warnings.filterwarnings('ignore')

from .calculator import build_chart
from .scorer import score_all_palaces, score_life_aspects_normalized


# 公司 IPO 日期資料庫
# 格式: (名稱, 年, 月, 日, 時, 性質)
# 時辰: M=早上(9-11), A=下午(13-15), X=未知用正午(12)
# 性質: 'M'=主要/核心, 'S'=子公司/衍生
DEFAULT_STOCKS = [
    # 科技
    ('騰訊控股', 2004, 6, 16, 10, 'M'),     # 0700.HK
    ('阿里巴巴', 2014, 9, 19, 9.5, 'M'),     # BABA / 9988.HK
    ('美團', 2018, 9, 20, 9.5, 'M'),         # 3690.HK
    ('京東', 2014, 5, 22, 9.5, 'M'),         # JD / 9618.HK
    ('百度', 2005, 8, 5, 9.5, 'M'),          # BIDU / 9888.HK
    ('網易', 2000, 6, 30, 9.5, 'M'),         # NTES / 9999.HK
    ('快手', 2021, 2, 5, 9.5, 'M'),          # 1024.HK
    ('比亞迪電子', 2007, 12, 20, 9.5, 'M'),  # 0285.HK
    ('中芯國際', 2004, 3, 18, 9.5, 'M'),     # 0981.HK

    # 金融
    ('工商銀行', 2006, 10, 27, 10, 'M'),     # 1398.HK
    ('建設銀行', 2005, 10, 27, 10, 'M'),     # 0939.HK
    ('中國平安', 2007, 3, 1, 10, 'M'),       # 2318.HK
    ('匯豐控股', 1992, 4, 2, 10, 'M'),       # 0005.HK (倫敦上市日)

    # 消費
    ('貴州茅臺', 2001, 8, 27, 10, 'M'),     # 600519.SH
    ('美的集團', 2013, 9, 18, 10, 'M'),      # 000333.SZ / 0300.HK
    ('海底撈', 2018, 9, 26, 10, 'M'),       # 6862.HK

    # 地產
    ('恒基地產', 1972, 11, 6, 10, 'M'),      # 0012.HK (上市日)
    ('新鴻基地產', 1972, 11, 10, 10, 'M'),   # 0016.HK

    # 醫藥
    ('藥明生物', 2017, 6, 13, 9.5, 'M'),     # 2269.HK
    ('百濟神州', 2016, 2, 4, 9.5, 'M'),      # 6160.HK / BGNE
]


# 篩選用嘅宮位權重 (針對股票分析優化)
STOCK_ASPECT_WEIGHTS = {
    '盈利能力': {
        '財帛宮': 0.40, '田宅宮': 0.20, '福德宮': 0.20, '命宮': 0.20,
    },
    '增長潛力': {
        '事業宮': 0.35, '遷移宮': 0.25, '命宮': 0.20, '子女宮': 0.20,
    },
    '風險指數': {
        '疾厄宮': 0.40, '命宮': 0.25, '交友宮': 0.20, '父母宮': 0.15,
    },
    '核心實力': {
        '命宮': 0.30, '事業宮': 0.25, '福德宮': 0.20, '財帛宮': 0.25,
    },
}


def stock_score(name: str, year: int, month: int, day: int,
                hour: float = 12.0, gender: str = 'M') -> dict:
    """計算單一股票嘅紫微斗數分析報告

    Parameters
    ----------
    name : str  公司名稱
    year, month, day : int  IPO 日期
    hour : float  IPO 時間（小時）
    gender : str  用 'M' 代表公司（陽性實體）

    Returns
    -------
    dict : 完整分析報告
    """
    chart = build_chart(year, month, day, hour, gender)
    palace_scores = score_all_palaces(chart)

    # 建立宮位名稱 → 分數映射
    palace_map = {ps['palace_name']: ps['total'] for ps in palace_scores}
    palace_map_raw = {ps['palace_name']: ps for ps in palace_scores}

    # 計算股票分析面向
    aspects = {}
    for aspect_name, weights in STOCK_ASPECT_WEIGHTS.items():
        score = 0.0
        breakdown = []
        for palace_name, w in weights.items():
            s = palace_map.get(palace_name, 0)
            score += s * w
            breakdown.append({
                'palace': palace_name,
                'weight': w,
                'raw_score': s,
                'contribution': round(s * w, 2),
            })
        aspects[aspect_name] = {
            'score_raw': round(score, 2),
            'score_normalized': _normalize(score),
            'breakdown': breakdown,
        }

    # 關鍵宮位詳情
    key_palaces = ['命宮', '事業宮', '財帛宮', '疾厄宮', '福德宮', '遷移宮']
    key_details = {}
    for pname in key_palaces:
        raw = palace_map_raw.get(pname, {})
        key_details[pname] = {
            'score': raw.get('total', 0),
            'main_stars': raw.get('main_breakdown', []),
            'b_grade': raw.get('b_grade_breakdown', []),
            'sihua': raw.get('sihua_breakdown', []),
        }

    # 綜合評分
    profit_score = aspects['盈利能力']['score_normalized']
    growth_score = aspects['增長潛力']['score_normalized']
    risk_score = aspects['風險指數']['score_normalized']
    core_score = aspects['核心實力']['score_normalized']

    # 綜合分 = 盈利30% + 增長30% + 風險反向20% + 核心20%
    composite = (profit_score * 0.30 + growth_score * 0.30
                 + (100 - risk_score) * 0.20 + core_score * 0.20)

    return {
        'name': name,
        'ipo_date': f'{year}-{month:02d}-{day:02d}',
        'aspects': aspects,
        'key_palaces': key_details,
        'composite_score': round(composite, 1),
        'ratings': _rating(composite),
    }


def batch_screen(stocks: list = None, sort_by: str = 'composite_score') -> list:
    """批量篩選股票

    Parameters
    ----------
    stocks : list of tuple  或 None 用預設清單
    sort_by : str  排序字段

    Returns
    -------
    list of dict  按綜合分數排序
    """
    if stocks is None:
        stocks = DEFAULT_STOCKS

    results = []
    for i, (name, y, m, d, h, _) in enumerate(stocks):
        try:
            report = stock_score(name, y, m, d, h)
            results.append(report)
            print(f'  [{i+1}/{len(stocks)}] {name:12s} 綜合={report["composite_score"]:5.1f}  '
                  f'盈利={report["aspects"]["盈利能力"]["score_normalized"]:5.1f}  '
                  f'增長={report["aspects"]["增長潛力"]["score_normalized"]:5.1f}  '
                  f'風險={report["aspects"]["風險指數"]["score_normalized"]:5.1f}')
        except Exception as e:
            print(f'  [{i+1}/{len(stocks)}] {name:12s} 錯誤: {e}')

    results.sort(key=lambda x: x.get(sort_by, 0), reverse=True)
    return results


def print_report(report: dict):
    """印出單一股票嘅完整報告"""
    r = report
    print(f'\n{"="*60}')
    print(f'  紫微斗數股票分析: {r["name"]}')
    print(f'  IPO 日期: {r["ipo_date"]}')
    print(f'  綜合評分: {r["composite_score"]}/100  {r["ratings"]}')
    print(f'{"="*60}')

    print(f'\n  四大面向:')
    for aname, adata in r['aspects'].items():
        print(f'    {aname:6s}: {adata["score_normalized"]:5.1f}/100  (原始分 {adata["score_raw"]:+.2f})')
        for b in adata['breakdown']:
            print(f'      └ {b["palace"]} x{b["weight"]:.2f} = {b["raw_score"]:+.2f} → {b["contribution"]:+.2f}')

    print(f'\n  關鍵宮位詳情:')
    for pname, pdetail in r['key_palaces'].items():
        stars_info = ', '.join(
            [f'{s["star"]}({s["brightness_label"]})' for s in pdetail['main_stars']]
        ) if pdetail['main_stars'] else '無主星'
        sihua_info = ', '.join([s['label'] for s in pdetail['sihua']]) if pdetail['sihua'] else ''
        b_info = ', '.join([f'{s["star"]}' for s in pdetail['b_grade']]) if pdetail['b_grade'] else ''
        extra = ''
        if sihua_info:
            extra += f' [{sihua_info}]'
        if b_info:
            extra += f' +{b_info}'
        print(f'    {pname}: {pdetail["score"]:+.2f}  {stars_info}{extra}')


def print_ranking(results: list):
    """印出排行榜"""
    print(f'\n{"="*70}')
    print(f'  紫微斗數股票篩選排行榜')
    print(f'{"="*70}')
    print(f'  {"排名":>4s} | {"股票":12s} | {"綜合":>6s} | {"盈利":>6s} | {"增長":>6s} | {"風險":>6s} | {"核心":>6s} | 評級')
    print(f'  {"-"*4} | {"-"*12} | {"-"*6} | {"-"*6} | {"-"*6} | {"-"*6} | {"-"*6} | {"-"*4}')
    for i, r in enumerate(results):
        print(f'  {i+1:4d} | {r["name"]:12s} | {r["composite_score"]:6.1f} | '
              f'{r["aspects"]["盈利能力"]["score_normalized"]:6.1f} | '
              f'{r["aspects"]["增長潛力"]["score_normalized"]:6.1f} | '
              f'{r["aspects"]["風險指數"]["score_normalized"]:6.1f} | '
              f'{r["aspects"]["核心實力"]["score_normalized"]:6.1f} | {r["ratings"]}')
    print(f'{"="*70}')


# --------------------------------------------------
# 內部函數
# --------------------------------------------------

def _normalize(score: float, min_val: float = -5, max_val: float = 25) -> float:
    """歸一化到 0-100"""
    return max(0, min(100, (score - min_val) / (max_val - min_val) * 100))


def _rating(score: float) -> str:
    """評級"""
    if score >= 70:
        return 'A'
    elif score >= 55:
        return 'B+'
    elif score >= 45:
        return 'B'
    elif score >= 35:
        return 'C+'
    elif score >= 25:
        return 'C'
    else:
        return 'D'
