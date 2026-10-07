# Excel tasks (steps)
| Task | How |
|---|---|
| Statistical summary of `amt`, `city_pop` | Data → Data Analysis → Descriptive Statistics |
| Histogram of `amt` | Select column → Insert → Charts → Histogram |
| Frauds by gender & category | PivotTable: Rows = gender, category; Values = count of is_fraud; Filter is_fraud = 1 |
| Top 3 states by transactions | PivotTable: Rows = state; Values = count; sort descending |
| Correlation amt vs city_pop | `=CORREL(amt_range, city_pop_range)` |
| Avg amount by job | PivotTable: Rows = job; Values = average of amt |
