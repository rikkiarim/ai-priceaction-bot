# src/engine/trade_loop.py

import os
from dotenv import load_dotenv

from notifier.telegram import TelegramNotifier
from engine.executor      import TradeExecutor
from engine.broker        import AlpacaBrokerClient
from engine.risk_manager  import RiskManager

from data.market_data     import MarketDataClient
from data.trend           import detect_trend


def main_loop_demo():
    """
    Demonstration of the trading loop with trend analysis and a sample entry/exit flow.
    """
    # Load environment variables
    load_dotenv()

    # Instantiate services
    notifier      = TelegramNotifier()
    data_client   = MarketDataClient()
    broker_client = AlpacaBrokerClient(
        endpoint=os.getenv("BROKER_ENDPOINT"),
        api_key=os.getenv("BROKER_API_KEY"),
        api_secret=os.getenv("BROKER_API_SECRET"),
        mode="paper"
    )
    risk_manager  = RiskManager(risk_per_trade=float(os.getenv("RISK_PER_TRADE", 1)))
    executor      = TradeExecutor(broker_client, risk_manager)

    # 1) Startup notification
    mode = "PAPER"
    start_msg = f"🚀 TradeLoop started in *{mode}* mode"
    notifier.send(start_msg)
    print(start_msg)

    # 2) Fetch bars and detect trend
    symbol   = "AAPL"
    lookback = 5
    bars     = data_client.get_historical_bars(symbol, timeframe="1Min", limit=lookback)
    trend    = detect_trend(bars, lookback=lookback)

    # 3) Guard against insufficient data
    if trend == "range" and len(bars) < lookback:
        warn = (f"⚠️ Not enough data to detect trend for {symbol} "
                f"(have {len(bars)}/{lookback} bars). Skipping trades.")
        notifier.send(warn)
        print(warn)
        return

    # 4) Report detected trend
    info = f"📈 Market trend for {symbol} over last {lookback} bars: *{trend}*"
    notifier.send(info)
    print(info)

    # 5) Sample entry trade
    entry_price = bars[-1]["c"]  # use last bar's close for demo price
    qty = 1
    entry = executor.enter_trade(symbol, "BUY", qty, entry_price)
    print(f"[TradeLoop] Entry order response: {entry}")

    # 6) Sample exit trade
    exit_price = entry_price + 1  # demo a $1 move
    pnl = (exit_price - entry_price) * qty
    exit = executor.exit_trade(symbol, "SELL", qty, exit_price, pnl)
    print(f"[TradeLoop] Exit order response: {exit}")

    # 7) Completion notification
    done_msg = "✅ TradeLoop demo complete"
    notifier.send(done_msg)
    print(done_msg)


if __name__ == "__main__":
    main_loop_demo()
