"""
Global Energy & Oil Business Analysis

"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

BASE = Path(".")
OUT = BASE / "visualizations"
OUT.mkdir(exist_ok=True)

FILES = {
    "country": "01_country_master.csv",
    "energy": "02_energy_monthly_master.csv",
    "market": "03_global_market_monthly_master.csv",
    "macro": "04_macro_annual_master.csv",
    "trade": "05_oil_trade_master.csv",
    "consumption": "06_oil_consumption_master.csv",
    "fx": "07_fx_annual_master_historical.csv",
    "shock": "08_energy_shock_scores.csv",
}

country = pd.read_csv(BASE/FILES["country"])
energy = pd.read_csv(BASE/FILES["energy"])
market = pd.read_csv(BASE/FILES["market"], parse_dates=["period"])
macro = pd.read_csv(BASE/FILES["macro"])
trade = pd.read_csv(BASE/FILES["trade"])
consumption = pd.read_csv(BASE/FILES["consumption"])
fx = pd.read_csv(BASE/FILES["fx"])
shock = pd.read_csv(BASE/FILES["shock"])

# 1) Structure and quality
datasets = {"country":country,"energy":energy,"market":market,"macro":macro,
            "trade":trade,"consumption":consumption,"fx":fx,"shock":shock}
for name, df in datasets.items():
    print(f"\n{name}: {df.shape}")
    print("duplicates:", df.duplicated().sum())
    print("missing (%):")
    print((df.isna().mean()*100).round(2))

# 2) Explicit quality checks
print("\nNegative energy production:")
print(energy[(energy.production_total_tbpd < 0) | (energy.production_crude_tbpd < 0)].head())

# 3) Oil price trend
plt.figure(figsize=(10,6))
plt.plot(market.period, market.brent_usd_bbl, label="Brent")
plt.plot(market.period, market.wti_usd_bbl, label="WTI")
plt.title("Global Crude Oil Benchmarks")
plt.xlabel("Period"); plt.ylabel("USD/bbl"); plt.legend(); plt.tight_layout()
plt.savefig(OUT/"01_oil_price_trend.png", dpi=160); plt.close()

# 4) Latest production leaders
latest = energy.period.max()
top_prod = (energy[energy.period == latest]
            .sort_values("production_crude_tbpd", ascending=False).head(10)
            .sort_values("production_crude_tbpd"))
plt.figure(figsize=(10,6))
plt.barh(top_prod.country_name, top_prod.production_crude_tbpd)
plt.title(f"Top Crude Producers — {latest}")
plt.xlabel("Thousand barrels per day"); plt.tight_layout()
plt.savefig(OUT/"02_top_crude_producers.png", dpi=160); plt.close()

# 5) Macro relationship
y = macro.year.max()
tmp = macro[macro.year == y].dropna(subset=["inflation_pct","gdp_growth_pct"])
plt.figure(figsize=(10,6))
plt.scatter(tmp.inflation_pct, tmp.gdp_growth_pct, alpha=.65)
plt.title(f"GDP Growth vs Inflation — {y}")
plt.xlabel("Inflation (%)"); plt.ylabel("GDP Growth (%)"); plt.tight_layout()
plt.savefig(OUT/"03_growth_vs_inflation.png", dpi=160); plt.close()

# 6) Import burden
tmp = shock.dropna(subset=["crude_import_burden_pct_gdp"]).nlargest(
    10, "crude_import_burden_pct_gdp").sort_values("crude_import_burden_pct_gdp")
plt.figure(figsize=(10,6))
plt.barh(tmp.country_name, tmp.crude_import_burden_pct_gdp)
plt.title("Top Crude Import Burden")
plt.xlabel("Crude imports / GDP (%)"); plt.tight_layout()
plt.savefig(OUT/"04_import_burden.png", dpi=160); plt.close()

# 7) Export dependence
tmp = shock.dropna(subset=["crude_export_dependence_pct_gdp"]).nlargest(
    10, "crude_export_dependence_pct_gdp").sort_values("crude_export_dependence_pct_gdp")
plt.figure(figsize=(10,6))
plt.barh(tmp.country_name, tmp.crude_export_dependence_pct_gdp)
plt.title("Top Crude Export Dependence")
plt.xlabel("Crude exports / GDP (%)"); plt.tight_layout()
plt.savefig(OUT/"05_export_dependence.png", dpi=160); plt.close()

# 8) Oil consumption
top = consumption.groupby("country_name").oil_consumption_twh.mean().nlargest(8).index
trend = consumption[consumption.country_name.isin(top)].groupby("year").oil_consumption_twh.sum()
plt.figure(figsize=(10,6))
trend.plot()
plt.title("Oil Consumption Trend — Top Markets")
plt.xlabel("Year"); plt.ylabel("TWh"); plt.tight_layout()
plt.savefig(OUT/"06_top_consumption_trend.png", dpi=160); plt.close()

# 9) FX stress
tmp = shock.dropna(subset=["currency_depreciation_pct"]).nlargest(
    10, "currency_depreciation_pct").sort_values("currency_depreciation_pct")
plt.figure(figsize=(10,6))
plt.barh(tmp.country_name, tmp.currency_depreciation_pct)
plt.title("Largest Currency Depreciation Signals")
plt.xlabel("Depreciation (%)"); plt.tight_layout()
plt.savefig(OUT/"07_currency_depreciation.png", dpi=160); plt.close()

# 10) Oil intensity
tmp = shock.nlargest(10, "oil_intensity_twh_per_billion_gdp").sort_values(
    "oil_intensity_twh_per_billion_gdp")
plt.figure(figsize=(10,6))
plt.barh(tmp.country_name, tmp.oil_intensity_twh_per_billion_gdp)
plt.title("Highest Oil Intensity Economies")
plt.xlabel("TWh per $1B GDP"); plt.tight_layout()
plt.savefig(OUT/"08_oil_intensity.png", dpi=160); plt.close()

print("\nAnalysis complete. Charts saved in ./visualizations/")
