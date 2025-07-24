# src/engine/risk_manager.py

class RiskManager:
    def __init__(self, risk_per_trade: float = 1.0):
        """
        risk_per_trade: percentage of equity to risk per trade (e.g. 1.0 for 1%)
        """
        self.risk_pct = risk_per_trade

    def calculate_quantity(self, equity: float, stop_distance: float, price: float) -> float:
        """
        Given current equity, stop-loss distance (in price units), and entry price,
        return the quantity size based on risk_pct.
        """
        dollar_risk = equity * (self.risk_pct / 100.0)
        qty = dollar_risk / (stop_distance * price)
        return qty
