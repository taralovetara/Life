# EP24: 全局回顧 + 6 個 EP22 遺留兼容性修復

## 資料來源
天心堂坤正師傅 第二十四集（回顧+修復）

## 本集內容

### 1. 全局回顧 EP01-24
- 逐一檢查引擎代碼正確性
- 確認所有 EP 知識點正確融入 engine_v2.py
- 發現 6 個 EP22 轉盤改動引入嘅兼容性 bug

### 2. 修復嘅 6 個 Bug

| # | Bug 描述 | 影響 | 修復方式 |
|---|---------|------|----------|
| 1 | `find_palace_of()` 只用 `==` 匹配 | 天芮/天禽合併格式 `'天芮/天禽'` 搵唔到 | `==` 改為 `in str.split('/')` |
| 2 | `find_tiangan_palace()` 同上 | 乙/庚合併格式搵唔到 | 同上 |
| 3 | `get_tianyi_palace()` 同上 | 天乙查找失敗 | 同上 |
| 4 | `predict_health()` 用錯 dict | `tp.get` 應該用 `tg_map.get` | 改用正確 dict |
| 5 | `predict_criminal` R04 | `tg_map.get` 無 `split` | 加 `.split('/')[0]` |
| 6 | `predict_criminal` R05 | 庚檢測用 `==` | 改為 `.split('/')[0] in ...` |

### 3. Bug 根因分析
EP22 轉盤改動引入嘅核心變化：
- **天禽寄天芮**：`tp[p]` 變成 `'天芮/天禽'` 格式
- **中五天干寄宮**：`tg_map[p]` 變成 `'戊/己'` 格式
- 所有查找函數必須支援合併格式

### 4. 修復驗證
- 確認 `find_palace_of(engine, '天芮')` 能搵到合併格式
- 確認 `find_palace_of(engine, '天禽')` 也能搵到
- 確認疾病預測函數用正確 dict
- 確認刑事預測 R04/R05 正確匹配

## 引擎改動
- `find_palace_of()` — 支援合併格式查找
- `find_tiangan_palace()` — 支援合併格式查找
- `get_tianyi_palace()` — 支援合併格式查找
- `predict_health()` — 修正 dict 引用
- `predict_criminal()` — R04/R05 加 split
- engine_v2.py docstring 更新至 EP01-EP24
