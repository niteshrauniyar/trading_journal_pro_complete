import streamlit as st
from data_fetcher import NEPSEFetcher
from analysis import run_analysis
from signals import generate_signals


st.set_page_config(layout="wide", page_title="NEPSE Quant App")

st.markdown("""
<style>
body { background-color: #0e1117; color: white; }
</style>
""", unsafe_allow_html=True)

st.title("📊 NEPSE Institutional Quant Dashboard")

st.latex(r"Amihud = \frac{|Return\%|}{Turnover\ in\ Millions}")

if "df" not in st.session_state:
    st.session_state.df = None


if st.button("🔄 Load Market Data"):

    try:
        fetcher = NEPSEFetcher()
        df = fetcher.fetch()

        df = run_analysis(df)
        df = generate_signals(df)

        st.session_state.df = df

    except Exception as e:
        st.error(f"Data error: {e}")


df = st.session_state.df

if df is not None and len(df) > 0:

    c1, c2, c3 = st.columns(3)

    c1.metric("Buy Signals", (df["Signal"] == "STRONG BUY").sum())
    c2.metric("Exit Signals", (df["Signal"] == "EXIT").sum())
    c3.metric("Institutional", (df["cluster_name"] == "Institutional").sum())

    st.subheader("📌 Trade Signals")

    st.dataframe(
        df[df["Signal"].isin(["STRONG BUY", "EXIT"])][
            ["symbol", "Signal", "Confidence %", "Target", "StopLoss", "Advice"]
        ],
        use_container_width=True
    )

    st.subheader("📊 Full Market Matrix")

    st.dataframe(df, use_container_width=True)

else:
    st.info("Click Load Market Data")
