#!/etc/inspiringmemes_bot/inspiringmemesenv/bin/python
# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import requests
import shutil
import datetime
import os
import json

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.

def timeStamped(fname, fmt='%d-%m-%Y %H-%M-%S_{fname}'):
    return datetime.datetime.now().strftime(fmt).format(fname=fname)

def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def biftdus(bot, update):
    """Send a message when the command /biftdus is issued."""
    update.message.reply_text('Ja! I bims! ¯\_(ツ)_/¯')

def fuckoff(bot, update):
    """Just find out"""
    update.message.reply_text('Oh fuck you too!')

def sendmeme(bot, update):
    """Send a dank inspiring meme when the command /sendmeme is issued."""
    chat_id = update.message.chat_id
    res = requests.get('http://inspirobot.me/api?generate=true').text

    response = requests.get(res, stream=True)

    with open('/etc/inspiringmemes_bot/inspiringmemesenv/memehof/img.jpg', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del res

    bot.send_photo(chat_id=chat_id, photo=open('/etc/inspiringmemes_bot/inspiringmemesenv/memehof/img.jpg','rb'))

def itsdangerous(bot, update):
    """command /dangerous"""
    chat_id = update.message.chat_id

    pic = '/etc/inspiringmemes_bot/inspiringmemesenv/memehof/dangerous.jpg'

    bot.send_photo(chat_id=chat_id, photo=open(pic,'rb'),caption="It's dangerous to go alone, take this!")

def SendDeal(bot, update):

    chat_id = update.message.chat_id
    res = requests.get('https://api.chrono.gg/deals').text
    res = json.loads(res)

    deal = "Today's Deal is: " + res['name'] + "!"
    sale_price = "The price is: " + res['sale_price'] + " USD"
    discount_fprice = "Which is a " + res['discount'] + " Discount " + "from it's original Price at " + res['normal_price'] + "." + "\n"
    gethere = "You can get it here: " + res['unique_url']
    messagetext = deal + "\n" + sale_price + "\n" + discount_fprice + "\n" + gethere + "\n"

    image = res['promo_image']

    responseimg = requests.get(image, stream=True)
    with open('/etc/inspiringmemes_bot/inspiringmemesenv/memehof/deal.jpg', 'wb') as out_file:
       shutil.copyfileobj(responseimg.raw, out_file)
    del responseimg

    bot.send_photo(chat_id=chat_id, photo=open('/etc/inspiringmemes_bot/inspiringmemesenv/memehof/deal.jpg','rb'))
    update.message.reply_text(messagetext,disable_web_page_preview=True)

def watt(bot, update):
    """Send a dank JJ Watt"""
    chat_id = update.message.chat_id

    bot.send_photo(chat_id=chat_id, photo=open('/etc/inspiringmemes_bot/inspiringmemesenv/memehof/watt.jpg','rb'))

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("YOUR_TOKEN_HERE")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("sendmeme", sendmeme))
    dp.add_handler(CommandHandler("biftdus", biftdus))
    dp.add_handler(CommandHandler("fuckoff", fuckoff))
    dp.add_handler(CommandHandler("watt", watt))
    dp.add_handler(CommandHandler("itsdangerous", itsdangerous))
    dp.add_handler(CommandHandler("SendDeal", SendDeal))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
