def generate_signals(df):

    df = df.copy()

    signals = []
    confidence = []
    advice = []
    target = []
    stoploss = []

    for _, r in df.iterrows():

        score = r["trend_strength"]

        sig = "HOLD"
        conf = 40
        msg = "No setup"
        tgt = r["ltp"]
        sl = r["ltp"] * 0.95

        # BUY condition
        if r["cluster"] == "Institutional" and score > 10:

            sig = "SWING BUY"
            conf = min(95, 60 + score * 2)

            tgt = r["ltp"] * 1.08
            sl = r["ltp"] * 0.94

            msg = "🔥 Institutional accumulation + momentum breakout"

        # EXIT condition
        elif r["cluster"] == "Institutional" and score < -5:

            sig = "EXIT"
            conf = min(90, 60 + abs(score) * 2)

            tgt = r["ltp"] * 0.93
            sl = r["ltp"] * 1.03

            msg = "⚠️ Distribution detected"

        # speculative filter
        elif r["cluster"] == "Speculative":
            sig = "NO TRADE"
            conf = 50
            msg = "High volatility zone"

        signals.append(sig)
        confidence.append(round(conf, 2))
        advice.append(msg)
        target.append(round(tgt, 2))
        stoploss.append(round(sl, 2))

    df["Signal"] = signals
    df["Confidence"] = confidence
    df["Advice"] = advice
    df["Target"] = target
    df["StopLoss"] = stoploss

    return df
