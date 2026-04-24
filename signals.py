import numpy as np


def generate_signals(df):

    df = df.copy()

    signals = []
    confidence = []
    advice = []
    target = []
    stoploss = []

    for _, r in df.iterrows():

        sig = "HOLD"
        conf = 40
        msg = "No clear setup"
        tgt = r["ltp"]
        sl = r["ltp"] * 0.97

        if r["cluster_name"] == "Institutional":

            if r["ltp"] > r["open"]:
                sig = "STRONG BUY"
                conf = 75 + min(r["return_pct"] * 2, 20)
                tgt = r["ltp"] * 1.06
                sl = r["ltp"] * 0.95
                msg = "🔥 Smart Money Accumulation Detected"

            elif r["ltp"] < r["open"]:
                sig = "EXIT"
                conf = 70 + min(abs(r["return_pct"]) * 2, 20)
                tgt = r["ltp"] * 0.94
                sl = r["ltp"] * 1.03
                msg = "⚠️ Distribution Phase Detected"

        signals.append(sig)
        confidence.append(round(conf, 2))
        advice.append(msg)
        target.append(round(tgt, 2))
        stoploss.append(round(sl, 2))

    df["Signal"] = signals
    df["Confidence %"] = confidence
    df["Advice"] = advice
    df["Target"] = target
    df["StopLoss"] = stoploss

    return df
