import os
import json
import requests
from datetime import datetime
from prettytable import PrettyTable as pt 
from colorama import init, Fore, Back, Style
init(convert=True)

convert = 'USD'

listing_url = 'https://api.coinmarketcap.com/v2/listings/?convert=' + convert
url_end = '?structure=array&convert=' + convert

request = requests.get(listing_url)
results = request.json()

data = results['data']

ticker_url_pairs = {}

for currency in data:
	symbol = currency['symbol']
	url = currency['id']
	name = currency['name']
	ticker_url_pairs[symbol] = url

print()
print("MY PORTFOLIO")
print()

portfolio_value = 0.00
last_updated = 0

table = pt(['Asset', 'Amount Owned', convert + ' Value', 'Price', '1h', '24h', '7d'])

with open ("portfolio.txt") as inp:
	for line in inp:
		ticker, amount = line.split()
		ticker = ticker.upper()

		ticker_url = 'https://api.coinmarketcap.com/v2/ticker/' + str(ticker_url_pairs[ticker]) + '/' + url_end
		request = requests.get(ticker_url)
		results = request.json()

		currency = results['data'][0]
		rank = currency['rank']
		name = currency['name']
		last_updated = currency['last_updated']
		symbol = currency['symbol']
		quotes = currency['quotes'][convert]
		hour_change = quotes['percent_change_1h']
		day_change = quotes['percent_change_24h']
		week_change = quotes['percent_change_7d']
		price = quotes['price']

		value = float(price) * float(amount)

		if hour_change > 0:
			hour_change = Back.GREEN + str(hour_change) + '%' + Style.RESET_ALL
		else:
			hour_change = Back.RED + str(hour_change) + '%' + Style.RESET_ALL

		if day_change > 0:
			day_change = Back.GREEN + str(day_change) + '%' + Style.RESET_ALL
		else:
			day_change = Back.RED + str(day_change) + '%' + Style.RESET_ALL

		if week_change > 0:
			week_change = Back.GREEN + str(week_change) + '%' + Style.RESET_ALL
		else:
			week_change = Back.RED + str(week_change) + '%' + Style.RESET_ALL

		portfolio_value += value

		value_str = '{:,}'.format(round(value, 3))
		price = round(price, 3)

		table.add_row([name + ' (' + symbol + ')',
						amount,
						convert + ' ' + value_str,
						convert + ' '+ str(price),
						str(hour_change),
						str(day_change),
						str(week_change)])

print(table)
print()

portfolio_value_str = '{:,}'.format(round(portfolio_value, 2))
last_updated_str = datetime.fromtimestamp(last_updated).strftime('%B %d, %Y at %I:%M%p')

print("Total Portfolio Value: " + Back.GREEN + convert + ' ' + portfolio_value_str + Style.RESET_ALL)
print("API Results last updated on " + last_updated_str)
