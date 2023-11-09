import platform
import aiohttp
import asyncio
import argparse
from datetime import datetime, timedelta

async def get_currency_rates(days, currencies):
    async with aiohttp.ClientSession() as session:
        currency_rates = []
        for i in range(days):
            date = (datetime.now() - timedelta(days=i + 1)).strftime('%d.%m.%Y')
            url = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date}'
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    rates = {}
                    for currency_code in currencies:
                        rate = next((rate for rate in data['exchangeRate'] if rate['currency'] == currency_code), None)
                        if rate:
                            rates[currency_code] = {
                                'sale': rate['saleRate'],
                                'purchase': rate['purchaseRate']
                            }
                    if rates:
                        currency_rates.append({date: rates})
        return currency_rates

if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    parser = argparse.ArgumentParser(description="Get currency rates from PrivatBank API.")
    parser.add_argument("days", type=int, help="Number of days to fetch currency rates for (up to 10 days)")
    parser.add_argument("--currencies", nargs="+", default=['EUR', 'USD'],
                        help="List of currencies to fetch rates for (e.g., EUR USD)")
    args = parser.parse_args()

    if args.days < 1 or args.days > 10:
        print("Error: Number of days must be between 1 and 10")
    else:
        currency_rates = asyncio.run(get_currency_rates(args.days, args.currencies))
        print(currency_rates)

# py .\API.py 2 --currencies EUR USD PLN
# >>> [{'08.11.2023': {'EUR': {'sale': 40.4, 'purchase': 39.4}, 'USD': {'sale': 37.4, 'purchase': 36.8}, 
# 'PLN': {'sale': 9.1, 'purchase': 8.55}}}, {'07.11.2023': {'EUR': {'sale': 40.4, 'purchase': 39.4}, 
# 'USD': {'sale': 37.4, 'purchase': 36.8}, 'PLN': {'sale': 9.1, 'purchase': 8.55}}}]

# py .\API.py 2
# >>> [{'08.11.2023': {'EUR': {'sale': 40.4, 'purchase': 39.4}, 'USD': {'sale': 37.4, 'purchase': 36.8}}}, 
# {'07.11.2023': {'EUR': {'sale': 40.4, 'purchase': 39.4}, 'USD': {'sale': 37.4, 'purchase': 36.8}}}]