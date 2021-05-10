
from binance.websockets import BinanceSocketManager
import websocket, json, numpy, pandas, datetime
import config
from algo_functions import *
from binance.client import Client
from binance.enums import *

client = Client(config.API_KEY, config.API_SECRET)
bm = BinanceSocketManager(client)

WATCH_LIST=['dogeusdt@kline_1m', 'btcusdt@kline_1m', 'ethusdt@kline_1m','ltcusdt@kline_1m']

# total portfolio size of 500 USD and max 2 positions
CASH=500.00000
max_pos=2
total_profit=0
start=True
stopper=False
portfolio= {}

# instantiate portfolio
for w in WATCH_LIST:
	portfolio[w]={}
	portfolio[w]['prices']=[]
	portfolio[w]['in_position']=False
	portfolio[w]['stop_price']=0
	portfolio[w]['quantity']=0
	portfolio[w]['bought_price']=0
	portfolio[w]['primed']=False # to indicate that the coin ema_short is below ema_long and is ready to be bought on cross above.

def order_handler(order_info, stream):
	global portfolio, CASH
	fills=order_info['fills']
	side=order_info['side']
	sale_price=0
	log(order_info)
	for f in fills:
		if side=='SELL':
			portfolio[stream]['quantity']-=float(f['qty'])
			CASH+=float(f['price'])*float(f['qty'])
			CASH-=float(f['commission'])
			portfolio[stream]['in_position']=False
			sale_price+=(float(f['price'])*float(f['qty'])-float(f['commission']))
			portfolio[stream]['stop_price']=0
		if side=='BUY':
			portfolio[stream]['quantity']+=float(f['qty'])
			portfolio[stream]['quantity']-=float(f['commission'])
			CASH-=float(f['price'])*float(f['qty'])
			portfolio[stream]['bought_price']+=float(f['price'])*float(f['qty'])
			portfolio[stream]['in_position']=True
	if side=='SELL':
		profit=sale_price-portfolio[stream]['bought_price']
		portfolio[stream]['bought_price']=0
		log('Profit on sale: '+ str(profit))
	log('New cash balance: ' + str(CASH))
	log(holdings(portfolio)) # print quantity/book value of current holdings

def buy(symbol,quantity):
	try:
		order = client.create_order(
		symbol=symbol,
		side=SIDE_BUY,
		type=ORDER_TYPE_MARKET,
		quantity=quantity
		)
	except Exception as e:
		log("an exception occured - {}".format(e))
		return False, False
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
		log("an exception occured - {}".format(e))
		return False, False
	return True, order

def on_message(message):
	global CASH, max_pos, stopper # import variables
	if stopper==True:
		return
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

	# append close and trim
	portfolio[stream]['prices'].append(float(close)) # put this in an if statement with in_position
	portfolio[stream]['prices']=portfolio[stream]['prices'][-600:] # trim

	# calculate emas
	if len(portfolio[stream]['prices'])>200:
		ema_short=ema(portfolio[stream]['prices'],30)
		ema_long=ema(portfolio[stream]['prices'],100)
		if ema_short<ema_long:
			portfolio[stream]['primed']=True
	else:
		# not enough data to calculate ema
		return

	# check close against stop price and sell if necessary
	if in_position and close<stop:
		order=sell(symbol,roundown(quantity))
		order_successful=order[0]
		order_info=order[1]
		if order_successful:
			print(order_info) # can remove later
			order_handler(order_info, stream) # updates cash, quantity, in_position, bought_price, prints to log
			return
		else:
			log('Trade did not go through, stopping.')
			# stopper=True
			return

	if in_position:
		if ema_short<ema_long:
			order=sell(symbol,roundown(quantity))
			order_successful=order[0]
			order_info=order[1]
			if order_successful:
				print(order_info) # can remove later
				order_handler(order_info, stream) # updates cash, quantity, in_position, bought_price, prints to log
				return
			else:
				log('Trade did not go through, stopping.')
				# stopper=True
				return

	# check whether ema_short has increased above ema_long
	else:
		if ema_short>ema_long and num_positions<max_pos and primed==True:
			portfolio[stream]['primed']=False
			quantity=round(CASH/close/(max_pos-num_positions),6)
			log(symbol)
			log(quantity)
			order=buy(symbol,quantity) # execute buy order
			order_successful=order[0]
			order_info=order[1]
			if order_successful:
				print(order_info) # can remove later
				order_handler(order_info, stream) # updates cash, quantity, in_position, bought_price, prints to log
				portfolio[stream]['stop_price']=ema_long
				return
			else:
				log('Trade did not go through')
				# stopper=True
				return

		elif ema_short>ema_long:
			portfolio[stream]['primed']=False
			return


# start any sockets here, i.e a trade socket
conn_key = bm.start_multiplex_socket(WATCH_LIST, on_message)
# then start the socket manager
bm.start()


