import streamlit as st
from fico_bucket_model import create_rating_map

st.set_page_config(
    page_title="Task 4 - FICO Bucketing",
    page_icon="📊",
    layout="wide"
)

st.title("📊 FICO Score Bucketing")

st.write("""
Generate rating buckets based on borrower FICO scores.
A lower rating indicates a better credit profile.
""")

num_buckets = st.slider(
    "Number of Buckets",
    2,
    20,
    10
)

if st.button("Generate Rating Map"):

    result = create_rating_map(num_buckets)

    st.subheader("Rating Map")

    st.dataframe(
        result,
        use_container_width=True,
        hide_index=True
    )

    st.bar_chart(
        result.set_index("Rating")["PD"]
    )
