-- Global Energy & Oil Business Analysis
-- Assumed SQL dialect: PostgreSQL
-- Load CSVs into tables named:
-- country_master, energy_monthly_master, global_market_monthly_master,
-- macro_annual_master, oil_trade_master, oil_consumption_master,
-- fx_annual_master_historical, energy_shock_scores

-- 01. Data-quality profile
SELECT 'country_master' AS table_name, COUNT(*) AS rows,
       SUM(CASE WHEN iso3 IS NULL THEN 1 ELSE 0 END) AS missing_iso3
FROM country_master
UNION ALL
SELECT 'energy_monthly_master', COUNT(*),
       SUM(CASE WHEN production_total_tbpd IS NULL OR production_crude_tbpd IS NULL THEN 1 ELSE 0 END)
FROM energy_monthly_master
UNION ALL
SELECT 'macro_annual_master', COUNT(*),
       SUM(CASE WHEN gdp_usd IS NULL OR gdp_growth_pct IS NULL OR inflation_pct IS NULL THEN 1 ELSE 0 END)
FROM macro_annual_master;

-- 02. Negative production quality check
SELECT *
FROM energy_monthly_master
WHERE production_total_tbpd < 0
   OR production_crude_tbpd < 0;

-- 03. Top crude producers in latest month
WITH latest AS (
    SELECT MAX(period) AS period FROM energy_monthly_master
)
SELECT country_name,
       production_crude_tbpd
FROM energy_monthly_master e
JOIN latest l ON e.period = l.period
ORDER BY production_crude_tbpd DESC
LIMIT 10;

-- 04. Brent / WTI trend
SELECT period, brent_usd_bbl, wti_usd_bbl,
       brent_usd_bbl - wti_usd_bbl AS brent_wti_spread
FROM global_market_monthly_master
ORDER BY period;

-- 05. Highest oil import burden
SELECT country_name,
       crude_import_burden_pct_gdp,
       oil_intensity_twh_per_billion_gdp,
       currency_depreciation_pct
FROM energy_shock_scores
WHERE crude_import_burden_pct_gdp IS NOT NULL
ORDER BY crude_import_burden_pct_gdp DESC
LIMIT 10;

-- 06. Highest crude export dependence
SELECT country_name,
       crude_export_dependence_pct_gdp,
       net_importer
FROM energy_shock_scores
WHERE crude_export_dependence_pct_gdp IS NOT NULL
ORDER BY crude_export_dependence_pct_gdp DESC
LIMIT 10;

-- 07. Net oil trade exposure by country
SELECT country_name,
       crude_oil_import_usd,
       crude_oil_export_usd,
       crude_oil_export_usd - crude_oil_import_usd AS net_trade_balance_usd
FROM oil_trade_master
ORDER BY net_trade_balance_usd DESC;

-- 08. Oil consumption growth by country
WITH x AS (
    SELECT country_name, year, oil_consumption_twh,
           LAG(oil_consumption_twh) OVER (
               PARTITION BY country_name ORDER BY year
           ) AS prior_consumption
    FROM oil_consumption_master
)
SELECT country_name, year, oil_consumption_twh, prior_consumption,
       100.0 * (oil_consumption_twh - prior_consumption)
       / NULLIF(prior_consumption,0) AS yoy_growth_pct
FROM x
WHERE prior_consumption IS NOT NULL;

-- 09. Macro relationship: growth and inflation by year
SELECT year,
       AVG(gdp_growth_pct) AS avg_gdp_growth_pct,
       AVG(inflation_pct) AS avg_inflation_pct
FROM macro_annual_master
GROUP BY year
ORDER BY year;

-- 10. Country-level macro + oil exposure
SELECT m.country_name, m.year, m.gdp_usd, m.gdp_growth_pct,
       m.inflation_pct, c.oil_consumption_twh,
       f.exchange_rate_lcu_per_usd
FROM macro_annual_master m
LEFT JOIN oil_consumption_master c
  ON m.iso3 = c.iso3 AND m.year = c.year
LEFT JOIN fx_annual_master_historical f
  ON m.iso3 = f.iso3 AND m.year = f.year;

-- 11. Rank countries within income group by import vulnerability
SELECT income_group, country_name,
       crude_import_burden_pct_gdp,
       RANK() OVER (
         PARTITION BY income_group
         ORDER BY crude_import_burden_pct_gdp DESC
       ) AS vulnerability_rank
FROM energy_shock_scores
WHERE crude_import_burden_pct_gdp IS NOT NULL;

-- 12. Integrated screening score
-- A simple analytical score; weights should be validated with business stakeholders.
SELECT country_name,
       0.40 * COALESCE(crude_import_burden_pct_gdp,0)
     + 0.30 * COALESCE(oil_intensity_twh_per_billion_gdp,0)
     + 0.30 * GREATEST(COALESCE(currency_depreciation_pct,0),0) AS oil_shock_screen_score
FROM energy_shock_scores
ORDER BY oil_shock_screen_score DESC;
