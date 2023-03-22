import requests
import hmac
import hashlib
import time
import os
import ccxt
from binance.client import Client
from func import getInfos, getSecrets, plotBitcoins, calcSellPrice, calcBuyPrice, lookForSellOrBuy, sell_bitcoins, \
    buy_bitcoins, sendMessage

password = ""               #password to start
api_key = ""                #api_key needed
api_secret = ""             #api_secret needed
endpoint = "https://api.binance.com/api/v3/account"     #endpoint of this connection



secrets = getSecrets(api_key,api_secret,password)

api_key = secrets[0]
api_secret = secrets[1].encode("utf-8")
password = secrets[2]

# Instantiate the Binance exchange object
exchange = ccxt.binance()

# Set your API key and secret
exchange.apiKey = secrets[0]
exchange.secret = secrets[1]
time.sleep(1)
passwordAnswer = input("Passwort:")         #Ask for the password

if password == passwordAnswer:
    os.system('cls')            #clear output
    timestamp = int(time.time() * 1000)  # Timestamp for request signature
    message = f"timestamp={timestamp}".encode("utf-8")  # Generate request signature
    signature = hmac.new(api_secret, message, hashlib.sha256).hexdigest()
    # Set up request headers
    headers = {
        "X-MBX-APIKEY": api_key
    }

    # Set up request parameters
    params = {
        "timestamp": timestamp,
        "signature": signature
    }
    time.sleep(2)
    # Make the request
    response = requests.get(endpoint, headers=headers, params=params)
    time.sleep(2)
    numX = list([0, 0])
    getInfos(response, numX)            #get Infos for your EUR and Bitcoin
    plotBitcoins(exchange)
    sellPrice = 25000
    buyPrice = 0
    oldPrice = 0
    btc_price = 0

    while (True):
        try:

            if response.status_code == 200:

                btc_ticker = exchange.fetch_ticker('BTC/EUR')
                balances = exchange.fetch_balance()
                btc_balance = balances['BTC']['free']
                eur_balance = balances['EUR']['free']
                oldPrice = btc_price
                btc_price = btc_ticker['last']
                os.system('cls')
                amount = eur_balance / btc_price
                bitcoinsPrice = btc_price * btc_balance
                print("Bitcoins:", btc_balance)
                print("Deine Bitcoins in EUR:", bitcoinsPrice)
                print("Allgemeiner Bitcoin Preis:", btc_price)
                print("Alter Bitcoin Preis:", oldPrice)
                print("Dein Verfügbares Geld in EUR", eur_balance)
                look = lookForSellOrBuy(exchange,btc_balance,oldPrice,buyPrice,btc_price,sellPrice)

                if look == 0  and eur_balance > 1:       #buy
                    buy_bitcoins(amount, exchange, btc_price)
                    buyPrice = btc_price

                if look == 1  and eur_balance < 1:       #sell
                    sell_bitcoins(btc_balance, exchange, btc_price)
                    sellPrice = btc_price
                    buyPrice = 0


            else:
                print("Error")
        except:
            print("Exception!!!!")

else:
    print("Password false!")


