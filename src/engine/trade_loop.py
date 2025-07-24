# src/engine/trade_loop.py
import os
from dotenv import load_dotenv
from notifier.telegram import TelegramNotifier
from engine.executor         import TradeExecutor
from engine.broker           import AlpacaBrokerClient
from engine.risk_manager     import RiskManager

from dotenv import load_dotenv
from notifier.telegram import TelegramNotifier
from engine.executor import TradeExecutor
# (You’ll swap these stubs for real implementations later)
from engine.broker import AlpacaBrokerClient
from engine.risk_manager import RiskManager

class TradeLoop:
    def __init__(self, mode: str = "paper"):
        load_dotenv()  # ensure .env is loaded here too, if not already
        self.mode = mode.upper()
        self.notifier = TelegramNotifier()

        # 1) Instantiate your broker client & risk manager
        self.broker_client = AlpacaBrokerClient(endpoint=os.getenv("BROKER_ENDPOINT"),
                                                api_key=os.getenv("BROKER_API_KEY"),
                                                api_secret=os.getenv("BROKER_API_SECRET"),
                                                mode=mode)
        self.risk_manager = RiskManager(risk_per_trade=float(os.getenv("RISK_PER_TRADE")))

        # 2) Wire up the TradeExecutor
        self.executor = TradeExecutor(self.broker_client, self.risk_manager)

    def run(self):
        # Startup notification
        start_msg = f"🚀 TradeLoop started in *{self.mode}* mode"
        self.notifier.send(start_msg)
        print(start_msg)

        # TODO: Replace this stub with real market-data loop
        # Example demonstration of entry/exit flow:
        symbol = "EURUSD"
        side = "BUY"
        qty = 1000
        price = 1.12345

        # 3) Execute an entry trade
        entry = self.executor.enter_trade(symbol, side, qty, price)
        print(f"[TradeLoop] Entry order response: {entry}")

        # 4) (In practice you'd wait for your exit signal...) simulate exit:
        exit_price = 1.12500
        pnl = (exit_price - price) * qty  # simplistic P/L calc
        exit = self.executor.exit_trade(symbol, "SELL", qty, exit_price, pnl)
        print(f"[TradeLoop] Exit order response: {exit}")

        # End of stub
        done_msg = "✅ TradeLoop demo complete"
        self.notifier.send(done_msg)
        print(done_msg)
