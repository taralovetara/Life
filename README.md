# Life — 紫微斗數量化系統

將紫微斗數術數運算邏輯量化成數學模型，用 Python 實現。

## 核心理念

術數運算可以量化成數字。傳統紫微斗數依賴文字解讀，本系統將其轉化為數值分數，實現確定性計算。

## 量化框架

### 星曜亮度（6級制）

| 等級 | 分數 | 說明 |
|------|------|------|
| 廟   | 5    | 星曜最強狀態 |
| 旺   | 4    | 星曜次強狀態 |
| 得地 | 3    | 星曜得力 |
| 利   | 2    | 星曜有利 |
| 平   | 1    | 星曜平淡 |
| 不落 | 0    | 星曜不在該宮位 |

### 四化權重

| 四化 | 權重 |
|------|------|
| 化祿 | +3.0 |
| 化權 | +2.0 |
| 化科 | +1.5 |
| 化忌 | -4.0 |

### 宮位評分公式

```
宮位分數 = Σ(主星亮度 × 主星權重)
           + Σ(吉星權重)
           - Σ(煞星權重)
           + Σ(四化權重)
```

分數範圍：約 -10 ~ +30（空宮約 0 分）

### 歸一化到 0-100

原始分透過線性映射歸一化：`(score - (-5)) / (25 - (-5)) × 100`

### 綜合分（Full Score）

6 個人生面向（事業運/財運/感情運/健康運/人際運/家運）各自歸一化後取平均。

**理論 Full Score = 100**（6 面向全滿分）

實際上因為星曜分佈有固定規則約束，100 分基本上不可能達到。
參考值：

| 平均宮分 | 歸一化 |
|----------|--------|
| 10       | 50.0   |
| 12       | 56.7   |
| 15       | 66.7   |
| 18       | 76.7   |
| 20       | 83.3   |

## 模組結構

```
ziwei/
├── __init__.py      # 公開 API
├── __main__.py      # python -m ziwei 入口
├── constants.py     # 全部常量與查找表
├── calculator.py    # 排盤引擎
├── scorer.py        # 量化評分系統
├── timeline.py      # 大限/流年時間軸
└── cli.py           # 命令行界面
```

## 使用方法

### CLI

```bash
pip install -r requirements.txt

# 基本命盤 + 分數
python -m ziwei 1974 8 10 9.0 男

# 加大限總覽
python -m ziwei 1974 8 10 9.0 男 --dajun

# 加時間線
python -m ziwei 1974 8 10 9.0 男 --timeline 40 60
```

### Python API

```python
from ziwei import (
    build_chart,
    score_all_palaces,
    score_life_aspects_normalized,
    generate_timeline,
)

# 排盤
chart = build_chart(1974, 8, 10, 9.0, '男')

# 12宮評分
palace_scores = score_all_palaces(chart)

# 人生面向 (歸一化 0-100)
aspects = score_life_aspects_normalized(palace_scores)

# 時間線
timeline = generate_timeline(chart, 40, 60)
```

## 計算流程

```
公曆出生日期 + 時間 + 性別
        │
        ▼
   公曆 → 農曆轉換
        │
        ▼
   命宮位置公式: (2 + 月 - 時) mod 12
        │
        ▼
   五行局 (60甲子納音查表)
        │
        ▼
   紫微位置 (局數 + 日查表)
        │
        ▼
   14主星安星 (固定偏移)
        │
        ▼
   六吉六煞安星 (公式)
        │
        ▼
   四化標記 (年干查表)
        │
        ▼
   宮位評分 (亮度×權重 + 吉星 - 煞星 + 四化)
        │
        ▼
   人生面向加權組合 → 綜合分 0-100
```

## 依賴

- Python >= 3.8
- [zhdate](https://pypi.org/project/zhdate/) — 公曆/農曆轉換
