import yfinance as yf
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

def get_selected_symbol():
    try:
        with open("selected_symbol.txt", "r") as file:
            symbol = file.read().strip().upper()
    except FileNotFoundError:
        print("selected_symbol.txt not found")
        return None

    if not symbol:
        print("No stock symbol selected")
        return None

    ticker = symbol + ".NS"

    print("-" * 60)
    print("Selected NSE Symbol:", symbol)
    print("Yahoo Finance Ticker:", ticker)
    print("-" * 60)

    return ticker

def fetch_stock_data(ticker):
    end_date = datetime.today()
    start_date = end_date - relativedelta(years=5)

    print("Ticker:", ticker)
    print("Start Date:", start_date.date())
    print("End Date:", end_date.date())

    data = yf.download(
        ticker,
        start=start_date,
        end=end_date,
        interval="1d",
        auto_adjust=False,
        progress=False
    )

    if data.empty:
        print("No stock data found for:", ticker)
        return None

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data = data.reset_index()

    data.to_csv("stock_data.csv", index=False)

    print("Raw stock data saved to stock_data.csv")

    return data

def clean_stock_data(data):
    df = data.copy()

    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )

    numeric_columns = [
        "Open",
        "High",
        "Low",
        "Close",
        "Adj Close",
        "Volume"
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    df = df.dropna().reset_index(drop=True)

    duplicate_count = df["Date"].duplicated().sum()

    print("Duplicate dates:", duplicate_count)

    if duplicate_count > 0:
        df = df.drop_duplicates(
            subset=["Date"],
            keep="first"
        ).reset_index(drop=True)

    df = df.sort_values("Date").reset_index(drop=True)

    df["Daily Return %"] = df["Close"].pct_change()

    print("Daily Return % column created")

    df.to_csv("clean_data.csv", index=False)

    print("Clean data saved to clean_data.csv")

    rounded_df = df.copy()

    price_columns = [
        "Open",
        "High",
        "Low",
        "Close",
        "Adj Close"
    ]

    rounded_df[price_columns] = rounded_df[price_columns].round(2)
    rounded_df["Daily Return %"] = rounded_df["Daily Return %"].round(6)

    rounded_df.to_csv(
        "cleaned_rounded.csv",
        index=False
    )

    print("Rounded clean data saved to cleaned_rounded.csv")

    return df

print("\n" + "=" * 70)
print("STARTING STOCK DATA PROCESS")
print("=" * 70)

ticker = get_selected_symbol()

if ticker:
    raw_data = fetch_stock_data(ticker)

    if raw_data is not None:
        df = clean_stock_data(raw_data)

        print("Cleaned data shape:", df.shape)

        print("\nFirst 5 rows:")
        print(df.head())

        print("\nDaily Return sample:")
        print(
            df[
                [
                    "Date",
                    "Close",
                    "Daily Return %"
                ]
            ].head(10)
        )

        print("\n" + "=" * 70)
        print("STOCK DATA PROCESS COMPLETED")
        print("=" * 70)
    else:
        print("\nStock data could not be fetched.")
else:
    print("Could not determine stock ticker.")

print("=" * 70)
