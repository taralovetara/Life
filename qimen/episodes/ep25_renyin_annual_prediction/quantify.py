#!/usr/bin/env python3
"""
EP25 量化腳本：壬寅年（2022）年度預測回測驗證
===================================================================

本集特點：年度預測應用篇，唔係方法論教學。
驗證方式：預測結論 vs 2022 年歷史事實 對照打分。

預測來源：天心堂坤正師傅 第二十五集（壬寅年預測）
驗證日期：2026-08-12（事後回測）
"""
import json
from datetime import datetime

print('=' * 70)
print('EP25 量化驗證：壬寅年（2022）年度預測回測')
print('=' * 70)

# ============================================================
# 預測 vs 歷史事實 對照表
# ============================================================
# 評分標準：
#   2.0 = 完全準確
#   1.0 = 基本正確（方向對但細節有偏差）
#   0.5 = 部分正確
#   0.0 = 不正確
#   -1.0 = 完全相反

predictions = [
    # === 疫情 ===
    {
        'id': 'P01',
        'category': '疫情',
        'prediction': '病毒繼續流行，新變種不斷出現，死亡人數繼續攀升',
        'timeline': '全年',
        'actual': 'Omicron 變種於 2022 年初全球大爆發，BA.1/BA.2/BA.5 接連出現；全球累計死亡持續上升',
        'score': 2.0,
        'notes': '完全準確。Omicron 多個亞型接連出現，殺傷力雖然相對 Delta 下降但感染人數龐大',
    },
    {
        'id': 'P02',
        'category': '疫情',
        'prediction': '病毒發展已進入最高峰，形勢兇猛但只係「最後的瘋狂」',
        'timeline': '全年',
        'actual': '2022 年確實係新冠最後一波全球大規模爆發，之後逐步轉為地方性流行',
        'score': 2.0,
        'notes': '完全準確。2022 年之後各國陸續取消防疫措施',
    },
    {
        'id': 'P03',
        'category': '疫情',
        'prediction': '六月份左右世界範圍內有一波相對較大的疫情',
        'timeline': '約6月',
        'actual': '2022 年 6 月 BA.4/BA.5 變種引發新一波全球疫情，多國確診數字回升',
        'score': 2.0,
        'notes': '時間點和事件完全吻合',
    },
    {
        'id': 'P04',
        'category': '疫情',
        'prediction': '疫苗效力越來越不明顯，三劑仍會感染',
        'timeline': '全年',
        'actual': 'Omicron 令疫苗防感染效力大幅下降，突破性感染普遍，三劑仍可感染',
        'score': 2.0,
        'notes': '完全準確。疫苗防重症仍有用但防感染效果確實大減',
    },
    {
        'id': 'P05',
        'category': '疫情',
        'prediction': '12 月左右新疫苗初步研發成功，更有效對付變種病毒',
        'timeline': '約12月',
        'actual': '2022 年 12 月，輝瑞/BioNTech 及 Moderna 均公佈針對 Omicron BA.4/BA.5 的新版疫苗數據並獲緊急授權',
        'score': 2.0,
        'notes': '時間點和內容完全吻合',
    },
    {
        'id': 'P06',
        'category': '疫情',
        'prediction': '新疫苗引發更多爭論爭議，甚至訴諸法律',
        'timeline': '12月後',
        'actual': '新版疫苗引發關於「是否應該更新疫苗」的爭論，各地對強制接種的法律訴訟持續',
        'score': 1.0,
        'notes': '方向正確，爭論確實存在，但「訴諸法律」的程度比預測的略低',
    },
    {
        'id': 'P07',
        'category': '疫情',
        'prediction': '大製藥商未能推出真正特效藥，無重大突破',
        'timeline': '全年',
        'actual': 'Paxlovid 雖獲廣泛使用但並非「特效藥」定義上的治癒藥物，全年無治療新冠的里程碑式突破',
        'score': 1.5,
        'notes': '基本正確。Paxlovid 存在但效果有限且有復陽問題',
    },
    # === 經濟 ===
    {
        'id': 'P08',
        'category': '經濟',
        'prediction': '環球經濟不好，恢復速度慢，困難重重',
        'timeline': '全年',
        'actual': '2022 年美國加息週期啟動，全球經濟放緩，俄烏戰爭引發能源危機',
        'score': 2.0,
        'notes': '完全準確。2022 年經濟確實困難重重',
    },
    {
        'id': 'P09',
        'category': '經濟',
        'prediction': '房地產/股市受壓制，有好的徵兆但無實質進展',
        'timeline': '全年',
        'actual': '2022 年美股大跌（標普跌約 19%），港股恆生指數跌約 15%，中國房地產持續暴雷',
        'score': 2.0,
        'notes': '完全準確。股市和房地產確實受壓',
    },
    {
        'id': 'P10',
        'category': '經濟',
        'prediction': '旅遊業繼續係重災區',
        'timeline': '全年',
        'actual': '2022 年上半年旅遊業仍因各國邊境限制而極度低迷，下半年才開始緩慢恢復',
        'score': 1.5,
        'notes': '基本正確。但下半年恢復速度比預測中嘅「重災區」略好',
    },
    {
        'id': 'P11',
        'category': '經濟',
        'prediction': '醫療/醫藥表現亮麗，吸金能力大',
        'timeline': '全年',
        'actual': '醫藥股 2022 年表現相對抗跌，疫苗和檢測相關企業營收大增',
        'score': 1.5,
        'notes': '方向正確，但醫藥股到後期隨疫情退潮而回落，全年並非一直「亮麗」',
    },
    {
        'id': 'P12',
        'category': '經濟',
        'prediction': '智慧科技/晶片/自動化/電子科技/新能源/貴金屬有不錯發展',
        'timeline': '全年',
        'actual': '2022 年新能源（電動車、太陽能）確實強勢；晶片因供應鏈問題先漲後跌；貴金屬（金）全年跌約 0.3% 基本持平',
        'score': 1.0,
        'notes': '部分正確。新能源準確，晶片波動大，貴金屬表現平平',
    },
    # === 香港 ===
    {
        'id': 'P13',
        'category': '香港',
        'prediction': '免檢疫通關確實會實現',
        'timeline': '全年',
        'actual': '香港到 2022 年底仍未能全面免檢疫通關（實際上到 2022 年 12 月才開始有限度通關）',
        'score': 0.5,
        'notes': '部分正確。年底有有限度通關，但全年大部分時間未能通關',
    },
    {
        'id': 'P14',
        'category': '香港',
        'prediction': '二月通關機會低，七月較有可能',
        'timeline': '2月/7月',
        'actual': '二月香港爆發第五波疫情，完全唔能通關；七月仍未能通關',
        'score': 0.5,
        'notes': '二月判斷正確；七月判斷偏差，實際通關延遲到年底',
    },
    {
        'id': 'P15',
        'category': '香港',
        'prediction': '特首選舉換屆，新人事新氣象，更多紀律部隊背景人士入班子',
        'timeline': '全年',
        'actual': '2022 年 5 月李家超當選並就任第六任特首，多名紀律部隊背景人士入局',
        'score': 2.0,
        'notes': '完全準確',
    },
    {
        'id': 'P16',
        'category': '香港',
        'prediction': '社會大體平靜，內部爭鬥內耗較少',
        'timeline': '全年',
        'actual': '2022 年香港社會確實較為平靜，無大型社會運動',
        'score': 2.0,
        'notes': '完全準確',
    },
    # === 人力市場 ===
    {
        'id': 'P17',
        'category': '人力市場',
        'prediction': '情況比較反覆，好勢頭無法持續，全年無大改善',
        'timeline': '全年',
        'actual': '2022 年香港失業率從年初 4.5% 降至年底 3.5% 左右，中間有反覆但趨勢向好',
        'score': 1.0,
        'notes': '「反覆」正確，但實際上年底有相當程度的改善，非「無大改善」',
    },
    {
        'id': 'P18',
        'category': '人力市場',
        'prediction': '根本解決需要全面通關，遊客恢復到疫情前水平',
        'timeline': '長期',
        'actual': '確實如此。香港人力市場最終隨通關恢復而改善',
        'score': 2.0,
        'notes': '完全準確',
    },
]

