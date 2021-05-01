
from binance.websockets import BinanceSocketManager
import websocket, json, numpy, pandas, datetime
import config
# from algo_functions import *
from binance.client import Client
from binance.enums import *

client = Client(config.API_KEY, config.API_SECRET)
bm = BinanceSocketManager(client)

print("success")

# balance = client.get_asset_balance(asset='USDT')

# print(balance)

# quant=float(balance['free'][:8])
# print(quant)


# def buy(stream,quantity):
# 	order_successful = order(SIDE_BUY, quantity, stream)
# 	if order_successful:
# 		return True
# 	else:
# 		return False

# def sell(stream,quantity):
# 	order_successful = order(SIDE_SELL, quantity, stream)
# 	if order_successful:
# 		return True
# 	else:
# 		return False

# def order(side, quantity, symbol,order_type=ORDER_TYPE_MARKET):
#     try:
#         print("sending order")
#         order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
#         print(order)
#     except Exception as e:
#         print("an exception occured - {}".ORDER_TYPE_MARKETformat(e))
#         return False
#     return True

# order_succeeded = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)

# order = client.create_order(
#     symbol='BTCUSDT',
#     side=SIDE_SELL,
#     type=ORDER_TYPE_MARKET,
#     quantity=quant
#     )

# print(order)