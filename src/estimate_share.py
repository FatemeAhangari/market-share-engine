from pathlib import Path
import pandas as pd

ROOT = Path(__file__).parents[1]
df = pd.read_csv(ROOT / "data" / "synthetic_market.csv")

GROUP = ["mode", "origin", "destination", "operator"]
market = df.groupby(["mode","origin","destination"], as_index=False).agg(
    market_tickets=("tickets_sold","sum"),
    market_capacity=("available_seats","sum"),
    market_searches=("searches","sum"),
)
op = df.groupby(GROUP, as_index=False).agg(
    tickets_sold=("tickets_sold","sum"),
    revenue_toman=("revenue_toman","sum"),
    capacity=("available_seats","sum"),
    searches=("searches","sum"),
)
out = op.merge(market, on=["mode","origin","destination"], how="left")
out["market_share"] = out["tickets_sold"] / out["market_tickets"]
out["load_factor"] = out["tickets_sold"] / out["capacity"]
out["search_share"] = out["searches"] / out["market_searches"]
# Confidence is a transparent data-quality heuristic, not a statistical CI.
volume_score = (out["tickets_sold"].clip(0, 50000) / 50000)
coverage_score = (out["capacity"] / out["market_capacity"]).clip(0, 1)
out["confidence_score"] = (0.55 * volume_score + 0.45 * coverage_score).clip(0,1)
out.to_csv(ROOT / "data" / "market_share_estimates.csv", index=False)
print(out.sort_values("market_share", ascending=False).head(20).to_string(index=False))
