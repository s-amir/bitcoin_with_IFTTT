
import json
import time
from datetime import datetime

import requests

my_bitcoin_key = "1b622c29897aa518cd170afda8bccc8a2e2f5b17"
my_IFTTT_key = "cA6gYmvhyLA5mGlPb7qTlG"
bitcoin_api = f"https://api.nomics.com/v1/currencies/ticker?key={my_bitcoin_key}&ids=BTC&interval=1d,30d&convert=USD&per-page=100&page=1"
ifttt_webhook_url = 'https://maker.ifttt.com/trigger/{}/with/key/{}'


def get_latest_bitcoin_price():
    response = requests.get(bitcoin_api)
    data = json.loads(response.text)
    return data[0].get('price')


def post_ifttt_webhook(event, value):
    data = {'value1': value}
    ifttt_event_url = ifttt_webhook_url.format(event, my_IFTTT_key)
    requests.post(ifttt_event_url, json=data)
    print(f'request be event:{event} and value:{value} sent')


def format_bitcoin_list(bitcoin_list):
    list = []
    for row in bitcoin_list:
        price = row['price']
        date = row['date'].strftime('%d.%m.%Y %H:%M')
        formatted_data = f'  {date} ----> ${price}  '
        list.append(formatted_data)
    return '<br>'.join(list)


def main():
    my_emergency_price = 60200
    bitcoin_price_history = []
    while (True):
        price = get_latest_bitcoin_price()
        date = datetime.now()
        bitcoin_price_history.append({'date': date, 'price': price})

        if float(price) <= float(my_emergency_price):
            post_ifttt_webhook('bitcoin_price_emergency', price)

        if len(bitcoin_price_history) == 5:
            post_ifttt_webhook('bitcoin_price_update', format_bitcoin_list(bitcoin_price_history))
            bitcoin_price_history = []

        time.sleep(3)

if __name__ == '__main__':
    main()