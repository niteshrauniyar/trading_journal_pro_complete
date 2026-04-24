import numpy as np
import pandas as pd


def run_analysis(df):

    df = df.copy()

    df["return_pct"] = ((df["ltp"] - df["open"]) / df["open"]) * 100
    df["turnover_m"] = df["turnover"] / 1_000_000

    df["amihud"] = np.where(
        df["turnover_m"] > 0,
        abs(df["return_pct"]) / df["turnover_m"],
        999
    )

    # Smart Money detection (quantile-based)
    turnover_cut = df["turnover"].quantile(0.80)
    amihud_low = df["amihud"].quantile(0.30)

    df["cluster_name"] = "Retail"

    df.loc[
        (df["turnover"] >= turnover_cut) &
        (df["amihud"] <= amihud_low),
        "cluster_name"
    ] = "Institutional"

    df.loc[
        df["return_pct"].abs() > df["return_pct"].quantile(0.85),
        "cluster_name"
    ] = "Speculative"

    return df
