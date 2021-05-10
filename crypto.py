import datetime
import pickle
import requests
import time
import re
from telegram.ext import Updater
from telegram import Update
from telegram.ext import CallbackContext, PollAnswerHandler, PollHandler


date = datetime.datetime.now().strftime("%d-%m-%Y")

def save_variables():
    with open('/home/arya/Documents/Org/Bots/Telegram/crypto', 'wb') as f:
        pickle.dump(variables, f)

with open('/home/arya/Documents/Org/Bots/Telegram/crypto', 'rb') as f:
    variables = pickle.load(f)


crypto_output = {}
    
# Telegram

updater = Updater(token=variables["KEY"], use_context=True)

dispatcher = updater.dispatcher

response = requests.get('https://api.wazirx.com/api/v2/market-status')
markets = [i['baseMarket'] for i in response.json()['markets']]



def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
    print(update,context)



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
            
            temp3 = [x for x in temp[1:] if x in locations.keys()]
            for district in temp3:
                temp2.append(district)
            variables['people'][str(update.effective_chat.id)] = list(set(temp2))
            context.bot.send_message(chat_id=update.effective_chat.id, text="Tracking: "+ str(temp2))
            save_variables()
        if lowered[0:3] == 'del':
            temp = list(map(str.strip, lowered[3:].split(',')))
            temp2 = variables['people'][str(update.effective_chat.id)]
            
            temp3 = [x for x in temp[1:] if x in locations.keys()]
            for district in temp3:
                temp2.append(district)
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
try:
    while True:
        prev_crypto_output = crypto_output
        crypto_output = {}
        
        for person in variables["people"].keys():
            for currency in variables["people"][person]:
                if currency[0] not in crypto_output.keys():
                    # print(currency[0])
                    response = requests.get('https://api.wazirx.com/api/v2/trades?market='+currency[0]+"inr")
                    data = response.json()
                    # print(data[0]["price"])
                    crypto_output[currency[0]] = float(data[0]["price"])
                if currency[1].isdigit():
                    if crypto_output[currency[0]] > float(currency[1]):
                        dispatcher.bot.send_message(chat_id=int(person), text="Target " + currency[0] +" of "+ currency[1] + " reached at " + str(crypto_output[currency[0]]))
                if 2 < len(currency) and currency[2].isdigit():
                    if crypto_output[currency[0]] < float(currency[2]):
                        dispatcher.bot.send_message(chat_id=int(person), text="Loss " + currency[0] +" of "+ currency[2] + " reached at " + str(crypto_output[currency[0]]))
        time.sleep(60)
except KeyboardInterrupt:
    save_variables()

"$(curl https://api.wazirx.com/api/v2/trades?market=$MARKET| jq .[].price | tr -d \")"
