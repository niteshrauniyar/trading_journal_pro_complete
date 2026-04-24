import pandas as pd
import requests
import os
import json


class NEPSEFetcher:

    CACHE_FILE = "cache.json"

    def safe_float(self, x):
        try:
            return float(str(x).replace(",", ""))
        except:
            return 0.0

    # ---------------------------
    # 1. Load cache (always works)
    # ---------------------------
    def load_cache(self):
        if os.path.exists(self.CACHE_FILE):
            with open(self.CACHE_FILE, "r") as f:
                return pd.DataFrame(json.load(f))
        return pd.DataFrame()

    # ---------------------------
    # 2. Save cache
    # ---------------------------
    def save_cache(self, df):
        with open(self.CACHE_FILE, "w") as f:
            json.dump(df.to_dict(orient="records"), f)

    # ---------------------------
    # 3. Try live source (optional)
    # ---------------------------
    def fetch_live(self):
        url = "https://nepsealpha.com/data/today-price"

        r = requests.get(url, timeout=10)

        if r.status_code != 200:
            raise Exception("Live API failed")

        data = r.json()

        if isinstance(data, dict):
            data = data.get("result", data.get("data", []))

        rows = []

        for r in data:
            rows.append({
                "symbol": r.get("symbol", ""),
                "ltp": self.safe_float(r.get("lastTradedPrice", 0)),
                "open": self.safe_float(r.get("openPrice", 0)),
                "volume": self.safe_float(r.get("totalTradedQuantity", 0)),
                "turnover": self.safe_float(r.get("totalTradedValue", 0)),
            })

        df = pd.DataFrame(rows)

        df = df[(df["ltp"] > 0) & (df["volume"] > 0)]

        return df

    # ---------------------------
    # 4. Main function (SAFE)
    # ---------------------------
    def fetch(self):

        try:
            df = self.fetch_live()

            # save cache if success
            self.save_cache(df)

            return df

        except Exception as e:
            print("Live failed:", e)

            # fallback to cache
            df = self.load_cache()

            if df.empty:
                raise Exception("No live data + no cache available")

            return df
