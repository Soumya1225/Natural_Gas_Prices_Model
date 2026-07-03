import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from datetime import timedelta
from pricing_model import price_contract
import warnings

warnings.filterwarnings("ignore")

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="Natural Gas Price Model",
    page_icon="⛽",
    layout="wide"
)

# ---------------- SIDEBAR ---------------- #
page = st.sidebar.selectbox(
    "Choose Task",
    [
        "Task 1 - Price Forecast",
        "Task 2 - Storage Contract Pricing"
    ]
)

# ===========================================================
# ====================== TASK 2 =============================
# ===========================================================

if page == "Task 2 - Storage Contract Pricing":

    st.title("⛽ Natural Gas Storage Contract Pricing")
    st.write("JPMorgan Chase & Co. - Quantitative Research (Forage Task 2)")

    st.markdown("---")

    injection_date = st.date_input("Injection Date")

    withdrawal_date = st.date_input("Withdrawal Date")

    st.markdown("### Contract Parameters")

    volume = st.number_input(
        "Gas Volume",
        min_value=1.0,
        value=100000.0
    )

    injection_rate = st.number_input(
        "Injection Rate (Units/Day)",
        min_value=1.0,
        value=50000.0
    )

    withdrawal_rate = st.number_input(
        "Withdrawal Rate (Units/Day)",
        min_value=1.0,
        value=50000.0
    )

    max_volume = st.number_input(
        "Maximum Storage Capacity",
        min_value=1.0,
        value=150000.0
    )

    storage_cost = st.number_input(
        "Storage Cost Per Day",
        min_value=0.0,
        value=20.0
    )

    st.markdown("---")

    if st.button("Calculate Contract Value"):

        contract_value = price_contract(
            str(injection_date),
            str(withdrawal_date),
            volume,
            injection_rate,
            withdrawal_rate,
            max_volume,
            storage_cost
        )

        st.success(
            f"Estimated Contract Value: ${contract_value:,.2f}"
        )

    st.stop()

# ===========================================================
# ====================== TASK 1 =============================
# ===========================================================

st.title("📈 JPMorgan Task 1: Natural Gas Price Analysis")

st.write(
    "Holt-Winters model with 12-month seasonality to forecast future prices."
)


@st.cache_data
def load_and_train():

    path = "data/gas_prices.csv"

    df = pd.read_csv(path)

    df = df.rename(
        columns={
            "Dates": "Date",
            "Prices": "Price"
        }
    )

    df["Date"] = pd.to_datetime(
        df["Date"],
        format="%m/%d/%y"
    )

    df["Price"] = pd.to_numeric(
        df["Price"],
        errors="coerce"
    )

    df = df.dropna()

    df = df.sort_values("Date")

    df = df.set_index("Date").asfreq("ME")

    df["Price"] = df["Price"].interpolate()

    model = ExponentialSmoothing(
        df["Price"],
        trend="add",
        seasonal="add",
        seasonal_periods=12
    ).fit(optimized=True)

    return df, model


try:

    df, model = load_and_train()

except FileNotFoundError:

    st.error(
        "data/gas_prices.csv not found."
    )

    st.stop()

except Exception as e:

    st.error(str(e))

    st.stop()

st.sidebar.header("Forecast Settings")

months_ahead = st.sidebar.slider(
    "Months to Forecast",
    1,
    24,
    12
)

forecast = model.forecast(months_ahead)

last_date = df.index[-1]

future_dates = pd.date_range(
    start=last_date + timedelta(days=1),
    periods=months_ahead,
    freq="ME"
)

forecast_df = pd.DataFrame(
    {
        "Date": future_dates,
        "Forecast": forecast.values
    }
)

fig, ax = plt.subplots(figsize=(11, 5))

ax.plot(
    df.index,
    df["Price"],
    label="Historical Price",
    linewidth=2
)

ax.plot(
    forecast_df["Date"],
    forecast_df["Forecast"],
    "--",
    linewidth=2,
    label="Forecast"
)

ax.set_xlabel("Date")

ax.set_ylabel("Price")

ax.set_title("Natural Gas Price Forecast")

ax.grid(alpha=0.3)

ax.legend()

st.pyplot(fig)

st.subheader(f"Forecast for Next {months_ahead} Months")

forecast_df["Date"] = forecast_df["Date"].dt.strftime("%b %Y")

forecast_df["Forecast"] = forecast_df["Forecast"].round(2)

st.dataframe(
    forecast_df,
    use_container_width=True,
    hide_index=True
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Last Actual Price",
    f"${df['Price'].iloc[-1]:.2f}"
)

col2.metric(
    "Final Forecast",
    f"${forecast.iloc[-1]:.2f}"
)

col3.metric(
    "Average Forecast",
    f"${forecast.mean():.2f}"
)

st.caption(
    "Model: Holt-Winters Exponential Smoothing with 12-month seasonality"
)
