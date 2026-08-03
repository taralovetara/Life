# -*- coding: utf-8 -*-
"""
紫微斗數 x 股票回測引擎
========================
用公司命盤嘅流年分數預測每年股價走勢，
對比實際股價回報做回測。

邏輯:
  1. 公司 IPO 日期 → 排盤
  2. 每年流年四化影響事業宮/財帛宮嘅分數
  3. 綜合分數 > 上年平均 → 預期升（LONG）
  4. 綜合分數 < 上年平均 → 預期跌（SHORT）
  5. 對比實際年回報
"""

import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
from datetime import date

from .calculator import build_chart
from .scorer import score_all_palaces, score_palace
from .timeline import get_dajun_sequence, get_liunian_sihua, score_dajun
from .constants import (
    BRANCHES, STEMS, SIHUA_WEIGHTS, SIHUA_LABELS,
    MAIN_STAR_WEIGHTS, STAR_BRIGHTNESS,
    AUSPICIOUS_WEIGHTS, MALEFIC_WEIGHTS, B_GRADE_WEIGHTS,
)


def stock_backtest(name: str, ticker: str,
                   ipo_year: int, ipo_month: int, ipo_day: int,
                   ipo_hour: float = 10.0,
                   start_year: int = None, end_year: int = None) -> dict:
    """對單一股票做紫微斗數回測

    Parameters
    ----------
    name : str  公司名稱
    ticker : str  yfinance ticker (e.g. '0700.HK')
    ipo_year, ipo_month, ipo_day : int  IPO 日期
    ipo_hour : float  IPO 時間
    start_year, end_year : int  回測年份範圍
    """
    if end_year is None:
        end_year = date.today().year
    if start_year is None:
        start_year = ipo_year + 1

    # 1. 排盤
    print(f'排盤: {name} IPO {ipo_year}-{ipo_month:02d}-{ipo_day:02d}')
    chart = build_chart(ipo_year, ipo_month, ipo_day, ipo_hour, 'M')
    palace_scores = score_all_palaces(chart)
    palace_map = {ps['palace_name']: ps['total'] for ps in palace_scores}

    # 建立宮位索引
    branch_to_palace = {}
    branch_to_palace_obj = {}
    for p in chart['palaces']:
        branch_to_palace[p['branch_idx']] = p['name']
        branch_to_palace_obj[p['name']] = p

    # 2. 找出事業宮同財帛宮嘅地支索引
    career_branch = None
    wealth_branch = None
    for p in chart['palaces']:
        if p['name'] == '事業宮':
            career_branch = p['branch_idx']
        if p['name'] == '財帛宮':
            wealth_branch = p['branch_idx']

    print(f'  事業宮: {BRANCHES[career_branch]} (本命分 {palace_map["事業宮"]:+.1f})')
    print(f'  財帛宮: {BRANCHES[wealth_branch]} (本命分 {palace_map["財帛宮"]:+.1f})')

    # 3. 拉取股價
    print(f'拉取 {ticker} 股價...')
    try:
        import yfinance as yf
        raw = yf.download(ticker, start=f'{start_year}-01-01', end=f'{end_year+1}-01-01', progress=False)
        if isinstance(raw.columns, pd.MultiIndex):
            raw.columns = raw.columns.get_level_values(0)
        yearly_price = raw['Close'].resample('YE').last()
        yearly_return = yearly_price.pct_change() * 100
        yearly_return = yearly_return.dropna()
        print(f'  拉取到 {len(raw)} 個交易日')
    except Exception as e:
        print(f'  拉取失敗: {e}')
        return {'error': str(e)}

    # 4. 大限序列
    dajun_seq = get_dajun_sequence(chart, count=20)
    birth_year = chart['lunar_year']

    # 建立年份 → 大限映射
    year_to_dajun = {}
    for dj in dajun_seq:
        for age in range(dj['age_start'], dj['age_end'] + 1):
            solar_year = birth_year + age
            year_to_dajun[solar_year] = dj

    # 5. 逐年計算紫微分數
    print(f'\n計算流年分數...')
    rows = []
    prev_career_score = None
    prev_wealth_score = None

    for year in range(start_year, end_year + 1):
        # 該年嘅股價回報
        if year not in yearly_return.index.year:
            continue
        actual_ret = yearly_return[yearly_return.index.year == year].values
        if len(actual_ret) == 0:
            continue
        actual_ret = actual_ret[0]

        # 流年四化
        ln = get_liunian_sihua(year)

        # 事業宮分數（本命 + 流年四化影響）
        career_dj = year_to_dajun.get(year)
        career_base = palace_map.get('事業宮', 0)

        # 流年四化對事業宮嘅影響
        career_ln_impact = 0.0
        career_ln_detail = []
        for label, star_name in ln['sihua'].items():
            weight = SIHUA_WEIGHTS.get(label, 0)
            star_branch = chart['main_stars_pos'].get(star_name)
            if star_branch is not None and star_branch == career_branch:
                career_ln_impact += weight
                career_ln_detail.append(f'{star_name}{label}')

        # 流年四化對財帛宮嘅影響
        wealth_base = palace_map.get('財帛宮', 0)
        wealth_ln_impact = 0.0
        wealth_ln_detail = []
        for label, star_name in ln['sihua'].items():
            weight = SIHUA_WEIGHTS.get(label, 0)
            star_branch = chart['main_stars_pos'].get(star_name)
            if star_branch is not None and star_branch == wealth_branch:
                wealth_ln_impact += weight
                wealth_ln_detail.append(f'{star_name}{label}')

        # 大限影響（大限宮同事業/財帛宮嘅關係）
        dajun_impact = 0.0
        if career_dj:
            dj_palace_name = career_dj['palace_name']
            dj_score = palace_map.get(dj_palace_name, 0)
            # 如果大限宮係事業宮或財帛宮，影響加倍
            if dj_palace_name == '事業宮':
                dajun_impact = dj_score * 0.5
            elif dj_palace_name == '財帛宮':
                dajun_impact = dj_score * 0.4
            elif dj_palace_name == '命宮':
                dajun_impact = dj_score * 0.3

        # 綜合分數 = 事業宮本命 + 流年四化影響 + 財帛宮本命 + 流年四化影響 + 大限影響
        career_total = career_base + career_ln_impact
        wealth_total = wealth_base + wealth_ln_impact
        combined = career_total * 0.5 + wealth_total * 0.3 + dajun_impact * 0.2

        # 信號: 與上一年比較
        if prev_career_score is not None:
            score_change = combined - (prev_career_score * 0.5 + prev_wealth_score * 0.3)
            signal = 'LONG' if score_change > 0 else 'SHORT'
        else:
            signal = 'LONG' if combined > 0 else 'SHORT'
            score_change = 0

        # 策略回報
        if signal == 'LONG':
            strat_ret = actual_ret
        else:
            strat_ret = -actual_ret

        correct = 1 if (signal == 'LONG' and actual_ret > 0) or (signal == 'SHORT' and actual_ret < 0) else 0

        rows.append({
            'year': year,
            'career_base': round(career_base, 2),
            'career_ln': round(career_ln_impact, 2),
            'career_total': round(career_total, 2),
            'career_ln_detail': ','.join(career_ln_detail) if career_ln_detail else '-',
            'wealth_base': round(wealth_base, 2),
            'wealth_ln': round(wealth_ln_impact, 2),
            'wealth_total': round(wealth_total, 2),
            'wealth_ln_detail': ','.join(wealth_ln_detail) if wealth_ln_detail else '-',
            'dajun_impact': round(dajun_impact, 2),
            'dajun_palace': career_dj['palace_name'] if career_dj else '?',
            'combined': round(combined, 2),
            'score_change': round(score_change, 2),
            'signal': signal,
            'actual_return': round(actual_ret, 2),
            'strategy_return': round(strat_ret, 2),
            'correct': correct,
        })

        prev_career_score = career_total
        prev_wealth_score = wealth_total

    df = pd.DataFrame(rows)
    if df.empty:
        return {'error': '無回測數據'}

    # 6. 統計
    n = len(df)
    win_rate = df['correct'].mean() * 100
    cum_strat = df['strategy_return'].sum()
    cum_bh = df['actual_return'].sum()

    # 相關性
    from scipy import stats as sp_stats
    r, p = sp_stats.pearsonr(df['combined'], df['actual_return'])
    r_s, p_s = sp_stats.spearmanr(df['combined'], df['actual_return'])

    return {
        'name': name,
        'ticker': ticker,
        'n_years': n,
        'win_rate': round(win_rate, 1),
        'cumulative_strategy': round(cum_strat, 2),
        'cumulative_bh': round(cum_bh, 2),
        'excess_return': round(cum_strat - cum_bh, 2),
        'pearson_r': round(r, 4),
        'pearson_p': round(p, 4),
        'spearman_r': round(r_s, 4),
        'spearman_p': round(p_s, 4),
        'df': df,
    }


