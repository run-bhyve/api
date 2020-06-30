import telegram

from flask import Flask, jsonify
import requests
import sys
import configparser
import threading
import time
import os
import datetime

app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.url_map.strict_slashes = False

teletoken=os.environ['TELETOKEN']


def sendAdmin(msg):
    admin_chat = '131719022'
    bot = telegram.Bot(teletoken)
    bot.send_message(chat_id=admin_chat, text='swapBot: ' + msg)


@app.route('/create/<image>')
def create_vps(image):
    if image in ['debian', 'centos', 'ubuntu', 'bitcoind', 'lightningd', 'rootshell', 'vpn', 'pay2exec']:

        os.system('ssh eb@10.0.0.15 sudo -u root cbsd bcreate jconf=/usr/jails/ftmp/vm.28426.jconf')

        result = {
            "host": 'test',
            "image": image
        }

        return jsonify(result)
    else:
        return {'error': 'no such image'}


@app.route('/destroy')
def destroy_vps():
    os.system('ssh eb@10.0.0.15 sudo -u root cbsd bremove vm')


if __name__ == '__main__':
    app.run(debug=False, port=8080)