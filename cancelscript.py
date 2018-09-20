#Use 'pip install ccxt' in terminal and install ccxt.

import ccxt
import time

__author__ = 'Jaqobs'
__credits__ = ['Jaqobs']
__version__ = '1.0'
__maintainer__ = 'Jaqobs'
__email__ = 'jaqobs@jaqobstran.com'
__status__ = 'Production'

apilimit = 5
apisleep = 5
bitmex = ccxt.bitmex({
					'apiKey': '<APIKEY>',		#your replace APIKEY with your API key
					'secret': '<SECRET>',		#replace SECRET with your API secret
					})
			
def create_order(symbol, ordertype, side, amount, price=None):
	apitry = 0
	condition = False

	while (apitry < apilimit) and not condition:
		try:
			order = bitmex.create_order(symbol=symbol, type=ordertype, side=side, amount=amount, price=price)
			print('Order successfully created!')
			print(order)
			condition = True
		except(ccxt.ExchangeError):
			print('Error. Could not create order. Trying again...')
			apitry += 1
			time.sleep(apisleep)


def get_all_positions():
	positions = []
	try:
		positions = bitmex.private_get_position()
	except(ccxt.ExchaneError):
		print('Error. Could not fetch positions.')
	
	return positions

def get_open_positions():
	positions = get_all_positions()
	open_positions = []

	for position in positions: 
		if (int(position['currentQty']) is not 0):
			open_positions.append(position)

	return open_positions


def get_open_orders():
	orders = []
	try:
		orders = bitmex.fetch_open_orders()
	except(ccxt.ExchangeError):
		print('Error. Could not fetch orders.')

	return orders


def cancel_order(orderid):
	apitry = 0
	condition = True
	while (apitry < apilimit) and condition: 
		try:
			bitmex.cancel_order(orderid)
			condition = False
		except:
			print('Could not cancel order. Trying again')
			apitry += 1
			time.sleep(apisleep)


def cancel_all_orders():
	orders = get_open_orders()
	if (orders):
		for order in orders:
			cancel_order (order['id'])

		print('All orders canceled.')
	else:
		print('No open orders.')


def close_all_positions():
	positions = get_open_positions()
	if (positions):
		for position in positions:
			
			if (int(position['currentQty']) > 0):
				side = 'sell'
			elif (int(position['currentQty']) < 0):
				side = 'buy'
			amount = float(position['currentQty']) * -1
			if position['symbol'] == 'XBTUSD':
				symbol = 'BTC/USD'
			else:
				symbol = position['symbol']

			print('Attempting to close position: {}'.format(position['symbol']))
			print('Side: {} -- Quantity: {} -- Symbol: {}'.format(side, amount, symbol))
			create_order(symbol,'market', side, amount)

		print('All open positions closed.')
	else:
		print('No open positions')


def main():
	close_all_positions()
	cancel_all_orders()

if __name__ == '__main__':
	main()