def print_backtest(result: dict):
    """印出回測結果"""
    if 'error' in result:
        print(f'錯誤: {result["error"]}')
        return

    r = result
    df = r['df']

    print(f'\n{"="*80}')
    print(f'  紫微斗數 x {r["name"]} ({r["ticker"]}) 回測結果')
    print(f'  回測期: {df["year"].min()}-{df["year"].max()} | {r["n_years"]} 年')
    print(f'{"="*80}')
    print(f'  方向勝率:        {r["win_rate"]:.1f}%')
    print(f'  策略累計回報:    {r["cumulative_strategy"]:+.2f}%')
    print(f'  Buy & Hold:      {r["cumulative_bh"]:+.2f}%')
    print(f'  超額回報:        {r["excess_return"]:+.2f}%')
    print(f'  Pearson 相關:    {r["pearson_r"]:+.4f} (p={r["pearson_p"]:.4f})')
    print(f'  Spearman 相關:   {r["spearman_r"]:+.4f} (p={r["spearman_p"]:.4f})')

    print(f'\n  {"年份":>4s} | {"事業宮":>6s} | {"流年影響":>8s} | {"財帛宮":>6s} | {"流年影響":>8s} | {"大限宮":>6s} | {"綜合分":>6s} | {"信號":>5s} | {"實際回報":>8s} | {"策略":>7s} | 結果')
    print(f'  {"─"*4} | {"─"*6} | {"─"*8} | {"─"*6} | {"─"*8} | {"─"*6} | {"─"*6} | {"─"*5} | {"─"*8} | {"─"*7} | {"─"*2}')

    for _, row in df.iterrows():
        mark = 'V' if row['correct'] else 'X'
        career_ln = row['career_ln_detail'] if row['career_ln_detail'] != '-' else ''
        wealth_ln = row['wealth_ln_detail'] if row['wealth_ln_detail'] != '-' else ''
        print(f'  {row["year"]:>4d} | {row["career_total"]:>+6.1f} | {career_ln:>8s} | {row["wealth_total"]:>+6.1f} | {wealth_ln:>8s} | {row["dajun_palace"]:>6s} | {row["combined"]:>+6.1f} | {row["signal"]:>5s} | {row["actual_return"]:>+7.2f}% | {row["strategy_return"]:>+6.2f}% | {mark}')

    print(f'{"="*80}')

    # 解讀
    print(f'\n  解讀:')
    if r['win_rate'] > 55:
        print(f'    勝率 {r["win_rate"]:.1f}% 高於隨機，紫微斗數對 {r["name"]} 可能有微弱預測力')
    elif r['win_rate'] > 45:
        print(f'    勝率 {r["win_rate"]:.1f}% 接近隨機，紫微斗數對 {r["name"]} 無明顯預測力')
    else:
        print(f'    勝率 {r["win_rate"]:.1f}% 低於隨機，紫微斗數對 {r["name"]} 無預測力')

    if r['pearson_p'] < 0.05:
        print(f'    Pearson 相關顯著 (p={r["pearson_p"]:.4f})，綜合分數同股價有統計關係')
    else:
        print(f'    Pearson 相關不顯著 (p={r["pearson_p"]:.4f})，綜合分數同股價無統計關係')


