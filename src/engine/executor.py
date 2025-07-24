# src/engine/executor.py

from notifier.telegram import TelegramNotifier

class TradeExecutor:
    def __init__(self, broker_client, risk_manager):
        self.broker = broker_client
        self.risk = risk_manager
        self.notifier = TelegramNotifier()           # ← instantiate once

    def enter_trade(self, symbol: str, side: str, qty: float, price: float):
        # … existing order placement logic …
        order = self.broker.place_order(symbol, side, qty)
        
        # Send a Telegram alert
        msg = (
            f"🟢 *Entry* — {symbol}\n"
            f"Side: {side}\n"
            f"Qty: {qty}\n"
            f"Price: {price:.5f}"
        )
        self.notifier.send(msg)

        return order

    def exit_trade(self, symbol: str, side: str, qty: float, price: float, pnl: float):
        # … existing exit logic …
        order = self.broker.close_position(symbol)

        # Send a Telegram alert
        msg = (
            f"🔴 *Exit* — {symbol}\n"
            f"Side: {side}\n"
            f"Qty: {qty}\n"
            f"Price: {price:.5f}\n"
            f"P/L: {pnl:.2f}"
        )
        self.notifier.send(msg)

        return order
