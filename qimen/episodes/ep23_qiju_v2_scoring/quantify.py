#!/usr/bin/env python3
"""
EP23 量化腳本：V2 增強評分系統 + 統一起局入口
===================================================================

本集新知識點：
1. palace_score_v2() 增強評分公式
2. qiju_v2() 統一起局入口
3. V2 決策閾值調整
4. detect_all_geju() 統一格局偵測
5. 多場景一鍵預測
"""
import sys
sys.path.insert(0, '../../')
from engine_v2 import (
    qiju_v2, print_chart_v2, decision_v2,
    palace_score_v2, detect_all_geju,
    SCENE_YONGSHEN, GONG_BAGUA, STAR_DOOR,
    JIUXING_SCORE, BAMEN_SCORE, BASHEN_SCORE,
    check_dedi, is_wang, check_liuyi_xingxing,
    check_menpo, check_tiangan_rumu, check_men_rumu,
    check_feigan, check_fugan,
)
from datetime import datetime

print('=' * 70)
print('EP23 量化驗證：V2 增強評分系統')
print('=' * 70)

# ============================================================
# Section 1: 評分公式組成驗證
# ============================================================
print('\n' + '=' * 70)
print('Section 1: V2 評分公式組成')
print('=' * 70)

print('\n  基礎分範圍:')
print(f'    九星: {min(JIUXING_SCORE.values()):+.1f} ~ {max(JIUXING_SCORE.values()):+.1f}')
print(f'    八門: {min(BAMEN_SCORE.values()):+.1f} ~ {max(BAMEN_SCORE.values()):+.1f}')
print(f'    八神: {min(BASHEN_SCORE.values()):+.1f} ~ {max(BASHEN_SCORE.values()):+.1f}')

print('\n  增強項目:')
items = [
    ('格局分(動態)', '所有吉凶格偵測總和', '不設限'),
    ('六儀擊刑', '6個固定組合', '-2.0'),
    ('門迫', '12+組', '-2.0'),
    ('天干入墓', '10干→4宮', '-2.5'),
    ('八門入墓', '8門→4宮', '-2.0'),
    ('得地', '門回本宮/宮生門', '+1.0'),
    ('長生旺', '用神處旺態', '+0.5'),
]
for name, desc, score in items:
    print(f'    {name}: {score} ({desc})')

# ============================================================
# Section 2: 決策閾值
# ============================================================
print('\n' + '=' * 70)
print('Section 2: V2 決策閾值')
print('=' * 70)

thresholds = [10, 7, 5, 3, 2, 1, 0, -1, -2, -3, -5, -7, -10]
print('\n  分數 → 決策:')
for s in thresholds:
    print(f'    {s:+5.1f} → {decision_v2(s)}')

# ============================================================
# Section 3: 場景用神配置表
# ============================================================
print('\n' + '=' * 70)
print('Section 3: 場景用神配置表 (11 場景)')
print('=' * 70)

for scene, cfg in SCENE_YONGSHEN.items():
    print(f'\n  {cfg["name"]}:')
    for ysh, meaning in cfg.get('yongshen', {}).items():
        print(f'    {ysh} = {meaning}')

# ============================================================
# Section 4: 實際起局對比 V1 vs V2 評分
# ============================================================
print('\n' + '=' * 70)
print('Section 4: 實際起局測試 (V2 增強評分)')
print('=' * 70)

test_time = datetime(2026, 8, 8, 9, 30)
r = qiju_v2(test_time)
print_chart_v2(r, 'EP23 V2 增強評分測試')

# 詳細顯示一個宮位嘅評分明細
best_p = max(r['scores'], key=r['scores'].get)
det = r['details'][best_p]
print(f'\n  最佳宮位 {GONG_BAGUA[best_p]}{best_p}宮 評分明細:')
print(f'    總分: {r["scores"][best_p]:+.1f}')
for k, v in det.items():
    if k not in ('gejus',) and v != 0:
        print(f'    {k}: {v}')
if det.get('gejus'):
    print(f'    格局:')
    for gtype, gname, gsc in det['gejus']:
        print(f'      [{gtype}] {gname}: {gsc:+.1f}')

# ============================================================
# Section 5: 多場景預測測試
# ============================================================
print('\n' + '=' * 70)
print('Section 5: 多場景一鍵預測')
print('=' * 70)

for scene in ['lawsuit_civil', 'health', 'exam']:
    r2 = qiju_v2(test_time, scene=scene)
    pred = r2.get('prediction', {})
    if pred:
        verdict = pred.get('verdict', pred.get('final_verdict', ''))
        print(f'\n  場景 {scene}: {verdict}')
        if 'steps' in pred:
            for step in pred['steps'][:3]:
                print(f'    Step {step.get("step","?")}: {step.get("detail", step.get("check", ""))}')

print('\n' + '=' * 70)
print('EP23 量化完成')
print('=' * 70)