# 2024 Presidential Election Forecast Scrapers

A collection of Python scrapers built to collect state-level win probability data from six major 2024 presidential election forecast models on Election Day (November 5, 2024). Output data feeds a comparative dashboard built in Observable.

**[View the Observable Dashboard](https://observablehq.com/@robertmreedy/2024-presidential-election-forecasts)**

---

## What This Project Does

Each scraper targets a different forecast model and extracts state-by-state win probabilities for the 2024 presidential race. The outputs are joined into a master dataset used to compare model consensus, divergence, and expected value across states.

**Models scraped:**
- [FiveThirtyEight](https://projects.fivethirtyeight.com/2024-election-forecast/)
- [JHK Forecasts](https://projects.jhkforecasts.com/2024/president/#standard)
- [Decision Desk HQ](https://elections2024.thehill.com/forecast/2024/president/)
- [Race to the WH](https://www.racetothewh.com/president/2024)

> Silver Bulletin and The Economist state-level odds were behind a paywall at time of collection and are not included in the scraped outputs. National odds for these models are included manually in the dashboard.

---

## Repo Structure

```
election-2024-forecast-scrapers/
├── scrapers/
│   ├── fte_state_odds.py          # FiveThirtyEight scraper (Selenium/headless Chrome)
│   ├── jhk_state_odds.py          # JHK Forecasts scraper
│   ├── ddhq_state_odds.py         # Decision Desk HQ scraper
│   └── rtwh_state_odds.py         # Race to the WH scraper
├── data/
│   ├── master_data_join.csv       # Joined dataset across all models, used in Observable
│   ├── pres24_538_scrape_stateodds_output.csv
│   ├── pres24_ddhq_scrape_stateodds_output.csv
│   ├── pres24_jhk_scrape_statesodds_output_v2.csv
│   └── pres24_rwh_scrape_stateodds_output.csv
└── analysis/
    └── expected_value.py          # Expected value calculations across model forecasts
```

---

## Data Schema

Each scraper outputs a two-column CSV:

| Column | Description |
|---|---|
| `State` | State name (title case); includes "Electoral College" row for national odds |
| `[Model]` | Democratic win probability as a decimal (e.g., 0.72 = 72%) |

`master_data_join.csv` merges all model outputs on `State`, with one column per model.

---

## Data Collection Note

All data was captured on **November 5, 2024 at approximately 5:45 PM ET** — Election Day, prior to poll closings. This is a point-in-time snapshot, not a live pipeline.
