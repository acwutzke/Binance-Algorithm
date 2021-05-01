
from binance.websockets import BinanceSocketManager
import websocket, json, numpy, pandas, datetime
import config
from algo_functions import *
from binance.client import Client

client = Client(config.API_KEY, config.API_SECRET)
bm = BinanceSocketManager(client)

WATCH_LIST=['dogeusdt@kline_1m', 'btcusdt@kline_1m', 'ethusdt@kline_1m','ltcusdt@kline_1m']

# total portfolio size of 500 USD and max 2 positions
CASH=500.00000
max_pos=2
start=True

portfolio= {}

# instantiate portfolio
for w in WATCH_LIST:
	portfolio[w]={}
	portfolio[w]['prices']=[]
	portfolio[w]['in_position']=False
	portfolio[w]['stop_price']=0
	portfolio[w]['quantity']=0
	portfolio[w]['bought_price']=0
	portfolio[w]['primed']=False #to indicate that the coin ema10 is below ema30


def on_message(message):
	global CASH, max_pos # import variables
	if message['data']['k']['x']==False: # candle is not closed, skip logic
		return

	# get info from message and portfolio
	num_positions=num_pos(portfolio)
	stream=message['stream']
	symbol=stream[:len(stream)-9].upper()
	close=float(message['data']['k']['c'])
	stop=portfolio[stream]['stop_price']
	bought_price=portfolio[stream]['bought_price']
	in_position=portfolio[stream]['in_position']
	quantity=portfolio[stream]['quantity']
	primed=portfolio[stream]['primed']
	profit=0.000000
	time=str(datetime.datetime.now())[:16]

	# append close and trim
	portfolio[stream]['prices'].append(float(close)) # put this in an if statement with in_position
	portfolio[stream]['prices']=portfolio[stream]['prices'][-300:]

	# calculate emas
	if len(portfolio[stream]['prices'])>200:
		ema10=ema(portfolio[stream]['prices'],30)
		ema30=ema(portfolio[stream]['prices'],100)
		if ema10<ema30:
			portfolio[stream]['primed']=True
	else:
		# not enough data to calculate ema
		return

	# check close against stop price
	if in_position and close<stop:
		# order_successful=sell(symbol,quantity)
		CASH=CASH+(close*quantity)
		profit=quantity*(close-bought_price)
		order_successful=True
		if order_successful:
			portfolio[stream]['in_position']=False
			portfolio[stream]['stop_price']=0
			portfolio[stream]['quantity']=0
			portfolio[stream]['bought_price']=0
			log_message=['Sell',symbol,quantity,stop,'STOP',profit]
			print(log_message)
			print(CASH)
			return

		else:
			# log('Failed to execute sale on stop price...')
		

	# check whether ema10 has decreased below ema30
	if in_position:
		if ema10<ema30:
			# order_successful=sell(symbol,quantity)
			CASH=CASH+(close*quantity)
			profit=quantity*(close-bought_price)
			order_successful=True
			if order_successful:
				portfolio[stream]['in_position']=False
				portfolio[stream]['stop_price']=0
				portfolio[stream]['quantity']=0
				portfolio[stream]['bought_price']=0
				log_message=['Sell',symbol,quantity,close,'EMA',profit]
				print(log_message)
				print(CASH)

			else:
				# log('Failed to execute sale on EMA...')
			return

	# check whether ema10 has increased above ema30
	else:
		if ema10>ema30 and num_positions<max_pos and primed==True:
			portfolio[stream]['primed']==False
			buy_quantity=CASH/close/(max_pos-num_positions)
			CASH=CASH-buy_quantity*close
			# order_successful=buy(symbol,buy_quantity)
			order_successful=True
			if order_successful:
				portfolio[stream]['in_position']=True
				portfolio[stream]['stop_price']=ema30
				portfolio[stream]['quantity']=buy_quantity
				portfolio[stream]['bought_price']=close
				CASH=CASH
				log_message=['Buy',symbol,buy_quantity,close,'EMA']
				print(log_message)
				print(CASH)

			else:
				# log('Failed to buy on EMA...')
		elif ema10>ema30:
			portfolio[stream]['primed']==False
		return




# start any sockets here, i.e a trade socket
conn_key = bm.start_multiplex_socket(WATCH_LIST, on_message)
# then start the socket manager
bm.start()

"""
Need to fix it so that coins are in wait mode so that we only buy on the cross.
"""

