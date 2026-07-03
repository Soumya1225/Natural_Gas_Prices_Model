import pandas as pd
from scipy.interpolate import interp1d

# Load historical gas prices
df = pd.read_csv("data/gas_prices.csv")

# Convert dates
df["Dates"] = pd.to_datetime(df["Dates"])

# Sort data
df = df.sort_values("Dates")

# Convert dates into numeric values
df["Days"] = (df["Dates"] - df["Dates"].min()).dt.days

# Create interpolation model
price_function = interp1d(
    df["Days"],
    df["Prices"],
    kind="linear",
    fill_value="extrapolate"
)

# Estimate gas price for any date
def get_price(date):
    date = pd.to_datetime(date)
    days = (date - df["Dates"].min()).days
    return float(price_function(days))


# Price storage contract
def price_contract(
    injection_date,
    withdrawal_date,
    volume,
    injection_rate,
    withdrawal_rate,
    max_volume,
    storage_cost_per_day
):

    # Respect storage capacity
    stored_volume = min(volume, max_volume)

    # Injection/withdrawal rates (simplified)
    injected_volume = min(stored_volume, injection_rate)
    withdrawn_volume = min(injected_volume, withdrawal_rate)

    # Market prices
    buy_price = get_price(injection_date)
    sell_price = get_price(withdrawal_date)

    # Storage duration
    storage_days = (
        pd.to_datetime(withdrawal_date)
        - pd.to_datetime(injection_date)
    ).days

    # Storage cost
    storage_cost = storage_days * storage_cost_per_day

    # Contract value
    contract_value = (
        (sell_price - buy_price) * withdrawn_volume
        - storage_cost
    )

    return round(contract_value, 2)
