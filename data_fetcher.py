import pandas as pd
import numpy as np
import random


class NEPSEFetcher:

    def fetch(self):

        # -----------------------------
        # SIMULATED EOD MARKET DATA
        # (Replace later with real feed)
        # -----------------------------

        symbols = [
            "NABIL", "GBIME", "NICA", "SCB", "HBL",
            "NIFRA", "UPPER", "SHIVM", "API", "NRIC"
        ]

        rows = []

        for s in symbols:

            base = random.randint(200, 1200)

            open_price = base + random.randint(-15, 15)
            ltp = base + random.randint(-25, 25)

            volume = random.randint(50000, 800000)
            turnover = volume * ltp

            rows.append({
                "symbol": s,
                "open": open_price,
                "ltp": ltp,
                "volume": volume,
                "turnover": turnover
            })

        return pd.DataFrame(rows)
