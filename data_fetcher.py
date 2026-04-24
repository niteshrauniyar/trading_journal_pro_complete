import pandas as pd
from nepse_data_api import Nepse


class ChukulFetcher:

    def safe_float(self, x):
        try:
            return float(str(x).replace(",", ""))
        except:
            return 0.0

    def fetch(self):
        try:
            nepse = Nepse()

            data = nepse.get_stocks()

            rows = []

            for row in data:

                rows.append({
                    "symbol": row.get("symbol") or row.get("stockSymbol") or "",

                    "ltp": self.safe_float(
                        row.get("ltp") or
                        row.get("lastTradedPrice") or
                        row.get("closingPrice")
                    ),

                    "open": self.safe_float(
                        row.get("open") or
                        row.get("openPrice")
                    ),

                    "volume": self.safe_float(
                        row.get("volume") or
                        row.get("totalTradedQuantity") or
                        row.get("qty")
                    ),

                    "turnover": self.safe_float(
                        row.get("turnover") or
                        row.get("totalTradedValue") or
                        row.get("amount")
                    ),
                })

            df = pd.DataFrame(rows)

            df = df[(df["ltp"] > 0) & (df["volume"] > 0)]

            return df.reset_index(drop=True)

        except Exception as e:
            raise Exception(f"NEPSE fetch failed: {e}")
