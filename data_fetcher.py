import pandas as pd
import random


class NEPSEFetcher:

    def fetch(self):

        symbols = ["NABIL", "GBIME", "NICA", "SCB", "HBL", "NIFRA"]

        rows = []

        for s in symbols:

            base = random.randint(200, 1200)

            ltp = base + random.randint(-25, 25)
            open_price = base + random.randint(-40, 40)

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
