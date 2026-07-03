import streamlit as st
import pandas as pd
from database_functions import get_history

st.title("📜 Prediction History")

df = get_history()

if df.empty:
    st.warning("No predictions found yet.")
else:
    st.dataframe(df)

    st.markdown("---")

    # Filters
    status_filter = st.selectbox(
        "Filter Result",
        ["All", "Placed", "Not Placed"]
    )

    if status_filter != "All":
        df = df[df["prediction"] == status_filter]

    st.subheader("Filtered Data")
    st.dataframe(df)

    # Download button
    csv = df.to_csv(index=False).encode('utf-8')

    st.download_button(
        "📥 Download CSV",
        csv,
        "prediction_history.csv",
        "text/csv"
    )