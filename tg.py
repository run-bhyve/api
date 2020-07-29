from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, RegexHandler, ConversationHandler, CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram import Bot as tgBot
import shelve
import requests
import datetime
import os
import re
import json

import logging

teletoken = os.environ['TELETOKEN']

updater = Updater(teletoken, use_context=True)
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


def start(update, context):
    userid = update.message.from_user.id
    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    print(dtime + " - " +str(userid) + ' started TG bot')


def myid(update, context):
    userid = update.message.from_user.id
    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    update.message.reply_text('Your Telegram ID is: ' + str(userid))
    print(dtime + " - " +str(userid) + ' asked for id')


def processphoto(update, context):
    userid = update.message.from_user.id
    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    update.message.reply_text('received image!')
    print(dtime + " - " + str(userid) + ' sent photo to bot')


def processtext(update, context):
    userid = update.message.from_user.id
    text = update.message.text
    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    update.message.reply_text('Greetings! This bot is alive!')
    print(dtime + " - " + str(userid) + ' sent text message:\n' + str(text))


def cmd_restart(bot, update):
    query = update.callback_query
    userid = query.message.chat_id  # need to reset previous selections

    responsedata = query['data']
    m = re.search('restart-([a-z0-9]+)', responsedata)
    jname = m.group(1)

    response = requests.get('http://' + os.environ['HOST_API'] + ':8080/restart/' + jname)
    sendTele(userid, response.json())


def cmd_destroy(bot, update):
    query = update.callback_query
    userid = query.message.chat_id  # need to reset previous selections

    responsedata = query['data']
    m = re.search('destroy-([a-z0-9]+)', responsedata)
    jname = m.group(1)
    response = requests.get('http://' + os.environ['HOST_API'] + ':8080/restart/' + jname)
    sendTele(userid, response.json())


def cmd_getinfo(bot, update):
    query = update.callback_query
    userid = query.message.chat_id  # need to reset previous selections

    responsedata = query['data']
    m = re.search('machine-([a-z0-9]+)', responsedata)
    jname = m.group(1)

    userdata = checkuser(userid)

    for vm in userdata['machines']:
        if vm['jname'] == jname:
            sendTele(userid, str(vm))


### Bot menus
def machine_keyboard(uid):
    keyboard = list()
    userdata = getdata(uid)

    for vm in userdata['machines']:
        keyboard.append([InlineKeyboardButton(vm['name'], callback_data='machine-'+str(vm['jname']))])

    return InlineKeyboardMarkup(keyboard)


def restart_keyboard(uid):
    keyboard = list()
    userdata = getdata(uid)

    for vm in userdata['machines']:
        keyboard.append([InlineKeyboardButton(vm['name'], callback_data='reset-'+str(vm['jname']))])

    return InlineKeyboardMarkup(keyboard)


def destroy_keyboard(uid):
    keyboard = list()
    userdata = getdata(uid)

    for vm in userdata['machines']:
        keyboard.append([InlineKeyboardButton(vm['name'], callback_data='destroy-'+str(vm['jname']))])

    return InlineKeyboardMarkup(keyboard)



### DB ops

def writedata(uid, userdata):
    s = shelve.open('tg_users')
    try:
        s[str(uid)] = userdata
    finally:
        s.close()


def getdata(uid):
    s = shelve.open('tg_users')
    try:
        userdata = s[str(uid)]
    except KeyError:
        return 'nodata'
    finally:
        s.close()
    return userdata


def checkuser(uid):
    if getdata(uid) == 'nodata':
        emptydata = {"machines": list()}
        writedata(uid, emptydata)
        return emptydata
    else:
        return getdata(uid)

### VM control


def create(update, context):

    userid = update.message.chat.id

    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

    userdata = checkuser(userid)

    reply_keyboard = [['Debian', 'CentOS']]

    update.message.reply_text('Okay, select <b>image</b>! You can also /cancel', parse_mode=ParseMode.HTML,
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))


    return IMAGE


def imageselect(update, context):
    userid = update.message.chat.id
    update.message.reply_text('Okay, give a name for your ' + update.message.text + ' image',
                              reply_markup=ReplyKeyboardRemove())


    context.user_data['image'] = update.message.text

    return VMNAME


def nameselect(update, context):
    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

    userid = update.message.chat.id
    update.message.reply_text('Okay, now we will create VM. Please, wait a bit!',
                              reply_markup=ReplyKeyboardRemove())
    context.user_data['vmmame'] = update.message.text
    vmimage = str(context.user_data['image']).lower()
    jname = 'tg' + str(userid) + '_' + (context.user_data['vmmame']).lower()
    response = requests.get('http://' + os.environ['HOST_API'] + ':8080/create/' + vmimage + '/' + jname)
    vmdata = response.json()
    vmdata['timestamp'] = dtime
    vmdata['jname'] = dtime
    userdata = checkuser(userid)
    userdata['machines'].append(vmdata)
    writedata(userid, userdata)
    sendTele(userid, str(vmdata))
    return ConversationHandler.END


def cancel(update, context):
    userid = update.message.chat.id
    update.message.reply_text('Bye! Just type /create when you need VM',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def destroy(update, context):
    userid = update.message.from_user.id
    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')


def restart(update, context):
    userid = update.message.from_user.id
    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

    userdata = checkuser(userid)


def listvms(update, context):
    userid = update.message.from_user.id
    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    userdata = checkuser(userid)
    try:
        if not userdata['machines']:
            sendTele(userid, "You have no machines")
        else:
            sendTele(userid, str(userdata['machines']))
            update.message.reply_text('Your VMs',
                                      reply_markup=machine_keyboard(userid))
    except KeyError:
        sendTele(userid, "KeyError!")


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

    dp.add_handler(CallbackQueryHandler(cmd_restart, pattern='restart-'))
    dp.add_handler(CallbackQueryHandler(cmd_getinfo, pattern='machine-'))
    dp.add_handler(CallbackQueryHandler(cmd_destroy, pattern='destroy-'))

    #    usertext = MessageHandler(Filters.private, processtext)
    #    userphoto = MessageHandler(Filters.photo, processphoto)

    #    dispatcher.add_handler(usertext)
    #    dispatcher.add_handler(userphoto)


initbot()
updater.start_polling()
