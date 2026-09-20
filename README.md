# Market Share Engine

An automated market intelligence prototype for estimating market size and competitor share from fragmented signals.

## Product problem

Market-share estimation is often a periodic, manual process: collect signals, normalize entities and time periods, estimate the market denominator, calculate share, and explain uncertainty.

This project explores how to turn that workflow into a repeatable decision-support system.

## Pipeline

**Sources → Normalization → Market-size estimation → Share calculation → Confidence → Dashboard**

### Current components

- `data/synthetic_market.csv` — generated monthly Bus/Train market signals
- `src/estimate_market_size.py` — explainable market-size estimation
- `src/estimate_share.py` — operator-level share and demand metrics
- `tests/test_estimation.py` — data-quality validation tests
- `dashboard/app.py` — interactive Streamlit dashboard

## Dashboard

The dashboard provides:

- Route / mode / operator filters
- Observed ticket and capacity KPIs
- Operator market-share comparison
- Revenue and ticket tables
- Monthly demand trends

Run locally:

```bash
pip install -r dashboard/requirements.txt
streamlit run dashboard/app.py
```

## Methodology

The market-size model combines two observable demand signals:

1. **Capacity-based demand:** observed available seats adjusted by the observed load factor.
2. **Search-based demand:** searches adjusted by the observed booking/search rate.

The current prototype blends these signals using a transparent weighted model and ensures that estimated market volume is not below observed ticket sales.

**Important:** the model is a portfolio prototype, not a validated market-sizing methodology. Its confidence score is a data-quality heuristic, not a statistical confidence interval.

## Product thinking

**Question → Data → Model → Validation → Decision**

The goal is not to produce a precise number from incomplete data. The goal is to make assumptions explicit, quantify uncertainty, and create a repeatable workflow that can improve as better signals become available.

## Data

All data in this repository is synthetic/generated for portfolio purposes. It does not represent Alibaba or any real company's market share.

## Next steps

- Add automated model tests
- Compare alternative market-size assumptions
- Add time-series stability analysis
- Add confidence/uncertainty visualization
- Calibrate the model against an external benchmark when available

## Portfolio focus

Product analytics · Market intelligence · Data systems · Estimation under uncertainty · Automation · Decision support

## Status

🚧 In development
