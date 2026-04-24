# =========================
# File 1: data_fetcher.py
# =========================
import requests
import pandas as pd
import numpy as np


class ChukulFetcher:
    """
    Fast NEPSE data connector using Chukul internal API.
    """

    URL = "https://chukul.com/api/market-data/today-price"

    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0 Safari/537.36"
        ),
        "Referer": "https://chukul.com/nepse-charts"
    }

    def __init__(self):
        self.df = pd.DataFrame()

    def _safe_float(self, x):
        try:
            if x in ["", None, "-", "null"]:
                return 0.0
            return float(str(x).replace(",", "").strip())
        except:
            return 0.0

    def fetch(self):
        try:
            r = requests.get(self.URL, headers=self.HEADERS, timeout=15)
            r.raise_for_status()
            data = r.json()

            rows = []

            for row in data:
                rows.append({
                    "symbol": row.get("symbol", ""),
                    "ltp": self._safe_float(row.get("ltp")),
                    "open": self._safe_float(row.get("open")),
                    "volume": self._safe_float(row.get("vol")),
                    "turnover": self._safe_float(row.get("turnover")),
                })

            df = pd.DataFrame(rows)

            # Pre-cleaning
            df = df[(df["ltp"] > 0) & (df["volume"] > 0)].copy()

            return df.reset_index(drop=True)

        except Exception as e:
            raise RuntimeError(f"API Error: {e}")
