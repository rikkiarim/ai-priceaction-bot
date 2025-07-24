# src/data/market_data.py

import os
import requests

class MarketDataClient:
    """
    Simple Alpaca Data API client for fetching historical bars.
    """
    def __init__(self):
        self.base_url   = os.getenv("DATA_ENDPOINT")
        self.api_key    = os.getenv("BROKER_API_KEY")
        self.api_secret = os.getenv("BROKER_API_SECRET")
        self.headers = {
            "APCA-API-KEY-ID":     self.api_key,
            "APCA-API-SECRET-KEY": self.api_secret
        }

    def get_historical_bars(self, symbol: str, timeframe: str = "1D", limit: int = 100):
        """
        Fetches the last `limit` bars for `symbol` at `timeframe` granularity.
        Returns a list of bar dicts: { t, o, h, l, c, v }.
        """
        url = f"{self.base_url}/stocks/{symbol}/bars"
        params = {
            "timeframe": timeframe,
            "limit":     limit
        }
        resp = requests.get(url, params=params, headers=self.headers)
        resp.raise_for_status()
        return resp.json().get("bars", [])

    def get_latest_bar(self, symbol: str, timeframe: str = "1Min"):
        """
        Convenience method: fetches a single latest bar.
        """
        bars = self.get_historical_bars(symbol, timeframe, limit=1)
        return bars[0] if bars else None
