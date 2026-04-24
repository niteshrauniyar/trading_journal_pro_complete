# =========================
# File 3: signals.py
# =========================
import numpy as np
import pandas as pd


def generate_signals(df):
    df = df.copy()

    signal = []
    confidence = []
    advice = []
    target = []
    stoploss = []

    for _, row in df.iterrows():

        sig = "HOLD"
        conf = 45
        msg = "Wait for better setup."
        tgt = row["ltp"]
        sl = row["ltp"] * 0.97

        if row["cluster_name"] == "Institutional":

            if row["ltp"] > row["open"]:
                sig = "STRONG BUY"
                conf = min(95, 70 + row["return_pct"] * 3)
                tgt = row["ltp"] * 1.05
                sl = row["ltp"] * 0.96
                msg = f"🔥 Smart Money is absorbing supply. Target Rs. {tgt:.2f}"

            elif row["ltp"] < row["open"]:
                sig = "EXIT"
                conf = min(90, 65 + abs(row["return_pct"]) * 2)
                tgt = row["ltp"] * 0.95
                sl = row["ltp"] * 1.03
                msg = f"⚠️ Institutions distributing stock. Protect capital."

        signal.append(sig)
        confidence.append(round(conf, 1))
        advice.append(msg)
        target.append(round(tgt, 2))
        stoploss.append(round(sl, 2))

    df["Signal"] = signal
    df["Confidence %"] = confidence
    df["SimpleAdvice"] = advice
    df["Target"] = target
    df["StopLoss"] = stoploss

    return df
