import platform
import aiohttp
import asyncio
import argparse
from datetime import datetime, timedelta

async def get_currency_rates(days):
    async with aiohttp.ClientSession() as session:
        currency_rates = []
        for i in range(days):
            date = (datetime.now() - timedelta(days=i+1)).strftime('%d.%m.%Y')
            url = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date}'
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    eur_rate = next((rate for rate in data['exchangeRate'] if rate['currency'] == 'EUR'), None)
                    usd_rate = next((rate for rate in data['exchangeRate'] if rate['currency'] == 'USD'), None)
                    if eur_rate and usd_rate:
                        currency_rates.append({
                            date: {
                                'EUR': {
                                    'sale': eur_rate['saleRate'],
                                    'purchase': eur_rate['purchaseRate']
                                },
                                'USD': {
                                    'sale': usd_rate['saleRate'],
                                    'purchase': usd_rate['purchaseRate']
                                }
                            }
                        })
        return currency_rates

if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    parser = argparse.ArgumentParser(description="Get currency rates from PrivatBank API.")
    parser.add_argument("days", type=int, help="Number of days to fetch currency rates for (up to 10 days)")

    args = parser.parse_args()
    if args.days < 1 or args.days > 10:
        print("Error: Number of days must be between 1 and 10")
    else:
        currency_rates = asyncio.run(get_currency_rates(args.days))
        print(currency_rates)
