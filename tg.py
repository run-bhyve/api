from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, RegexHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram import Bot as tgBot
import shelve
import requests
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

IMAGE, VMNAME = range(2)

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


### Bot menus

def inline_keyboard():
    keyboard = [[InlineKeyboardButton('menu1', callback_data='vmcreate-debian')],
                [InlineKeyboardButton('menu2', callback_data='vmcreate-centos')]
                ]
    return InlineKeyboardMarkup(keyboard)


### DB ops

def writedata(uid, userdata):
    s = shelve.open('tg_users.db')
    try:
        s[str(uid)] = userdata
    finally:
        s.close()


def getdata(uid):
    s = shelve.open('tg_users.db')
    try:
        userdata = s[str(uid)]
    except KeyError:
        return 'nodata'
    finally:
        s.close()
    return userdata


def checkuser(uid):
    if getdata(uid) == 'nodata':
        emptydata = dict()
        writedata(uid, emptydata)
        return emptydata
    else:
        return getdata(uid)

### VM control


def create(update, context):
    userid = update.message.from_user.id
    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

    userdata = checkuser(userid)

    reply_keyboard = [['Debian', 'CentOS']]

    update.message.reply_text('Okay, select <b>image</b>! You can also /cancel', parse_mode=ParseMode.HTML,
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return IMAGE


def imageselect(update, context):
    userid = update.message.from_user.id
    update.message.reply_text('Okay, give a name for your ' + update.message.text + ' image',
                              reply_markup=ReplyKeyboardRemove())

    return VMNAME


def nameselect(update, context):
    userid = update.message.from_user.id
    update.message.reply_text('Okay, now we will create VM. Please, wait a bit!',
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def cancel(update, context):
    userid = update.message.from_user.id
    update.message.reply_text('Bye! Just type /create when you need VM',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


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


    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('create', create)],

        states={
            IMAGE: [MessageHandler(Filters.regex('^(Debian|CentOS)$'), imageselect)],

            VMNAME: [MessageHandler(Filters.text & ~Filters.command, nameselect)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)


    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('myid', myid))

    #updater.dispatcher.add_handler(CommandHandler('create', create))
    dp.add_handler(CommandHandler('destroy', destroy))
    dp.add_handler(CommandHandler('restart', restart))
    dp.add_handler(CommandHandler('list', listvms))

    #    usertext = MessageHandler(Filters.private, processtext)
    #    userphoto = MessageHandler(Filters.photo, processphoto)

    #    dispatcher.add_handler(usertext)
    #    dispatcher.add_handler(userphoto)


initbot()
updater.start_polling()
