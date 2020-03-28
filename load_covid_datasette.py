import sqlite3
import requests

import numpy as np
import pandas as pd

from pathlib import Path
from datetime import datetime


def get_sqlite_from_web():
    """
    Would be convenient to have at least a content-length or
    etag header for caching, caching for 2h for now
    """
    sqlite_db_path = Path("covid.db")
    # would be convenient to have at least a content-length or
    # etag header for caching, caching for 2h for now
    seconds_since_last_download = (
        datetime.now() - datetime.fromtimestamp(sqlite_db_path.stat().st_mtime)
    ).seconds
    outdated = seconds_since_last_download > 7200
    if not sqlite_db_path.exists() or outdated:
        response = requests.get("https://covid-19.datasettes.com/covid.db")
        with sqlite_db_path.open("wb") as f:
            f.write(response.content)
    return sqlite_db_path


def get_dataframe_from_sqlite(sqlite_db_path):
    conn = sqlite3.connect(sqlite_db_path)
    return pd.read_sql_query("select * from daily_reports", conn)


def initial_cleanup(df):
    """
    Renames some columns, groups by country and sums up numbers, drops
    states and filters relevant columns.
    """
    column_map = {"country_or_region": "country"}
    relevant_columns = ["country", "date", "confirmed", "deaths", "recovered", "active"]
    return (
        (
            df.assign(date=pd.to_datetime(df.day, yearfirst=True))
            .drop(columns=["day"])
            .rename(columns=column_map)
            .fillna(value={"active": 0})
        )[relevant_columns]
        .groupby(["country", "date"])
        .sum()
        .reset_index()
    )


def add_confirmed_after_n_days_column(df, n_days=100, relevant_threshold=1000):
    affected_countries = df[df.confirmed > relevant_threshold].country.unique()
    affected_country = df.country.isin(affected_countries)
    query = (df.confirmed >= n_days) & affected_country
    cols = ["country", "date"]
    date_since_n_lookup = dict(
        (df[query][cols].groupby("country").min().reset_index()).values
    )
    first_confirmed_date = f"first_{n_days}_confirmed_date"
    days_since = f"days_since_{n_days}"
    df[first_confirmed_date] = df.country.apply(lambda x: date_since_n_lookup.get(x))
    df[days_since] = (df.date - df[first_confirmed_date]).dt.days
    df = df.drop(columns=[first_confirmed_date])
    df = df.set_index("date")
    return df


def add_estimated_critical_cases(df):
    df["critical_estimate"] = (df.confirmed * 0.05).astype(np.int32)
    return df


def replace_country_names(df):
    total_countries = ["France", "United Kingdom", "US", "Canada", "Australia"]
    total_replacements = {tc: f"{tc} (total)" for tc in total_countries}
    return df.replace({"country": total_replacements})


def filter_by_number_of_days_after_100(df, filter_n_days_100):
    """Select countries for which we have at least some information."""
    countries = pd.Series(
        df.loc[df.days_since_100 >= filter_n_days_100].country.unique()
    )
    df = df.loc[lambda x: x.country.isin(countries)]
    return df


def load_data(filter_n_days_100=None):
    sqlite_db_path = get_sqlite_from_web()
    df = get_dataframe_from_sqlite(sqlite_db_path)
    df = initial_cleanup(df)
    df = add_confirmed_after_n_days_column(df)
    df = add_estimated_critical_cases(df)
    df = replace_country_names(df)
    if filter_n_days_100 is not None:
        df = filter_by_number_of_days_after_100(df, filter_n_days_100)
    return df
