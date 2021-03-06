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

def log(text):
    time=str(datetime.datetime.now())[:16]
    text=time+' : '+str(text)
    with open(r'log.txt', 'a') as f:
        f.write(text)
        f.write('\n')

def roundown(num, dec):
    num=str(num)
    new=float(num[:num.find('.')+dec+1])
    return new



def holdings(portfolio):
    holdings={}
    for h in portfolio:
        if portfolio[h]['in_position']:
            holdings[h]={}
            holdings[h]['quantity']=portfolio[h]['quantity']
            holdings[h]['bought_price']=portfolio[h]['bought_price']
    return holdings










		



