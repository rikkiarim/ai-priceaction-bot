# src/engine/broker.py

import os
import requests

class AlpacaBrokerClient:
    def __init__(self, endpoint: str, api_key: str, api_secret: str, mode: str = "paper"):
        self.endpoint   = endpoint
        self.api_key    = api_key
        self.api_secret = api_secret
        self.mode       = mode.lower()

        # Example headers for Alpaca
        self.headers = {
            "APCA-API-KEY-ID":     self.api_key,
            "APCA-API-SECRET-KEY": self.api_secret,
            "Content-Type":        "application/json"
        }

    def place_order(self, symbol: str, side: str, qty: float):
        """
        Place a market order.
        """
        url = f"{self.endpoint}/orders"
        payload = {
            "symbol": symbol,
            "qty":    qty,
            "side":   side.lower(),
            "type":   "market",
            "time_in_force": "day"
        }
        resp = requests.post(url, json=payload, headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def close_position(self, symbol: str):
        """
        Close an open position on `symbol`.
        """
        url = f"{self.endpoint}/positions/{symbol}"
        resp = requests.delete(url, headers=self.headers)
        resp.raise_for_status()
        return resp.json()
