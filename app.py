# =========================
# File 4: app.py
# =========================
import streamlit as st
import pandas as pd
from data_fetcher import ChukulFetcher
from analysis import run_analysis
from signals import generate_signals


st.set_page_config(
    page_title="NEPSE Institutional Quant App",
    layout="wide"
)

# -----------------------
# Dark Theme CSS
# -----------------------
st.markdown("""
<style>
body, .stApp {
    background-color:#0e1117;
    color:white;
}
[data-testid="metric-container"]{
    background:#161b22;
    border:1px solid #2f3542;
    padding:15px;
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

# Session Safety
if "df" not in st.session_state:
    st.session_state["df"] = pd.DataFrame()

st.title("📈 Institutional Quant App - NEPSE")
st.caption("Powered by Chukul Data Source")

# Formula
st.latex(r'''
Amihud = \frac{|Return\%|}{Turnover\ in\ Millions}
''')

# -----------------------
# Fetch Button
# -----------------------
if st.button("🔄 Refresh Market Data"):

    try:
        fetcher = ChukulFetcher()
        raw_df = fetcher.fetch()

        df = run_analysis(raw_df)
        df = generate_signals(df)

        st.session_state["df"] = df

    except Exception as e:
        st.warning(f"Unable to connect to Chukul API. {e}")

df = st.session_state["df"]

# -----------------------
# If data exists
# -----------------------
if not df.empty:

    col1, col2, col3 = st.columns(3)

    buys = (df["Signal"] == "STRONG BUY").sum()
    sells = (df["Signal"] == "EXIT").sum()
    institutional = (df["cluster_name"] == "Institutional").sum()

    col1.metric("📊 Buy Signals", buys)
    col2.metric("🚪 Exit Signals", sells)
    col3.metric("🏦 Institutional Stocks", institutional)

    st.divider()

    # -----------------------
    # Signal Table
    # -----------------------
    st.subheader("🚀 Trade Signals")

    signal_df = df[df["Signal"].isin(["STRONG BUY", "EXIT"])]

    show_cols = [
        "symbol", "Signal", "Confidence %",
        "ltp", "Target", "StopLoss",
        "SimpleAdvice"
    ]

    show_cols = [c for c in show_cols if c in signal_df.columns]

    st.dataframe(
        signal_df[show_cols],
        use_container_width=True,
        height=350
    )

    st.divider()

    # -----------------------
    # Full Data Matrix
    # -----------------------
    st.subheader("📌 Full Quant Matrix")

    def highlight_rows(row):
        if row["cluster_name"] == "Institutional":
            return ['background-color:#123524'] * len(row)
        return [''] * len(row)

    st.dataframe(
        df.style.apply(highlight_rows, axis=1),
        use_container_width=True,
        height=600
    )

else:
    st.info("Click Refresh Market Data to load live NEPSE data.")
