import streamlit as st
from credit_risk_model import expected_loss

st.set_page_config(
    page_title="JPMorgan Task 3",
    page_icon="💳",
    layout="wide"
)

st.title("💳 Credit Risk Analysis")

st.write(
    """
Predict the **Probability of Default (PD)** and
**Expected Loss** for a loan applicant.
"""
)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:

    credit_lines = st.number_input(
        "Credit Lines Outstanding",
        min_value=0,
        value=2
    )

    loan_amount = st.number_input(
        "Loan Amount Outstanding ($)",
        min_value=0.0,
        value=5000.0
    )

    total_debt = st.number_input(
        "Total Debt Outstanding ($)",
        min_value=0.0,
        value=12000.0
    )

with col2:

    income = st.number_input(
        "Annual Income ($)",
        min_value=0.0,
        value=60000.0
    )

    years = st.number_input(
        "Years Employed",
        min_value=0,
        value=5
    )

    fico = st.number_input(
        "FICO Score",
        min_value=300,
        max_value=850,
        value=700
    )

st.markdown("---")

if st.button("Predict Credit Risk"):

    probability, loss = expected_loss(
        credit_lines,
        loan_amount,
        total_debt,
        income,
        years,
        fico
    )

    col1, col2 = st.columns(2)

    col1.metric(
        "Probability of Default",
        f"{probability:.2%}"
    )

    col2.metric(
        "Expected Loss",
        f"${loss:,.2f}"
    )

    st.markdown("---")

    if probability < 0.20:
        st.success("🟢 Low Risk")

    elif probability < 0.50:
        st.warning("🟡 Medium Risk")

    else:
        st.error("🔴 High Risk")
