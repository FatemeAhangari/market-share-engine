from pathlib import Path
import pandas as pd

ROOT = Path(__file__).parents[1]
df = pd.read_csv(ROOT / "data" / "synthetic_market.csv")

ROUTE = ["mode", "origin", "destination"]

# Estimate demand from two observable signals:
# 1) Capacity: observed seats divided by a route/mode benchmark load factor.
# 2) Search demand: searches multiplied by the observed booking/search conversion.
#
# The final estimate is a transparent blend, capped by available capacity.
route = df.groupby(ROUTE, as_index=False).agg(
    available_seats=("available_seats", "sum"),
    tickets_sold=("tickets_sold", "sum"),
    searches=("searches", "sum"),
    bookings=("bookings", "sum"),
)

route["observed_load_factor"] = (
    route["tickets_sold"] / route["available_seats"]
).clip(0.05, 0.98)

route["booking_search_rate"] = (
    route["bookings"] / route["searches"]
).clip(0.001, 0.50)

# A conservative benchmark prevents low-observation routes from implying
# unrealistic market sizes.
route["capacity_demand"] = (
    route["available_seats"] / route["observed_load_factor"]
)

route["search_demand"] = (
    route["searches"] * route["booking_search_rate"]
)

route["estimated_market_tickets"] = (
    0.60 * route["capacity_demand"]
    + 0.40 * route["search_demand"]
)

# The estimate cannot be below observed sold tickets.
route["estimated_market_tickets"] = route[
    ["estimated_market_tickets", "tickets_sold"]
].max(axis=1)

route["observed_share"] = (
    route["tickets_sold"] / route["estimated_market_tickets"]
).clip(0, 1)

# Model confidence is a data-quality score, not a statistical confidence interval.
volume_score = (route["tickets_sold"] / 50000).clip(0, 1)
signal_balance = (
    1
    - (
        (route["capacity_demand"] - route["search_demand"]).abs()
        / route[["capacity_demand", "search_demand"]].max(axis=1)
    )
).clip(0, 1)

route["confidence_score"] = (
    0.55 * volume_score + 0.45 * signal_balance
).clip(0, 1)

output = ROOT / "data" / "market_size_estimates.csv"
route.to_csv(output, index=False)

print(
    route.sort_values("estimated_market_tickets", ascending=False)
    .head(20)
    .to_string(index=False)
)
