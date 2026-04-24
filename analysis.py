import numpy as np
import pandas as pd


def run_analysis(df):

    df = df.copy()

    # safety fixes
    df["open"] = df["open"].replace(0, df["ltp"])

    # returns
    df["return_pct"] = ((df["ltp"] - df["open"]) / df["open"]) * 100

    # liquidity
    df["turnover_m"] = df["turnover"] / 1_000_000

    df["amihud"] = np.where(
        df["turnover_m"] > 0,
        abs(df["return_pct"]) / df["turnover_m"],
        999
    )

    # momentum
    df["momentum"] = df["ltp"] - df["open"]

    # trend score
    df["trend_strength"] = (
        df["return_pct"] * 0.5 +
        df["momentum"] * 0.3 -
        df["amihud"] * 0.2
    )

    # clustering (rule-based)
    df["cluster"] = "Retail"

    df.loc[
        (df["turnover"] > df["turnover"].quantile(0.80)) &
        (df["amihud"] < df["amihud"].quantile(0.35)),
        "cluster"
    ] = "Institutional"

    df.loc[
        df["return_pct"].abs() > df["return_pct"].quantile(0.85),
        "cluster"
    ] = "Speculative"

    return df
