import requests
import pandas as pd

class ChukulFetcher:

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://chukul.com/nepse-charts"
        }

        self.urls = [
            "https://chukul.com/api/market-data/today-price",
            "https://chukul.com/api/market-data/live",
            "https://chukul.com/api/nepse/today-price",
            "https://chukul.com/api/today-price"
        ]

    def safe_float(self, x):
        try:
            return float(str(x).replace(",", ""))
        except:
            return 0.0

    def fetch(self):

        for url in self.urls:
            try:
                r = requests.get(url, headers=self.headers, timeout=10)

                if r.status_code == 200:
                    data = r.json()

                    rows = []

                    for row in data:
                        rows.append({
                            "symbol": row.get("symbol", ""),
                            "ltp": self.safe_float(row.get("ltp")),
                            "open": self.safe_float(row.get("open")),
                            "volume": self.safe_float(row.get("vol")),
                            "turnover": self.safe_float(row.get("turnover"))
                        })

                    df = pd.DataFrame(rows)

                    df = df[(df["ltp"] > 0) & (df["volume"] > 0)]

                    return df

            except:
                continue

        raise Exception("All Chukul endpoints failed.")