def plot_backtest(result: dict, save_path: str = None):
    """畫回測圖"""
    if 'error' in result or 'df' not in result:
        return

    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.font_manager as fm

    fm.fontManager.addfont('/usr/share/fonts/truetype/chinese/SarasaMonoSC-Regular.ttf')
    fm.fontManager.addfont('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
    plt.rcParams['font.sans-serif'] = ['Sarasa Mono SC', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False

    df = result['df']
    fig, axes = plt.subplots(3, 1, figsize=(14, 10), constrained_layout=True)

    # 圖1: 累計回報對比
    ax1 = axes[0]
    ax1.plot(df['year'], df['actual_return'].cumsum(), label='Buy & Hold', color='#FFD700', linewidth=2)
    ax1.plot(df['year'], df['strategy_return'].cumsum(), label='紫微斗數策略', color='#e74c3c', linewidth=2)
    ax1.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax1.set_title(f'{result["name"]} ({result["ticker"]}) 紫微斗數回測')
    ax1.set_ylabel('累計回報 (%)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 圖2: 綜合分數 vs 實際回報
    ax2 = axes[1]
    colors = ['#2ecc71' if r > 0 else '#e74c3c' for r in df['actual_return']]
    ax2.bar(df['year'] - 0.2, df['combined'], width=0.4, color='#3498db', alpha=0.7, label='紫微綜合分')
    ax2.bar(df['year'] + 0.2, df['actual_return'], width=0.4, color=colors, alpha=0.7, label='實際回報%')
    ax2.axhline(y=0, color='black', linewidth=0.5)
    ax2.set_title('紫微綜合分 vs 實際股價回報')
    ax2.set_ylabel('分數 / 回報%')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 圖3: 散點圖
    ax3 = axes[2]
    ax3.scatter(df['combined'], df['actual_return'], c=df['correct'], cmap='RdYlGn',
               edgecolors='gray', s=80, zorder=5)
    ax3.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax3.axvline(x=0, color='gray', linestyle='--', alpha=0.5)
    for _, row in df.iterrows():
        ax3.annotate(str(row['year']), (row['combined'], row['actual_return']), fontsize=8,
                    xytext=(5, 5), textcoords='offset points')
    ax3.set_xlabel('紫微綜合分')
    ax3.set_ylabel('實際回報 (%)')
    ax3.set_title(f'相關性: Pearson={result["pearson_r"]:+.3f}')
    ax3.grid(True, alpha=0.3)

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f'\n  圖表已儲存: {save_path}')
    else:
        plt.show()
    plt.close(fig)
