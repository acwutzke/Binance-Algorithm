
from binance.websockets import BinanceSocketManager
import websocket, json, numpy, pandas, datetime
import config
# from algo_functions import *
from binance.client import Client
from testdep import *
# import sys

client = Client(config.API_KEY, config.API_SECRET)
bm = BinanceSocketManager(client)

WATCH_LIST=['dogeusdt@kline_1m', 'btcusdt@kline_1m', 'ethusdt@kline_1m','ltcusdt@kline_1m']

# total portfolio size of 500 USD and max 2 positions
CASH=500.00000
max_pos=2
start=True

portfolio= {}
test=True

# instantiate portfolio
for w in WATCH_LIST:
	portfolio[w]={}
	portfolio[w]['prices']=[]
	portfolio[w]['in_position']=False
	portfolio[w]['stop_price']=0
	portfolio[w]['quantity']=0
	portfolio[w]['bought_price']=0
	portfolio[w]['primed']=False #to indicate that the coin ema10 is below ema30

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

def on_message(message):
	global test
	stream=message['stream']
	symbol=stream[:len(stream)-9].upper()
	close=float(message['data']['k']['c'])
	quantity=0.00438682

	if test:
		order=sell('BTCUSDT',roundown(quantity))
		test=False
		order_successful=order[0]
		order_info=order[1]
		order_handler(order_info, stream)
		print(order_successful)
		print(order_info)








conn_key = bm.start_multiplex_socket(WATCH_LIST, on_message)
# then start the socket manager
bm.start()

# cd desktop\binance-algorithm
# python algotest.py