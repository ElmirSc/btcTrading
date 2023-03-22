import pandas as pd
import matplotlib.pyplot as plt
import datetime
import telebot
import time
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events

def getSecrets(api_key, api_secret, password):
    secrets = list(["", "", ""])
    with open("infos.txt") as file:
        contents = file.readlines()

    for line in contents:
        if "Passwort" in line:
            password = line.split(":")[1].strip()
        elif "Api" in line:
            api_key = line.split(":")[1].strip()
        elif "Secret key" in line:
            api_secret = line.split(":")[1].strip()

    secrets[0] = api_key
    secrets[1] = api_secret
    secrets[2] = password

    return secrets


def calcSellPrice(price):

    sellPrice = price*1.02

    return sellPrice

def sendMessage(priceBitcoins,numberBitcoins,check):
    api_id = '26278017'
    api_hash = '4ffa33f476571fa6641b014e523722ed'
    token = '6252172068:AAF_vSsOUJyYFLsdXmdx0wtbhggXzoH6DVc'
    message = "Anzahl Bitcoins: " + numberBitcoins
    message2 = "Bitcoins in EUR: " + priceBitcoins
    message3 = "-----------------------------------------"

    # your phone number
    phone = '+436604479892'

    # creating a telegram session and assigning
    # it to a variable client
    client = TelegramClient('session', api_id, api_hash)

    # connecting and building the session
    client.connect()

    # in case of script ran first time it will
    # ask either to input token or otp sent to
    # number or sent or your telegram id
    if not client.is_user_authorized():

        client.send_code_request(phone)

        # signing in the client
        client.sign_in(phone, input('Enter the code: '))

    try:
        # receiver user_id and access_hash, use
        # my user_id and access_hash for reference
        myself = client.get_me()
        print(myself)

        receiver = InputPeerUser(5198418491, -6655568474495981349)

        # sending message using telegram client
        client.send_message(receiver, message3, parse_mode='html')
        client.send_message(receiver, message, parse_mode='html')
        client.send_message(receiver, message2, parse_mode='html')
    except Exception as e:

        # there may be many error coming in while like peer
        # error, wrong access_hash, flood_error, etc
        print(e);

    # disconnecting the telegram session
    client.disconnect()
    return

def sendMessageSell(sold):
    api_id = '26278017'
    api_hash = '4ffa33f476571fa6641b014e523722ed'
    token = '6252172068:AAF_vSsOUJyYFLsdXmdx0wtbhggXzoH6DVc'
    message = "Sold Bitcoins: " + str(sold)

    message3 = "-----------------------------------------"

    # your phone number
    phone = '+436604479892'

    # creating a telegram session and assigning
    # it to a variable client
    client = TelegramClient('session', api_id, api_hash)

    # connecting and building the session
    client.connect()

    # in case of script ran first time it will
    # ask either to input token or otp sent to
    # number or sent or your telegram id
    if not client.is_user_authorized():
        client.send_code_request(phone)

        # signing in the client
        client.sign_in(phone, input('Enter the code: '))

    try:
        # receiver user_id and access_hash, use
        # my user_id and access_hash for reference
        myself = client.get_me()
        print(myself)

        receiver = InputPeerUser(5198418491, -6655568474495981349)

        # sending message using telegram client
        client.send_message(receiver, message3, parse_mode='html')
        client.send_message(receiver, message, parse_mode='html')

    except Exception as e:

        # there may be many error coming in while like peer
        # error, wrong access_hash, flood_error, etc
        print(e);

    # disconnecting the telegram session
    client.disconnect()
    return


