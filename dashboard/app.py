from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).parents[1]
DATA = ROOT / "data" / "synthetic_market.csv"

st.set_page_config(page_title="Market Share Engine", page_icon="📊", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv(DATA)

df = load_data()

st.title("Market Share Engine")
st.caption("Synthetic market intelligence dashboard — portfolio prototype")

# Filters
c1, c2, c3 = st.columns(3)
with c1:
    mode = st.selectbox("Mode", ["All"] + sorted(df["mode"].unique().tolist()))
with c2:
    routes = sorted((df["origin"] + " → " + df["destination"]).unique().tolist())
    route = st.selectbox("Route", ["All"] + routes)
with c3:
    operators = sorted(df["operator"].unique().tolist())
    operator = st.selectbox("Operator", ["All"] + operators)

filtered = df.copy()
if mode != "All":
    filtered = filtered[filtered["mode"] == mode]
if route != "All":
    origin, destination = route.split(" → ")
    filtered = filtered[
        (filtered["origin"] == origin) & (filtered["destination"] == destination)
    ]
if operator != "All":
    filtered = filtered[filtered["operator"] == operator]

if filtered.empty:
    st.warning("No data matches the selected filters.")
    st.stop()

# Market metrics
market_tickets = filtered["tickets_sold"].sum()
capacity = filtered["available_seats"].sum()
searches = filtered["searches"].sum()
revenue = filtered["revenue_toman"].sum()

k1, k2, k3, k4 = st.columns(4)
k1.metric("Observed tickets", f"{market_tickets:,.0f}")
k2.metric("Capacity", f"{capacity:,.0f}")
k3.metric("Load factor", f"{market_tickets / capacity:.1%}" if capacity else "—")
k4.metric("Searches", f"{searches:,.0f}")

st.divider()

# Operator share
st.subheader("Operator market share")

share = (
    filtered.groupby("operator", as_index=False)
    .agg(tickets_sold=("tickets_sold", "sum"), revenue_toman=("revenue_toman", "sum"))
)
share["market_share"] = share["tickets_sold"] / share["tickets_sold"].sum()
share = share.sort_values("market_share", ascending=False)

left, right = st.columns(2)
with left:
    st.bar_chart(share.set_index("operator")["market_share"], y_label="Share")
with right:
    display = share.copy()
    display["market_share"] = display["market_share"].map(lambda x: f"{x:.1%}")
    display["revenue_toman"] = display["revenue_toman"].map(lambda x: f"{x:,.0f}")
    display.columns = ["Operator", "Tickets", "Revenue (Toman)", "Market share"]
    st.dataframe(display, hide_index=True, use_container_width=True)

# Trend
st.subheader("Monthly demand trend")
trend = (
    filtered.groupby("month", as_index=False)
    .agg(
        tickets_sold=("tickets_sold", "sum"),
        searches=("searches", "sum"),
    )
    .sort_values("month")
)
st.line_chart(trend.set_index("month")[["tickets_sold", "searches"]])

st.info(
    "Data is synthetic/generated for portfolio purposes. "
    "Market share shown here is observed share within the dataset, "
    "not a claim about any real market or company."
)
