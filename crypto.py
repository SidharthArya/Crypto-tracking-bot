import datetime
import pickle
import requests
import time
import re
import os
from telegram.ext import Updater
from telegram import Update
from telegram.ext import CallbackContext, PollAnswerHandler, PollHandler
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--conky')
parser.add_argument('-f')
parser.add_argument('--cb', default=False, action='store_true')
args = parser.parse_args()
me = os.path.isdir("/home/arya")
date = datetime.datetime.now().strftime("%d-%m-%Y")
if args.f:
    variables_file = args.f
    try:
        with open("/home/arya/Documents/Org/Bots/Telegram/me") as f:
            me = f.read()
    except:
        me = ""
else:
    variables_file = '~/.config/crypto'
    if not os.path.isfile(variables_file):
        with open(variables_file, 'w') as f:
            pass
def save_variables():
    with open(variables_file, 'wb') as f:
        pickle.dump(variables, f)

with open(variables_file, 'rb') as f:
    variables = pickle.load(f)

if args.conky:
    with open(args.conky, 'w') as d:
        d.truncate(0)
        d.write("Cryptocurrency\n\n")


def coinbase():
    pass
        
crypto_output = {}
    
# Telegram

updater = Updater(token=variables["KEY"], use_context=True)

dispatcher = updater.dispatcher

response = requests.get('https://api.wazirx.com/api/v2/market-status')
markets = [i['baseMarket'] for i in response.json()['markets']]
print(variables["people"])



def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
    if os.path.isdir("/home/arya"):
        print(update,context)
    else:
        variables[str(update.effective_chat.id)] = []
        context.bot.send_message(chat_id=update.effective_chat.id, text="Registered")
        



def echo (update, context):
    if str(update.effective_chat.id) in variables['people'].keys():
        lowered = update.message.text.lower()
        if lowered[0:4] == 'list':
            context.bot.send_message(chat_id=update.effective_chat.id, text="List: " + str(markets))
            return
        if lowered[0:3] == 'val':
            temp = list(map(str.strip, lowered[3:].split(',')))
            for i in temp:
                context.bot.send_message(chat_id=update.effective_chat.id, text= i + ": " + str(crypto_output[i]))
            return
        if lowered[0:3] == 'get':
            temp = list(map(str.strip, lowered[3:].split(',')))
            context.bot.send_message(chat_id=update.effective_chat.id, text="Tracking: " + str(variables['people'][str(update.effective_chat.id)]))
            return
        if lowered[0:3] == 'add':
            temp = list(map(str.strip, lowered[3:].split(',')))
            temp2 = variables['people'][str(update.effective_chat.id)]
            
            temp3 = [x for x in temp if x[0] in markets]
            for rule in temp3:
                temp2.append(rule)
            variables['people'][str(update.effective_chat.id)] = list(set(temp2))
            context.bot.send_message(chat_id=update.effective_chat.id, text="Tracking: "+ str(temp2))
            save_variables()
            return
        if lowered[0:3] == 'del':
            temp = list(map(str.strip, lowered[3:].split(',')))
            temp2 = variables['people'][str(update.effective_chat.id)]
            
            temp3 = [x for x in temp[1:] if x in locations.keys()]
            for rule in temp3:
                temp2.append(rule)
            variables['people'][str(update.effective_chat.id)] = list(set(temp2))
            context.bot.send_message(chat_id=update.effective_chat.id, text="Tracking: "+ str(temp2))
            save_variables()
        
        temp = list(map(str.split, list(map(str.strip, lowered.split(',')))))
        temp3 = [x for x in temp if x[0] in markets]
        variables['people'][str(update.effective_chat.id)] = temp3
        context.bot.send_message(chat_id=update.effective_chat.id, text="Tracking: "+ str(temp3))
        save_variables()
            


from telegram.ext import CommandHandler
start_handler = CommandHandler('start', start)

from telegram.ext import MessageHandler, Filters
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    
dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)

updater.start_polling()

if args.conky:
   with open(args.conky, 'w') as d:
       d.truncate(0)
       d.write("Cryptocurrency\n\n")

while True:
    prev_crypto_output = crypto_output
    crypto_output = {}
    try:
        wazirx = requests.get('https://api.wazirx.com/api/v2/tickers')
        data = wazirx.json()
        if args.cb:
            coinb = requests.get('https://api.coinbase.com/v2/exchange-rates?currency=INR')
            coinb = coinb.json()
    except Exception as e:
        time.sleep(10)
        print("Exception " + str(e))
        continue
    for person in variables["people"].keys():
        if person == me:
            conkytext = ""
        for currency in variables["people"][person]:
            up = 0
            down = 0
            if currency[1].isdigit():
                current= data[currency[0] + "inr"]["last"]
                if float(current) > float(currency[1]):
                    up += 1
                    dispatcher.bot.send_message(chat_id=int(person), text="Target " + currency[0] +" of "+ currency[1] + " reached at " + str(crypto_output[currency[0]]))
            if 2 < len(currency) and currency[2].isdigit():
                if float(current) < float(currency[2]):
                    down += 1
                    dispatcher.bot.send_message(chat_id=int(person), text="Loss " + currency[0] +" of "+ currency[2] + " reached at " + str(crypto_output[currency[0]]))
            if args.conky and me == person:
                try:
                    coinbasev = str(1.0/float(coinb["data"]["rates"][currency[0].upper()]))
                except:
                    coinbasev = ""
                if up > down:
                    conkytext += currency[0].capitalize() + ": ${color green}" +  current + "${color}\n"
                elif up < down:
                    conkytext += currency[0].capitalize() + ": ${color red} " + current + "${color}\n"
                else:
                    conkytext += currency[0].capitalize() + ": " + current + " " + coinbasev + "\n"
        if args.conky:
            with open(args.conky, 'w') as d:
                d.truncate(0)
                d.write(conkytext)
                
    time.sleep(10)

"$(curl https://api.wazirx.com/api/v2/trades?market=$MARKET| jq .[].price | tr -d \")"
