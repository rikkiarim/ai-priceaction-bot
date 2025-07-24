# src/engine/trade_loop.py

from notifier.telegram import TelegramNotifier

class TradeLoop:
    def __init__(self, mode: str = "paper"):
        self.mode = mode
        self.notifier = TelegramNotifier()

    def run(self):
        # This is where your main trading loop will go.
        msg = f"🚀 TradeLoop started in *{self.mode.upper()}* mode"
        self.notifier.send(msg)
        print(msg)
        # TODO: Replace with your real loop logic:
        #   - load market data
        #   - identify setups
        #   - call TradeExecutor.enter_trade / exit_trade
        #   - respect session hours, risk limits, etc.