# ============================================================
# Section 1: 各領域預測準確度
# ============================================================
print('\n' + '=' * 70)
print('Section 1: 各預測項目驗證')
print('=' * 70)

categories = {}
for p in predictions:
    cat = p['category']
    if cat not in categories:
        categories[cat] = []
    categories[cat].append(p)

for cat, preds in categories.items():
    print(f'\n  【{cat}】')
    for p in preds:
        score_bar = '*' * int(abs(p['score']) * 10)
        print(f'    {p["id"]} [{p["score"]:+.1f}] {score_bar}')
        print(f'        預測: {p["prediction"]}')
        print(f'        事實: {p["actual"]}')
        print(f'        評語: {p["notes"]}')
        print()

# ============================================================
# Section 2: 分數統計
# ============================================================
print('\n' + '=' * 70)
print('Section 2: 分數統計')
print('=' * 70)

all_scores = [p['score'] for p in predictions]
total = len(predictions)
avg_score = sum(all_scores) / total if total > 0 else 0
perfect = sum(1 for s in all_scores if s >= 2.0)
good = sum(1 for s in all_scores if 1.0 <= s < 2.0)
partial = sum(1 for s in all_scores if 0.1 <= s < 1.0)
wrong = sum(1 for s in all_scores if s <= 0.0)

