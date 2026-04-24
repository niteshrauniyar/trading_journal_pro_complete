import pandas as pd
import requests


class NEPSEFetcher:

    URLS = [
        "https://nepsealpha.com/trading/1/market",
        "https://nepsealpha.com/data/today-price"
    ]

    def safe_float(self, x):
        try:
            if x in [None, "", "-", "null"]:
                return 0.0
            return float(str(x).replace(",", ""))
        except:
            return 0.0

    def fetch(self):

        for url in self.URLS:
            try:
                r = requests.get(url, timeout=10)
                if r.status_code != 200:
                    continue

                data = r.json()

                # unwrap common API formats
                if isinstance(data, dict):
                    data = data.get("result") or data.get("data") or []

                rows = []

                for r in data:

                    rows.append({
                        "symbol": r.get("symbol", ""),

                        "ltp": self.safe_float(
                            r.get("ltp") or r.get("lastTradedPrice") or r.get("close")
                        ),

                        "open": self.safe_float(
                            r.get("open") or r.get("openPrice")
                        ),

                        "volume": self.safe_float(
                            r.get("volume") or r.get("qty") or r.get("totalTradedQuantity")
                        ),

                        "turnover": self.safe_float(
                            r.get("turnover") or r.get("totalTradedValue")
                        ),
                    })

                df = pd.DataFrame(rows)

                # enforce schema
                for col in ["symbol", "ltp", "open", "volume", "turnover"]:
                    if col not in df.columns:
                        df[col] = 0

                df = df[(df["ltp"] > 0) & (df["volume"] > 0)]

                if len(df) > 0:
                    return df.reset_index(drop=True)

            except:
                continue

        raise Exception("All data sources failed")
