from pathlib import Path
import pandas as pd

ROOT = Path(__file__).parents[1]
DATA = ROOT / "data" / "synthetic_market.csv"


def load_data():
    return pd.read_csv(DATA)


def test_required_columns_exist():
    df = load_data()
    required = {
        "mode", "origin", "destination", "operator",
        "available_seats", "tickets_sold", "avg_fare_toman",
        "revenue_toman", "searches", "bookings", "cancellations",
    }
    assert required.issubset(df.columns)


def test_sold_tickets_do_not_exceed_capacity():
    df = load_data()
    assert (df["tickets_sold"] <= df["available_seats"]).all()


def test_bookings_do_not_exceed_searches():
    df = load_data()
    assert (df["bookings"] <= df["searches"]).all()


def test_revenue_is_non_negative():
    df = load_data()
    assert (df["revenue_toman"] >= 0).all()


def test_fares_are_positive():
    df = load_data()
    assert (df["avg_fare_toman"] > 0).all()


def test_cancellations_do_not_exceed_bookings():
    df = load_data()
    assert (df["cancellations"] <= df["bookings"]).all()
