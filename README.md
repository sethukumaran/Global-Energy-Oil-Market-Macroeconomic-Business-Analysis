# Global-Energy-Oil-Market-Macroeconomic-Business-Analysis

## Executive Summary

This project analyzes an integrated global dataset covering **150 countries**, monthly energy production, global Brent/WTI oil benchmarks, annual macroeconomic indicators, crude-oil trade, oil consumption, foreign exchange and a pre-calculated energy-shock screening dataset.

The objective is to answer a senior-analyst question:

 **Which countries and markets are most exposed to oil-price, oil-import and currency shocks, and what commercial actions should decision-makers consider?**

### Key findings from the supplied data

- **Brent oil prices** range from **$18.38/bbl** to **$125.45/bbl** over the available monthly history.
- The dataset's highest crude-import burden is **Brunei Darussalam at 26.91% of GDP**.
- The highest crude-export dependence is **Iraq at 33.98% of GDP**.
- The highest oil-intensity observation is **Libya at 2.69 TWh per $1B GDP**.
- **40 countries** have a non-null net-importer flag equal to 1 in the shock-score table.
- Average GDP growth across the macro panel moved from **-4.22% in 2020** to **5.58% in 2021**, indicating a clear shock/recovery pattern.
- **928 energy-production records are negative**, which should be investigated before productionizing the analysis.

## Dataset Architecture

| File | Grain | Purpose |
|---|---|---|
| `01_country_master.csv` | Country | Country/region/income-group dimension |
| `02_energy_monthly_master.csv` | Country-month | Energy and crude production |
| `03_global_market_monthly_master.csv` | Month | Brent and WTI benchmarks |
| `04_macro_annual_master.csv` | Country-year | GDP, growth, inflation, trade |
| `05_oil_trade_master.csv` | Country-year | Crude imports and exports |
| `06_oil_consumption_master.csv` | Country-year | Oil consumption |
| `07_fx_annual_master_historical.csv` | Country-year | Local-currency-per-USD FX |
| `08_energy_shock_scores.csv` | Country | Integrated oil/FX vulnerability measures |

## Business Questions

1. Which countries are the largest crude producers?
2. How volatile are Brent and WTI prices?
3. Which economies have the largest crude-import burden?
4. Which oil exporters are most dependent on crude exports?
5. Which markets have the highest oil intensity?
6. Where does currency depreciation amplify the local-currency oil bill?
7. How do oil exposure and macroeconomic performance interact?
8. Which markets should be prioritized for hedging, procurement, energy efficiency or scenario planning?

## Senior Analyst Business Insights

### 1. Importer vulnerability
High crude-import burden means a rise in global oil prices can transfer directly into the external account and domestic cost structure. Markets should be prioritized when **import burden + oil intensity + FX depreciation** are simultaneously high.

### 2. Exporter concentration risk
High crude-export dependence creates the opposite exposure: falling oil prices can pressure export earnings, government revenues, FX liquidity and investment.

### 3. Oil intensity as an efficiency signal
Oil consumption per $1B of GDP is useful for identifying economies where energy-efficiency programs, alternative fuels or logistics optimization could have relatively large economic benefits.

### 4. FX can amplify oil shocks
Because oil is internationally priced in USD, local-currency depreciation can increase the domestic cost of imported oil even when the USD oil price is unchanged. This is particularly important for treasury, procurement and pricing teams.

### 5. Commodity-cycle risk
The Brent/WTI series shows a wide price range, so static planning assumptions are inappropriate. Businesses should use at least three scenarios: **low-price, base-price and high-price**.

### 6. Macro shock/recovery
The macro panel shows a sharp deterioration in average GDP growth in 2020 followed by a strong rebound in 2021. Oil-sensitive sectors should therefore be evaluated using scenario-based rather than single-point forecasts.

## Recommended Business Actions

1. **Create an oil-shock scenario model** combining Brent price changes, FX depreciation and import burden.
2. **Prioritize hedging/procurement analysis** for high import-burden economies.
3. **Build exporter downside scenarios** for countries with high crude-export dependence.
4. **Target energy-efficiency investments** toward high oil-intensity markets.
5. **Develop a monthly executive dashboard** linking oil prices, production, consumption, trade, inflation and FX.
6. **Establish data-quality rules** for negative production, missing trade values and extreme macro observations.
7. **Use country segmentation** by region and income group to compare structural vulnerability rather than relying only on global averages.

## SQL Analysis

The SQL includes:
- data-quality checks
- negative production checks
- top producer ranking
- Brent/WTI spread analysis
- import burden ranking
- export dependence ranking
- net oil trade balance
- consumption YoY growth
- macro trend analysis
- integrated country joins
- income-group ranking
- an illustrative oil-shock screening score

## Python Analysis
The Python workflow performs:
- dataset loading
- schema and shape inspection
- duplicate checks
- missing-value analysis
- negative-value validation
- descriptive statistics
- time-series analysis
- country rankings
- macro relationship analysis
- business-risk screening
- visualization generation

## Visualizations

The `visualizations/` folder contains:
1. `01_oil_price_trend.png`
2. `02_top_crude_producers.png`
3. `03_growth_vs_inflation.png`
4. `04_import_burden.png`
5. `05_export_dependence.png`
6. `06_top_consumption_trend.png`
7. `07_currency_depreciation.png`
8. `08_oil_intensity.png`

## Data Quality & Limitations

The data contains meaningful missingness in oil trade, macro, FX and shock-score fields. Missing values should **not automatically be interpreted as zero**.
Important validation findings:
- Energy production contains negative records that require source-level investigation.
- Oil trade has substantial missing import/export observations.
- FX values are not directly comparable across countries without understanding currency denomination and methodology.
- The shock-score file contains derived measures; its calculation logic should be documented and validated before using it as an official risk score.
- Correlation should not be interpreted as causation.

## Conclusion

This project demonstrates how a data analyst can move from raw multi-source datasets to **decision-oriented business intelligence**.

The strongest analytical opportunity is not simply identifying which countries consume or produce the most oil. It is identifying **where oil-price exposure, economic dependence, oil intensity and currency movements interact**.

A practical executive output would be a country risk matrix with four dimensions:

**Oil import exposure → Oil intensity → FX amplification → Macro resilience**

This framework can support procurement strategy, commodity hedging, market prioritization, pricing decisions, energy-efficiency investment and scenario planning.
