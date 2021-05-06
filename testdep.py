
from binance.websockets import BinanceSocketManager
import websocket, json, numpy, pandas, datetime
import config
from algo_functions import *
from binance.client import Client
from binance.enums import *

client = Client(config.API_KEY, config.API_SECRET)
bm = BinanceSocketManager(client)


def buy(symbol,quantity):
	try:
		order = client.create_order(
		symbol=symbol,
		side=SIDE_BUY,
		type=ORDER_TYPE_MARKET,
		quantity=quantity
		)
	except Exception as e:
		print("an exception occured - {}".format(e))
		return False
	log(order)
	return True, order

def sell(symbol,quantity):
	try:
		order = client.create_order(
		    symbol=symbol,
		    side=SIDE_SELL,
		    type=ORDER_TYPE_MARKET,
		    quantity=quantity
		    )
	except Exception as e:
		print("an exception occured - {}".format(e))
		return False
	log(order)
	return True, order


def order_handler(order_info, stream):
	global portfolio, CASH
	fills=order_info['fills']
	side=order_info['side']
	log(order_info)

	for f in fills:
		if side=='SELL':
			portfolio[stream]['quantity']-=float(f['qty'])
			CASH+=float(f['price'])*float(f['qty'])
			CASH-=float(f['commission'])
			portfolio[stream]['in_position']=False
		if side=='BUY':
			portfolio[stream]['quantity']+=float(f['qty'])
			portfolio[stream]['quantity']-=float(f['commission'])
			CASH-=float(f['price'])*float(f['qty'])
			portfolio[stream]['bought_price']+=float(f['price'])*float(f['qty'])
			portfolio[stream]['in_position']=True
	log(portfolio)
	log(CASH)

def roundown(num):
    num=str(num)
    new=float(num[:num.find('.')+7])
    return new


		






			



	
















# def order(side, quantity, symbol,order_type=ORDER_TYPE_MARKET):
#     try:
#         print("sending order")
#         order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
#         print(order)
#     except Exception as e:
#         print("an exception occured - {}".ORDER_TYPE_MARKETformat(e))
#         return False
#     return True

# # order_succeeded = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)


# order = client.create_order(
#     symbol='BTCUSDT',
#     side=SIDE_SELL,
#     type=ORDER_TYPE_MARKET,
#     quantity=quant
#     )

# print(order)