print(f'\n  總預測數: {total}')
print(f'  平均分:   {avg_score:.2f} / 2.0')
print(f'  完全準確 (>=2.0): {perfect} 個 ({perfect/total*100:.0f}%)')
print(f'  基本正確 (1.0-1.9): {good} 個 ({good/total*100:.0f}%)')
print(f'  部分正確 (0.1-0.9): {partial} 個 ({partial/total*100:.0f}%)')
print(f'  不正確 (<=0.0):    {wrong} 個 ({wrong/total*100:.0f}%)')

# 按類別統計
print(f'\n  按類別平均分:')
for cat, preds in categories.items():
    cat_avg = sum(p['score'] for p in preds) / len(preds)
    bar = '#' * int(cat_avg * 15)
    print(f'    {cat:6s}: {cat_avg:.2f} {bar}')

# ============================================================
# Section 3: 預測能力分析
# ============================================================
print('\n' + '=' * 70)
print('Section 3: 預測能力分析')
print('=' * 70)

# 區分「方法論型」vs「時間點型」預測
methodology_preds = [p for p in predictions if p['timeline'] in ('全年', '長期')]
timing_preds = [p for p in predictions if p['timeline'] not in ('全年', '長期')]

meth_avg = sum(p['score'] for p in methodology_preds) / len(methodology_preds) if methodology_preds else 0
time_avg = sum(p['score'] for p in timing_preds) / len(timing_preds) if timing_preds else 0

print(f'\n  趨勢/方向預測（全年/長期）: 平均 {meth_avg:.2f} ({len(methodology_preds)} 個)')
print(f'  具體時間點預測:            平均 {time_avg:.2f} ({len(timing_preds)} 個)')

if meth_avg > time_avg:
    print('\n  結論: 趨勢預測明顯優於時間點預測')
    print('  → 奇門遁甲擅長斷方向，斷時間需要更精細的方法')
else:
    print('\n  結論: 時間點預測不遜於趨勢預測')
    print('  → 時間預測能力亦值得關注')

# ============================================================
# Section 4: 關鍵洞察
# ============================================================
print('\n' + '=' * 70)
print('Section 4: 關鍵洞察')
print('=' * 70)

print('''
  1. 疫情預測最準確（平均分最高）
     → 疫情作為全球性重大事件，盤面信息最明顯

  2. 香港通關時間預測有偏差
     → 原因可能是：預測時未考慮香港第五波疫情（2月）的突發影響
     → 通關最終延遲到 2022 年 12 月底 / 2023 年初才真正落實

  3. 趨勢判斷 > 時間點判斷
     → 「最後的瘋狂」「逐漸消退」等趨勢描述極為準確
     → 「六月」「十二月」等具體時間點大致吻合但有誤差

  4. 經濟行業預測分化
     → 負面預測（壓制、重災區）比正面預測更準
     → 行業細分預測的準確度需要更多數據驗證
''')

# ============================================================
# Section 5: 輸出結構化 JSON
# ============================================================
output = {
    'episode': 'EP25',
    'title': '壬寅年（2022）年度預測',
    'quantify_date': str(datetime.now().date()),
    'total_predictions': total,
    'avg_score': round(avg_score, 2),
    'perfect_count': perfect,
    'good_count': good,
    'partial_count': partial,
    'wrong_count': wrong,
    'category_scores': {cat: round(sum(p['score'] for p in preds)/len(preds), 2)
                        for cat, preds in categories.items()},
    'methodology_avg': round(meth_avg, 2),
    'timing_avg': round(time_avg, 2),
    'predictions': predictions,
}

output_path = '../../download/ep25_renyin_prediction.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
print(f'  結構化數據已保存: {output_path}')

print('\n' + '=' * 70)
print('EP25 量化完成')
print('=' * 70)
