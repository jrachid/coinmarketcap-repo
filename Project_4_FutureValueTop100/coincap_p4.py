import math
import json
import locale
import requests
from prettytable import PrettyTable 

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

global_url = 'https://api.coinmarketcap.com/v2/global'
ticker_url = 'https://api.coinmarketcap.com/v2/ticker/?structure=array'

request = requests.get(global_url)
result = request.json()
data = result['data']

global_cap = int(data['quotes']['USD']['total_market_cap'])

table = PrettyTable(['Name','Ticker',"% of total global cap",'Current','7.7T (Gold)',
	'36.8T (Narrow Money)', '73T (World Stock Markets)','90.4T (Broad Money)', '217T (Real Estate)','544T (Derivatives'])

request = requests.get(ticker_url)
results = request.json()
data = results['data']

for currency in data:
	name = currency['name']
	ticker = currency['symbol']
	percentage_of_global_cap = float(currency['quotes']['USD']['market_cap']) / float(global_cap)

	current_price = round(float(currency['quotes']['USD']['price']), 2)
	available_supply = float(currency['total_supply'])

	tri_7price = round(7700000000000 * percentage_of_global_cap / available_supply, 2)
	tri_36price = round(36800000000000 * percentage_of_global_cap / available_supply, 2)
	tri_73price = round(73000000000000 * percentage_of_global_cap / available_supply, 2)
	tri_90price = round(90400000000000 * percentage_of_global_cap / available_supply, 2)
	tri_217price = round(217000000000000 * percentage_of_global_cap / available_supply, 2)
	tri_544price = round(544000000000000 * percentage_of_global_cap / available_supply, 2)

	percentage_of_global_cap_str = str(round(percentage_of_global_cap * 100, 2)) + '%'
	current_price_str = '$' + str(current_price)
	tri_7price_str = '$' + locale.format('%.2f', tri_7price, True)
	tri_36price_str = '$' + locale.format('%.2f', tri_36price, True)
	tri_73price_str = '$' + locale.format('%.2f', tri_73price, True)
	tri_90price_str = '$' + locale.format('%.2f', tri_90price, True)
	tri_217price_str = '$' + locale.format('%.2f', tri_217price, True)
	tri_544price_str = '$' + locale.format('%.2f', tri_544price, True)

	table.add_row([name,
					ticker,
					percentage_of_global_cap_str,
					current_price_str,
					tri_7price_str,
					tri_36price_str,
					tri_73price_str,
					tri_90price_str,
					tri_217price_str,
					tri_544price_str])
print()
print(table)
print()