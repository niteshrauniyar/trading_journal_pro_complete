import streamlit as st
import pandas as pd

from data_fetcher import NEPSEFetcher
from analysis import run_analysis
from signals import generate_signals


st.set_page_config(layout="wide", page_title="Swing Engine V2")

st.title("📈 NEPSE Swing Trading Engine V2")

st.caption("Stable swing system (demo + manual + analysis)")

# session state
if "manual_df" not in st.session_state:
    st.session_state.manual_df = None

# -----------------------------
# MANUAL INPUT
# -----------------------------
st.subheader("✍️ Manual Input (Optional Override)")

with st.form("manual_form"):

    symbol = st.text_input("Symbol", "NABIL")
    ltp = st.number_input("LTP", value=0.0)
    open_price = st.number_input("Open", value=0.0)
    volume = st.number_input("Volume", value=0.0)
    turnover = st.number_input("Turnover", value=0.0)

    submit = st.form_submit_button("Add Manual Data")

    if submit:
        st.session_state.manual_df = pd.DataFrame([{
            "symbol": symbol,
            "ltp": ltp,
            "open": open_price,
            "volume": volume,
            "turnover": turnover
        }])

# -----------------------------
# FETCH DATA
# -----------------------------
fetcher = NEPSEFetcher()
live_df = fetcher.fetch()

# PRIORITY LOGIC
if st.session_state.manual_df is not None and not st.session_state.manual_df.empty:
    df = st.session_state.manual_df
else:
    df = live_df

# -----------------------------
# ANALYSIS
# -----------------------------
df = run_analysis(df)
df = generate_signals(df)

# -----------------------------
# METRICS
# -----------------------------
c1, c2, c3 = st.columns(3)

c1.metric("Swing BUY", (df["Signal"] == "SWING BUY").sum())
c2.metric("EXIT", (df["Signal"] == "EXIT").sum())
c3.metric("Institutional", (df["cluster"] == "Institutional").sum())

# -----------------------------
# SIGNAL TABLE
# -----------------------------
st.subheader("📊 Swing Signals")

st.dataframe(
    df[df["Signal"].isin(["SWING BUY", "EXIT"])][
        ["symbol", "Signal", "Confidence", "Target", "StopLoss", "Advice"]
    ],
    use_container_width=True
)

# -----------------------------
# FULL DATA
# -----------------------------
st.subheader("📌 Full Market Scan")

st.dataframe(df, use_container_width=True)
