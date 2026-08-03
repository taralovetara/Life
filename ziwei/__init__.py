# -*- coding: utf-8 -*-
"""
紫微斗數量化系統 (Zi Wei Dou Shu Quantified)
=================================================

Usage:
  from ziwei import build_chart, score_all_palaces, score_life_aspects_normalized, generate_timeline

  chart = build_chart(1974, 8, 10, 8.5, '男')
  scores = score_all_palaces(chart)
  aspects = score_life_aspects_normalized(scores)
  timeline = generate_timeline(chart, 40, 60)
"""
from .calculator import build_chart
from .scorer import score_all_palaces, score_palace, score_life_aspects, score_life_aspects_normalized
from .timeline import get_dajun_sequence, generate_timeline, score_dajun, score_dajun_with_liunian, get_liunian_sihua
from .stock_screener import stock_score, batch_screen, print_report, print_ranking
from .stock_backtest import stock_backtest, print_backtest, plot_backtest

__version__ = '1.2.0'
__all__ = [
    'build_chart',
    'score_all_palaces', 'score_palace',
    'score_life_aspects', 'score_life_aspects_normalized',
    'get_dajun_sequence', 'generate_timeline',
    'score_dajun', 'score_dajun_with_liunian',
    'get_liunian_sihua',
    'stock_score', 'batch_screen', 'print_report', 'print_ranking',
    'stock_backtest', 'print_backtest', 'plot_backtest',
]
