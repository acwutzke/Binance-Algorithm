import datetime

def num_pos(portfolio):
	count=0
	for p in portfolio:
		if portfolio[p]['in_position']:
			count+=1
	return count

def ema(prices,length):
	init=sum(prices[:length])/length
	ema=[init]
	mult=(2/(length+1))

	for i in range(length,len(prices)):
		current_ema=(prices[i]-ema[i-length])*mult+ema[i-length]
		ema.append(current_ema)
	return ema[-1:][0]

def sell(stream,quantity):
	order_successful = order(SIDE_SELL, quantity, stream)
	if order_successful:
		return True
	else:
		return False
    	
def buy(stream,quantity):
	order_successful = order(SIDE_BUY, quantity, stream)
	if order_successful:
		return True
	else:
		return False

# def order(side, quantity, symbol,order_type=ORDER_TYPE_MARKET):
#     try:
#         print("sending order")
#         order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
#         print(order)
#     except Exception as e:
#         print("an exception occured - {}".format(e))
#         return False
#     return True

def log(text):
    time=str(datetime.datetime.now())[:16]
    text=time+' : '+str(text)
    with open(r'log.txt', 'a') as f:
        f.write(text)
        f.write('\n')

def holdings(portfolio):
	hold={}
	for p in portfolio:
		if portfolio[p]['in_position']:
				hold[p]=[portfolio[p]['quantity'],portfolio[p]['bought_price']]

	print(hold)










		



