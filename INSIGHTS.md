# Product Insights

These observations are derived from the synthetic dataset and are intended to demonstrate how market data can be translated into product questions.

## 1. Demand differs materially by route

Ticket volume and search volume vary substantially across routes. This suggests that market sizing should not rely on a single global conversion assumption.

**Product implication:** route-level assumptions and benchmarks are more useful than one market-wide benchmark.

## 2. Capacity is an important constraint

Observed tickets are bounded by available seats, making capacity a useful signal when estimating the addressable observed market.

**Product implication:** supply-side data should be combined with demand signals rather than treating searches as direct demand.

## 3. Search volume and ticket volume are not interchangeable

A high number of searches does not necessarily translate into the same number of tickets. Booking/search conversion varies by route and mode.

**Product implication:** search share can be a leading indicator, but it should not be presented as market share.

## 4. Market share needs an explicit denominator

Observed operator share answers:

> "What percentage of observed tickets in this dataset belongs to each operator?"

It does **not** automatically answer:

> "What percentage of the real market does each operator own?"

The second question requires an estimated or externally validated market denominator.

## 5. Uncertainty should be a first-class product output

The prototype exposes a confidence score based on data quality and signal consistency.

**Product implication:** market intelligence should communicate both the estimate and how much trust the user should place in it.

## Limitations

- Data is synthetic/generated.
- The market-size model is a transparent prototype, not a validated forecasting model.
- Confidence is a heuristic, not a statistical confidence interval.
- No external benchmark is used.
- Results should not be interpreted as real market shares or Alibaba metrics.