def sendMessageBuy(bought):
    api_id = '26278017'
    api_hash = '4ffa33f476571fa6641b014e523722ed'
    token = '6252172068:AAF_vSsOUJyYFLsdXmdx0wtbhggXzoH6DVc'
    message = "Gekaufte Bitcoins: " + str(bought)

    message3 = "-----------------------------------------"

    # your phone number
    phone = '+436604479892'

    # creating a telegram session and assigning
    # it to a variable client
    client = TelegramClient('session', api_id, api_hash)

    # connecting and building the session
    client.connect()

    # in case of script ran first time it will
    # ask either to input token or otp sent to
    # number or sent or your telegram id
    if not client.is_user_authorized():
        client.send_code_request(phone)

        # signing in the client
        client.sign_in(phone, input('Enter the code: '))

    try:
        # receiver user_id and access_hash, use
        # my user_id and access_hash for reference
        myself = client.get_me()
        print(myself)

        receiver = InputPeerUser(5198418491, -6655568474495981349)

        # sending message using telegram client
        client.send_message(receiver, message3, parse_mode='html')
        client.send_message(receiver, message, parse_mode='html')

    except Exception as e:

        # there may be many error coming in while like peer
        # error, wrong access_hash, flood_error, etc
        print(e);

    # disconnecting the telegram session
    client.disconnect()
    return

def calcBuyPrice(price):
    buyPrice = price
    return buyPrice

def lookForSellOrBuy(exchange, numberBitcoins, oldPrice,buyPrice, btcPrice , sellPrice):

    symbol = 'BTC/EUR'

    # Abrufen der letzten Woche an Kursdaten
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe='1m')

    # Konvertieren Sie die Daten in einen Pandas DataFrame
    df = pd.DataFrame(ohlcv, columns=['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])

    # Konvertieren Sie die Zeitstempel in Datetime-Objekte
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms')
    sumOfMax = sum(df['Close']) / 500
    a = df['Close']

    sumOfLittle = 0

    for x in range(374, 499):
        sumOfLittle = sumOfLittle + a[x]

    sumOfLittle = sumOfLittle/125

    bitcoins = float(numberBitcoins)
    if oldPrice == 0:
        oldPrice = a[499]

    if  sumOfMax < sumOfLittle  and sellPrice < btcPrice and sellPrice > 0 or sumOfMax < sumOfLittle and btcPrice > oldPrice or btcPrice < sellPrice-1000:
        return 0


    if btcPrice < buyPrice-1000  or btcPrice < oldPrice :
        return 1


    return 3

def getInfos(response, numb):
    data = response.json()
    counter = 0

    # Parse the response JSON
    for asset in data["balances"]:
        # Check if the asset symbol is BTC
        if asset["asset"] == "BTC":
            counter = counter + 1
            numb[0] = asset["free"]
        if asset["asset"] == "EUR":
            counter = counter + 1
            numb[1] = asset["free"]
        if counter == 2:
            break

    else:
        print("Request failed with status code:", response.status_code)
    return

def buy_bitcoins(amount, exchange,btc_price):
    order = exchange.create_order(symbol='BTC/EUR', type='limit', side='buy', amount=amount, price=btc_price)
    print("Bought Bitcoins", amount)
    sendMessageBuy(amount)


def sell_bitcoins(amount, exchange,btc_price):
    order = exchange.create_order(symbol='BTC/EUR', type='limit', side='sell', amount=amount, price=btc_price)
    print("Sold Bitcoins", amount)
    sendMessageSell(amount)

def plotBitcoins(exchange):
    symbol = 'BTC/EUR'
    # get the server timestamp
    # get the server timestamp

    # send the request
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe='1m')

    # Abrufen der letzten Woche an Kursdaten
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe='1m')

    # Konvertieren Sie die Daten in einen Pandas DataFrame
    df = pd.DataFrame(ohlcv, columns=['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])

    # Konvertieren Sie die Zeitstempel in Datetime-Objekte
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms')
    df['Timestamp'] = df['Timestamp'].dt.strftime('%H:%M')


    # Plotten Sie die Daten
    plt.plot(df['Timestamp'], df['Close'])
    plt.xlabel('Datum')
    plt.ylabel('Preis (EUR)')
    plt.title('Bitcoin-Preis der letzten Woche')
    plt.xticks(df['Timestamp'][::50])

    plt.show()

