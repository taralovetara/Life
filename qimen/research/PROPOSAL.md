# Research Proposal

## Cultural Alternative Data in Financial Risk Management
### An Empirical Study of Traditional Chinese Decision Frameworks as Predictive Signals in FX Markets

---

## 1. Research Background

### 1.1 The Rise of Alternative Data in Finance

Over the past decade, the financial industry has witnessed an explosion of alternative data sources used for risk management and alpha generation. Satellite imagery, social media sentiment, credit card transactions, and web scraping have become mainstream inputs for quantitative trading strategies. The global alternative data market is projected to exceed USD 100 billion by 2028, driven by institutional demand for non-traditional signals that offer incremental predictive power over conventional fundamental and technical indicators.

Despite this proliferation, one category of data remains almost entirely unexplored in academic finance: cultural decision frameworks. Across East Asia, hundreds of millions of individuals incorporate traditional metaphysical systems — such as Qimen Dunjia (奇門遁甲), Ziwei Doushu (紫微斗數), Bazi (八字), and Feng Shui (風水) — into their financial decision-making processes. These systems provide structured, quantifiable outputs that can be formalized as time-series signals, yet they have received virtually no rigorous empirical examination in the context of modern financial risk management.

### 1.2 Research Gap

Existing literature on cultural finance (Guiso, Sapienza & Zingales, 2006; Beckmann, Menkhoff & Suto, 2008) has examined how cultural values affect financial behavior at a macro level. Behavioral finance (Kahneman & Tversky, 1979; Thaler, 2015) has documented systematic cognitive biases in trading decisions. However, no study has systematically:

1. **Quantified** a traditional Chinese metaphysical system into a structured numerical indicator
2. **Tested** that indicator's predictive power using rigorous out-of-sample methodologies
3. **Evaluated** its incremental information value when combined with established technical indicators
4. **Assessed** its impact on risk metrics (VaR, CVaR, Maximum Drawdown, Sharpe Ratio)

This research addresses all four gaps using Qimen Dunjia (QMDJ) as the primary case study.

### 1.3 Why Qimen Dunjia?

QMDJ was selected for several methodological reasons:

- **Deterministic output**: Given identical inputs (date, time, location), the system produces identical outputs. This reproducibility is essential for scientific testing.
- **Temporal resolution**: QMDJ operates at the shichen (時辰) level — 2-hour intervals — providing sufficient granularity for short-term trading signal generation.
- **Multi-dimensional scoring**: The system evaluates multiple factors (celestial stems, earthly branches, nine stars, eight gates, eight deities, palace interactions, five-element relationships) and combines them into composite scores, analogous to multi-factor risk models.
- **Established quantitative framework**: Prior work in the Life project has already developed a computational engine (engine.py) that formalizes QMDJ into numerical outputs, providing a foundation for this research.

---

## 2. Research Questions

### Primary Question

> **RQ1**: Does Qimen Dunjia, when quantified as a structured trading signal, provide incremental predictive power for short-term FX market movements beyond conventional technical indicators?

### Secondary Questions

> **RQ2**: What is the marginal contribution of QMDJ signals to portfolio risk metrics (VaR, CVaR, Maximum Drawdown, Sharpe Ratio) when used as a filter or supplementary input?

> **RQ3**: How does the predictive performance of QMDJ signals vary across different market regimes (trending vs. range-bound, high vs. low volatility)?

> **RQ4**: Can machine learning models effectively leverage QMDJ features, and which algorithmic architectures are most suited to this type of cultural alternative data?

> **RQ5**: What are the behavioral implications of using cultural decision frameworks — do they improve or impair risk-adjusted decision quality compared to purely quantitative approaches?

---

## 3. Research Objectives

### 3.1 Primary Objectives

1. **Formalize** QMDJ into a reproducible, time-series trading signal (Qimen Signal Index, QSI)
2. **Backtest** QSI-based trading strategies on historical FX data (EUR/USD, GBP/USD, USD/JPY)
3. **Evaluate** the incremental information value of QSI using machine learning benchmarks
4. **Quantify** the impact on risk management metrics

### 3.2 Secondary Objectives

5. **Compare** QSI performance across different asset classes (FX, commodities, equity indices)
6. **Analyze** the sensitivity of QSI to its component sub-signals (stars, gates, deities, five-element interactions)
7. **Investigate** regime-dependent effectiveness
8. **Provide** a methodological template for evaluating other cultural decision frameworks as alternative data sources

---

## 4. Conceptual Framework

### 4.1 The Qimen Signal Index (QSI)

The core contribution of this research is the formalization of QMDJ into a structured index:

```
QSI(t) = w1 * Star_Score(t) + w2 * Gate_Score(t) + w3 * Deity_Score(t)
        + w4 * Stem_Branch_Relation(t) + w5 * Pattern_Bonus(t)
        + w6 * Void_Penalty(t) + w7 * Fuyin_Penalty(t)
```

