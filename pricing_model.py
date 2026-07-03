import pandas as pd
from scipy.interpolate import interp1d

# Load CSV
df = pd.read_csv("data/gas_prices.csv")

df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

df["Days"] = (df["Date"] - df["Date"].min()).dt.days

price_function = interp1d(
    df["Days"],
    df["Prices"],
    kind="linear",
    fill_value="extrapolate"
)


def get_price(date):

    date = pd.to_datetime(date)

    days = (date - df["Date"].min()).days

    return float(price_function(days))


def price_contract(
        injection_date,
        withdrawal_date,
        volume,
        storage_cost_per_day):

    buy_price = get_price(injection_date)

    sell_price = get_price(withdrawal_date)

    storage_days = (
        pd.to_datetime(withdrawal_date)
        -
        pd.to_datetime(injection_date)
    ).days

    storage_cost = storage_days * storage_cost_per_day

    value = (
        (sell_price - buy_price)
        * volume
        - storage_cost
    )

    return round(value,2)
