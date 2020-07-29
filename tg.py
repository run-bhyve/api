from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, RegexHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, ReplyKeyboardRemove
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

def vmimage_keyboard():
    keyboard = [[InlineKeyboardButton('Debian', callback_data='vmcreate-debian')],
                [InlineKeyboardButton('Centos', callback_data='vmcreate-centos')]
                ]
    return InlineKeyboardMarkup(keyboard)


### DB ops

def writedata(uid, userdata):
    s = shelve.open('tg_users.db')
    try:
        s[uid] = userdata
    finally:
        s.close()


def getdata(uid):
    s = shelve.open('tg_users.db')
    try:
        userdata = s[uid]
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

def create(bot, update):
    userid = update.message.from_user.id
    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

    userdata = checkuser(userid)
    update.message.reply_text('Okay, select <b>image</b>!', parse_mode=ParseMode.HTML,
                              reply_markup=vmimage_keyboard())

    return IMAGE


def vmname(update, context):
    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('I see! Please send me a photo of yourself, '
                              'so I know what you look like, or send /skip if you don\'t want to.',
                              reply_markup=ReplyKeyboardRemove())

    return PHOTO


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

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('create', create)],

        states={
            IMAGE: [MessageHandler(Filters.regex('^(Boy|Girl|Other)$'), gender)],

            NAME: [MessageHandler(Filters.photo, photo),
                    CommandHandler('skip', skip_photo)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('myid', myid))

    #updater.dispatcher.add_handler(CommandHandler('create', create))
    updater.dispatcher.add_handler(CommandHandler('destroy', destroy))
    updater.dispatcher.add_handler(CommandHandler('restart', restart))
    updater.dispatcher.add_handler(CommandHandler('list', listvms))


    dispatcher.add_handler(usertext)
    dispatcher.add_handler(userphoto)


initbot()
updater.start_polling()
