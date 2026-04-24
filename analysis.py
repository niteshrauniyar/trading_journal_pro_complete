# =========================
# File 2: analysis.py
# =========================
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def run_analysis(df):
    df = df.copy()

    # Return %
    df["return_pct"] = ((df["ltp"] - df["open"]) / df["open"]) * 100

    # Turnover in millions
    df["turnover_m"] = df["turnover"] / 1_000_000

    # Amihud Illiquidity Ratio
    df["amihud"] = np.where(
        df["turnover_m"] > 0,
        abs(df["return_pct"]) / df["turnover_m"],
        999
    )

    # High turnover threshold (top 20%)
    threshold = df["turnover"].quantile(0.80)

    # Prepare clustering
    features = df[["turnover", "volume", "amihud", "return_pct"]].fillna(0)

    scaler = StandardScaler()
    X = scaler.fit_transform(features)

    km = KMeans(n_clusters=3, random_state=42, n_init=10)
    df["cluster"] = km.fit_predict(X)

    # Determine which cluster is institutional:
    # highest turnover + lowest amihud
    cluster_summary = df.groupby("cluster").agg({
        "turnover": "mean",
        "amihud": "mean"
    })

    score = (
        cluster_summary["turnover"].rank(ascending=False) +
        cluster_summary["amihud"].rank(ascending=True)
    )

    institutional_cluster = score.idxmin()

    labels = {}

    for c in cluster_summary.index:
        if c == institutional_cluster:
            labels[c] = "Institutional"
        else:
            # classify others
            if cluster_summary.loc[c, "amihud"] > cluster_summary["amihud"].median():
                labels[c] = "Speculative"
            else:
                labels[c] = "Retail"

    df["cluster_name"] = df["cluster"].map(labels)

    # Institutional Activity Condition
    df["institutional_activity"] = np.where(
        (df["turnover"] >= threshold) &
        (df["cluster_name"] == "Institutional"),
        True,
        False
    )

    return df