Where each component is derived from the QMDJ computational engine:

| Component | Source | Range | Description |
|-----------|--------|-------|-------------|
| Star_Score | Nine Stars (九星) in target palaces | [-3, +3] | Celestial influence on outcome |
| Gate_Score | Eight Gates (八門) in target palaces | [-3, +3] | Human action doors |
| Deity_Score | Eight Deities (八神) in target palaces | [-2, +2] | Environmental/spiritual factors |
| Stem_Branch_Relation | Five-element generation/restraint | [-2, +2] | Palace-element interactions |
| Pattern_Bonus | Auspicious/inauspicious patterns (格局) | [-3, +3] | Special combinations |
| Void_Penalty | Void branches (空亡) affecting key palaces | [-2, 0] | Nullification penalty |
| Fuyin_Penalty | Stagnation pattern (伏吟) | [-1, 0] | No-change penalty |

The weights (w1-w7) will be calibrated using both traditional QMDJ theory (domain-driven) and empirical optimization (data-driven), with a comparison between the two approaches.

### 4.2 Asset-Specific Yong Shen (用神) Mapping

The QSI is context-dependent — different financial instruments require different "focus palaces" (用神). The mapping logic:

| Instrument | Direction | Yong Shen Configuration |
|------------|-----------|----------------------|
| EUR/USD (long) | Bullish | Sheng Gate (生門) + Metal Palace (Qian 6/Dui 7) |
| EUR/USD (short) | Bearish | Jing Gate (驚門) + Fire Palace (Li 9) |
| GBP/USD | Dynamic | Based on currency element analysis |
| Gold (XAU/USD) | Dynamic | Earth-Metal palace interactions |

### 4.3 Signal-to-Decision Pipeline

```
DateTime Input
    ↓
QMDJ Engine (engine.py)
    ↓
Nine Palaces Layout (地/天/人/神盤)
    ↓
Component Scoring (7 dimensions)
    ↓
QSI(t) = weighted composite score
    ↓
Trading Decision Rule:
    QSI ≥ +2  →  LONG
    QSI ≤ -2  →  SHORT
    -2 < QSI < +2 → NO POSITION
    ↓
Position Duration: 1-2 shichen (2-4 hours)
```

---

## 5. Literature Review

### 5.1 Alternative Data in Finance

- **Bollen, Mao & Zeng (2011)**: Twitter mood predicts stock market (precursor to sentiment-as-alternative-data)
- **Cavallo, Cavallo & Rigobon (2023)**: Online price data for inflation nowcasting
- **Gao, targetal. (2020)**: Satellite imagery for economic activity prediction
- **Scholz & Yim (2022)**: A comprehensive taxonomy of alternative data for investment

### 5.2 Behavioral Finance

- **Kahneman & Tversky (1979)**: Prospect Theory — irrational decision-making under risk
- **Thaler (2015)**: Misbehaving — systematic biases in financial decisions
- **Shiller (2019)**: Narrative Economics — stories drive economic behavior
- **Tversky & Kahneman (1974)**: Heuristics and biases in judgment

### 5.3 Cultural Finance

- **Guiso, Sapienza & Zingales (2006)**: Does culture affect economic outcomes?
- **Beckmann, Menkhoff & Suto (2008)**: Does culture influence asset managers' views?
- **Chui, Titman & Wei (2010)**: Individualism and momentum around the world
- **Karolyi (2016)**: Cultural finance: a review and assessment

### 5.4 Chinese Metaphysical Systems in Academic Context

- **Smith (1991)**: Fortune-tellers and philosophers: Divination in traditional Chinese society
- **Sung (2017)**: A brief history of Chinese fortune-telling (historical overview)
- **Existing gap**: No peer-reviewed study has empirically tested Chinese metaphysical systems as trading signals using modern quantitative methods

---

## 6. Methodology Overview

### 6.1 Research Design

This study employs a **quantitative, experimental research design** with four sequential phases:

```
Phase 1: Signal Construction (Months 1-3)
    → Formalize QMDJ engine, generate QSI time series

Phase 2: Backtesting (Months 4-6)
    → Historical performance evaluation of QSI-based strategies

Phase 3: Machine Learning Evaluation (Months 7-12)
    → Predictive power tests, incremental value analysis

Phase 4: Risk Analysis (Months 13-15)
    → Risk metrics comparison, regime analysis

Phase 5: Writing & Defense (Months 16-24)
    → Dissertation, publications, defense preparation
```

### 6.2 Data Requirements

| Data Type | Source | Period | Frequency |
|-----------|--------|--------|-----------|
| FX OHLC | Bloomberg / Dukascopy | 2015-2026 | 1-hour |
| QMDJ Calculations | Life/engine.py | 2015-2026 | Per shichen (2h) |
| Technical Indicators | Calculated from OHLC | 2015-2026 | 1-hour |
| Macro Data | FRED / BIS | 2015-2026 | Daily |
| Volatility Index | CBOE / investing.com | 2015-2026 | Daily |

