import pandas as pd
from nepse_data_api import Nepse

class ChukulFetcher:
    def fetch(self):
        try:
            nepse = Nepse()
            stocks = nepse.get_stocks()

            rows = []
            for s in stocks:
                rows.append({
                    "symbol": s.get("symbol", ""),
                    "ltp": float(s.get("lastTradedPrice", 0)),
                    "open": float(s.get("openPrice", 0)),
                    "volume": float(s.get("totalTradedQuantity", 0)),
                    "turnover": float(s.get("totalTradedValue", 0)),
                })

            df = pd.DataFrame(rows)
            df = df[(df["ltp"] > 0) & (df["volume"] > 0)]
            return df

        except Exception as e:
            raise Exception(f"NEPSE fetch failed: {e}")
