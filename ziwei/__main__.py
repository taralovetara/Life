# -*- coding: utf-8 -*-
"""
紫微斗數量化系統 — CLI 入口
==================================

Usage:
  python -m ziwei 1974 8 10 8.5 男                    # 個人命盤
  python -m ziwei 1974 8 10 8.5 男 --timeline 40 60    # 含時間線
  python -m ziwei --stock 腾讯                        # 單一股票分析
  python -m ziwei --stock-all                          # 全部股票排行榜
"""
import argparse
import sys

from .cli import main as cli_main


def main():
    parser = argparse.ArgumentParser(description='紫微斗數量化系統')
    parser.add_argument('year', type=int, nargs='?', default=None, help='出生年/IPO年 (公曆)')
    parser.add_argument('month', type=int, nargs='?', default=None, help='出生月/IPO月')
    parser.add_argument('day', type=int, nargs='?', default=None, help='出生日/IPO日')
    parser.add_argument('hour', type=float, nargs='?', default=None, help='出生時間')
    parser.add_argument('gender', nargs='?', default=None, choices=['男', '女'], help='性別')
    parser.add_argument('--timeline', nargs=2, type=int, metavar=('START_AGE', 'END_AGE'))
    parser.add_argument('--dajun', action='store_true')
    parser.add_argument('--scores-only', action='store_true')
    parser.add_argument('--stock', type=str, metavar='NAME', help='股票分析 (用預設IPO日期)')
    parser.add_argument('--stock-all', action='store_true', help='全部股票排行榜')
    args = parser.parse_args()

    # 股票模式
    if args.stock or args.stock_all:
        from .stock_screener import stock_score, batch_screen, print_report, print_ranking, DEFAULT_STOCKS

        if args.stock:
            # 搵匹配嘅股票
            name = args.stock
            matched = [s for s in DEFAULT_STOCKS if name in s[0]]
            if not matched:
                print(f'搵唔到包含 "{name}" 嘅股票')
                print(f'可用: {", ".join(s[0] for s in DEFAULT_STOCKS)}')
                return
            for s_name, y, m, d, h, _ in matched:
                report = stock_score(s_name, y, m, d, h)
                print_report(report)
        else:
            results = batch_screen()
            print_ranking(results)
        return

    # 個人命盤模式 (原有功能)
    if args.year is None:
        parser.print_help()
        return

    # 重建原始 CLI 參數
    sys.argv = ['ziwei', str(args.year), str(args.month), str(args.day), str(args.hour), args.gender]
    if args.timeline:
        sys.argv += ['--timeline'] + [str(x) for x in args.timeline]
    if args.dajun:
        sys.argv.append('--dajun')
    if args.scores_only:
        sys.argv.append('--scores-only')
    cli_main()


if __name__ == '__main__':
    main()