### 6.3 Machine Learning Models

| Model | Rationale | Expected Strength |
|-------|-----------|------------------|
| Logistic Regression | Baseline, interpretable | Coefficient significance testing |
| Random Forest | Non-linear relationships | Feature importance ranking |
| XGBoost | Gradient boosting, robust | Best-in-class tabular performance |
| LSTM | Temporal dependencies | Sequential pattern capture |
| LightGBM | Efficiency, regularization | Large-scale feature engineering |

### 6.4 Risk Metrics

- **Value at Risk (VaR)** — Parametric (95%, 99%) and Historical
- **Conditional VaR (CVaR / Expected Shortfall)** — Tail risk
- **Maximum Drawdown** — Peak-to-trough decline
- **Sharpe Ratio** — Risk-adjusted return
- **Sortino Ratio** — Downside risk-adjusted return
- **Calmar Ratio** — Return / Maximum Drawdown
- **Win Rate & Profit Factor** — Strategy-level metrics

---

## 7. Expected Contributions

### 7.1 Theoretical Contributions

1. **First empirical study** to rigorously quantify and test a Chinese metaphysical system as a financial trading signal using machine learning
2. **Methodological template** for evaluating other cultural decision frameworks as alternative data
3. **Bridge** between cultural finance, behavioral finance, and financial technology

### 7.2 Practical Contributions

4. A **reproducible QSI calculation engine** (open-source, Python)
5. A **benchmark dataset** of QMDJ signals aligned with FX price data
6. **Actionable insights** for risk managers on the value (or lack thereof) of cultural alternative data

### 7.3 Policy Implications

7. If QMDJ signals demonstrate predictive power, this raises questions about **market efficiency** and whether culturally-influenced trading behavior creates exploitable patterns
8. If QMDJ signals show no predictive power, this provides **evidence-based guidance** against relying on such systems, contributing to financial literacy

---

## 8. Timeline

| Phase | Duration | Deliverables |
|-------|----------|-------------|
| Signal Construction | Months 1-3 | QSI engine, validation tests, preliminary data |
| Backtesting | Months 4-6 | Backtest results, strategy comparison report |
| ML Evaluation | Months 7-12 | Model comparison, feature importance, ablation study |
| Risk Analysis | Months 13-15 | Risk metrics report, regime analysis |
| Writing | Months 16-22 | Dissertation chapters, conference papers |
| Revision & Defense | Months 23-24 | Final dissertation, defense preparation |

---

## 9. Potential Limitations

1. **Data availability**: High-quality historical FX data with precise timestamps may require paid sources
2. **QMDJ calculation accuracy**: Relies on correct jieqi (節氣) dates; approximate dates introduce noise
3. **Cultural specificity**: Findings may not generalize to non-East-Asian markets or cultural contexts
4. **Publication bias risk**: Null results (no predictive power) may be less publishable, though we argue null results are equally valuable
5. **Computational complexity**: Full backtest across multiple currencies and 10+ years of data requires significant computing resources

---

## 10. References

*(To be expanded)*

- Bollen, J., Mao, H., & Zeng, X. (2011). Twitter mood predicts the stock market. *Journal of Computational Science*, 2(1), 1-8.
- Beckmann, D., Menkhoff, L., & Suto, M. (2008). Does culture influence asset managers' views and behavior? *Journal of Economic Behavior & Organization*, 67(3-4), 624-643.
- Cavallo, A., Cavallo, A., & Rigobon, R. (2023). Online and official price indexes: Measuring Argentina's inflation. *Journal of Monetary Economics*, 134, S1-S18.
- Chui, A. C., Titman, S., & Wei, K. J. (2010). Individualism and momentum around the world. *The Journal of Finance*, 65(1), 361-392.
- Guiso, L., Sapienza, P., & Zingales, L. (2006). Does culture affect economic outcomes? *Journal of Economic Perspectives*, 20(2), 23-48.
- Kahneman, D., & Tversky, A. (1979). Prospect theory: An analysis of decision under risk. *Econometrica*, 47(2), 263-291.
- Karolyi, G. A. (2016). Cultural finance: A review and assessment. *Annual Review of Financial Economics*, 8, 437-461.
- Scholz, M., & Yim, B. (2022). Alternative data for investment: A taxonomy. *The Journal of Financial Data Science*, 4(2), 66-83.
- Shiller, R. J. (2019). *Narrative Economics: How Stories Go Viral and Shape Major Economic Events*. Princeton University Press.
- Thaler, R. H. (2015). *Misbehaving: The Making of Behavioral Economics*. W. W. Norton & Company.
- Tversky, A., & Kahneman, D. (1974). Judgment under uncertainty: Heuristics and biases. *Science*, 185(4157), 1124-1131.
