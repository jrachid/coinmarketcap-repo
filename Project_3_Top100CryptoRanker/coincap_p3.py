import os
import json
import requests
from prettytable import PrettyTable
from colorama import init, Fore, Back, Style
init(convert=True)

convert = input("Please choose your currency (EUR or USD): ").upper()

global_url = 'https://api.coinmarketcap.com/v2/global/?convert=' + convert

request = requests.get(global_url)
results = request.json()

data = results['data']

global_cap = data['quotes'][convert]['total_market_cap']
global_cap_str = '{:,}'.format(global_cap)

while True:
	print()
	print("CoinMarketCap Explorer Menu")
	print("The global market cap is " + convert + global_cap_str)
	print()
	print("1 - Top 100 sorted by rank")
	print("2 - Top 100 sorted by 24 hour change")
	print("3 - Top 100 sorted by 24 hour volume")
	print("0 - Exit")
	print()

	choice = input("What is your choice (1-3): ")

	ticker_url = "https://api.coinmarketcap.com/v2/ticker/?convert=" + convert + "&structure=array&sort="

	if choice == "1":
		ticker_url += 'rank'
	elif choice == "2":
		ticker_url += 'percent_change_24h'
	elif choice == "3":
		ticker_url += 'volume_24h'
	else:
		break

	request = requests.get(ticker_url)
	results = request.json()
	data = results['data']

	table = PrettyTable(['rank', 'Asset', 'Price', 'Market Cap', 'Volume', '1h','24h','7d'])

	print()
	for currency in data:
		rank = currency['rank']
		name = currency['name']
		symbol = currency['symbol']
		quotes = currency['quotes'][convert]
		market_cap = quotes['market_cap']
		hour_change = quotes['percent_change_1h']
		day_change = quotes['percent_change_24h']
		week_change = quotes['percent_change_7d']
		price = round(quotes['price'], 3)
		volume = round(quotes['volume_24h'], 3)

		if hour_change is not None:
			if hour_change > 0:
				hour_change = Back.GREEN + str(hour_change) + '%' + Style.RESET_ALL
			else:
				hour_change = Back.RED + str(hour_change) + '%' + Style.RESET_ALL

		if day_change is not None:
			if day_change > 0:
				day_change = Back.GREEN + str(day_change) + '%' + Style.RESET_ALL
			else:
				day_change = Back.RED + str(day_change) + '%' + Style.RESET_ALL

		if week_change is not None:
			if week_change > 0:
				week_change = Back.GREEN + str(week_change) + '%' + Style.RESET_ALL
			else:
				week_change = Back.RED + str(week_change) + '%' + Style.RESET_ALL

		if volume is not None:
			volume_str = '{:,}'.format(volume)
		else:
			volume_str = str(volume)

		if market_cap is not None:
			market_cap_str = '{:,}'.format(market_cap)
		else:
			market_cap_str = str(market_cap)

		table.add_row([rank,
						name + ' (' + symbol + ')',
						convert + ' ' + str(price),
						convert + ' ' + market_cap_str,
						convert + ' ' + volume_str,
						str(hour_change),
						str(day_change),
						str(week_change)])
	print()
	print(table)
	print()

	choice = input("Again? (y/n): ")
	if choice == 'n':
		break