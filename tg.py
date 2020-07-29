from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, RegexHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram import Bot as tgBot
import shelve

import datetime
import os

import logging

teletoken = os.environ['TELETOKEN']

updater = Updater(teletoken)
dispatcher = updater.dispatcher

loglevel = "DEBUG"
logpath = "bot.log"
if loglevel == "DEBUG":
    logging.basicConfig(filename=logpath, level=logging.DEBUG, format='%(asctime)s %(message)s')
elif loglevel == "INFO":
    logging.basicConfig(filename=logpath, level=logging.INFO, format='%(asctime)s %(message)s')
else:
    logging.basicConfig(filename=logpath, level=logging.WARNING, format='%(asctime)s %(message)s')


### Bot stuff

def sendTele(recv, msg):
    bot = tgBot(teletoken)
    bot.send_message(chat_id=str(recv), text=str(msg))


def start(bot, update):
    userid = update.message.from_user.id
    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    print(dtime + " - " +str(userid) + ' started TG bot')


def myid(bot, update):
    userid = update.message.from_user.id
    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    update.message.reply_text('Your Telegram ID is: ' + str(userid))
    print(dtime + " - " +str(userid) + ' asked for id')


def processphoto(bot, update):
    userid = update.message.from_user.id
    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    update.message.reply_text('received image!')
    print(dtime + " - " + str(userid) + ' sent photo to bot')


def processtext(bot, update):
    userid = update.message.from_user.id
    text = update.message.text
    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    update.message.reply_text('Greetings! This bot is alive!')
    print(dtime + " - " + str(userid) + ' sent text message:\n' + str(text))


### VM control

def create(bot, update):
    userid = update.message.from_user.id
    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')


def destroy(bot, update):
    userid = update.message.from_user.id
    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')


def restart(bot, update):
    userid = update.message.from_user.id
    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')


def listvms(bot, update):
    userid = update.message.from_user.id
    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')


def initbot():

    usertext = MessageHandler(Filters.private, processtext)
    userphoto = MessageHandler(Filters.photo, processphoto)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('myid', myid))

    updater.dispatcher.add_handler(CommandHandler('create', create))
    updater.dispatcher.add_handler(CommandHandler('destroy', destroy))
    updater.dispatcher.add_handler(CommandHandler('restart', restart))
    updater.dispatcher.add_handler(CommandHandler('list', listvms))


    dispatcher.add_handler(usertext)
    dispatcher.add_handler(userphoto)


initbot()
updater.start_polling()
