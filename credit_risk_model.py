import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

# Load dataset
df = pd.read_csv("data/loan_data.csv")

# Features
X = df[
    [
        "credit_lines_outstanding",
        "loan_amt_outstanding",
        "total_debt_outstanding",
        "income",
        "years_employed",
        "fico_score",
    ]
]

# Target
y = df["default"]

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train Logistic Regression model
model = LogisticRegression(max_iter=1000)
model.fit(X_scaled, y)


def predict_default_probability(
    credit_lines_outstanding,
    loan_amt_outstanding,
    total_debt_outstanding,
    income,
    years_employed,
    fico_score,
):
    data = pd.DataFrame(
        [[
            credit_lines_outstanding,
            loan_amt_outstanding,
            total_debt_outstanding,
            income,
            years_employed,
            fico_score,
        ]],
        columns=[
            "credit_lines_outstanding",
            "loan_amt_outstanding",
            "total_debt_outstanding",
            "income",
            "years_employed",
            "fico_score",
        ],
    )

    data_scaled = scaler.transform(data)

    pd_value = model.predict_proba(data_scaled)[0][1]

    return pd_value


def expected_loss(
    credit_lines_outstanding,
    loan_amt_outstanding,
    total_debt_outstanding,
    income,
    years_employed,
    fico_score,
):
    pd_value = predict_default_probability(
        credit_lines_outstanding,
        loan_amt_outstanding,
        total_debt_outstanding,
        income,
        years_employed,
        fico_score,
    )

    recovery_rate = 0.10
    lgd = 1 - recovery_rate

    loss = pd_value * loan_amt_outstanding * lgd

    return pd_value, loss
