import streamlit as st
from data_fetcher import NEPSEFetcher
from analysis import run_analysis
from signals import generate_signals


st.set_page_config(layout="wide", page_title="Swing Trading Engine V2")

st.title("📈 NEPSE Swing Trading Engine V2")

st.caption("EOD-based institutional swing detection system")

if "df" not in st.session_state:
    st.session_state.df = None


if st.button("🔄 Run Swing Scan"):

    fetcher = NEPSEFetcher()
    df = fetcher.fetch()

    df = run_analysis(df)
    df = generate_signals(df)

    st.session_state.df = df


df = st.session_state.df

if df is not None:

    c1, c2, c3 = st.columns(3)

    c1.metric("Swing Buys", (df["Signal"] == "SWING BUY").sum())
    c2.metric("Exits", (df["Signal"] == "EXIT").sum())
    c3.metric("Institutional", (df["cluster"] == "Institutional").sum())

    st.subheader("📊 Swing Trade Signals")

    st.dataframe(
        df[df["Signal"].isin(["SWING BUY", "EXIT"])][
            ["symbol", "Signal", "Confidence", "Target", "StopLoss", "Advice"]
        ],
        use_container_width=True
    )

    st.subheader("📌 Full Market Scan")

    st.dataframe(df, use_container_width=True)

else:
    st.info("Click Run Swing Scan to generate signals")
