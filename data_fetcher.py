import pandas as pd
import random
import os
import json


class NEPSEFetcher:

    CACHE_FILE = "nepse_cache.json"

    # -------------------------
    # SAFE DEMO DATA (ALWAYS WORKS)
    # -------------------------
    def demo_data(self):

        symbols = [
            "NABIL", "GBIME", "NICA", "SCB", "HBL",
            "NIFRA", "UPPER", "SHIVM", "API", "NRIC"
        ]

        rows = []

        for s in symbols:

            base = random.randint(200, 1200)

            ltp = base + random.randint(-20, 20)
            open_price = base + random.randint(-15, 15)

            volume = random.randint(50000, 800000)
            turnover = volume * ltp

            rows.append({
                "symbol": s,
                "ltp": ltp,
                "open": open_price,
                "volume": volume,
                "turnover": turnover
            })

        return pd.DataFrame(rows)

    # -------------------------
    # LOAD CACHE
    # -------------------------
    def load_cache(self):

        if os.path.exists(self.CACHE_FILE):
            with open(self.CACHE_FILE, "r") as f:
                return pd.DataFrame(json.load(f))

        return None

    # -------------------------
    # SAVE CACHE
    # -------------------------
    def save_cache(self, df):

        try:
            with open(self.CACHE_FILE, "w") as f:
                json.dump(df.to_dict(orient="records"), f)
        except:
            pass

    # -------------------------
    # MAIN FETCH (NEVER FAILS)
    # -------------------------
    def fetch(self):

        df = None

        # 1. Try live (optional)
        try:
            df = self.try_live()
        except:
            df = None

        # 2. Try cache
        if df is None or len(df) == 0:
            df = self.load_cache()

        # 3. FINAL FALLBACK → DEMO DATA
        if df is None or len(df) == 0:
            df = self.demo_data()

        # Save latest usable dataset
        self.save_cache(df)

        return df

    # -------------------------
    # OPTIONAL LIVE PLACEHOLDER
    # -------------------------
    def try_live(self):
        """
        Keep empty or plug real API later.
        Must NOT crash system.
        """
        raise Exception("Live API disabled (unstable)")
