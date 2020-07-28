from flask import Flask, jsonify
import requests
import sys
import configparser
import threading
import time
import os
import datetime
from tg import sendTele

app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.url_map.strict_slashes = False

teletoken=os.environ['TELETOKEN']


def sendAdmin(msg):
    admin_chat = os.environ['TELETOKEN']
    sendTele(admin_chat, msg)

@app.route('/create/<image>')
def create_vps(image):
    if image in ['linux']:
        os.system('ssh eb@' + os.environ['HOST_SERV'] + ' sudo -u root cbsd bcreate jconf=/usr/jails/ftmp/vm.jconf')

        result = {
            "host": 'test',
            "image": image
        }

        return jsonify(result)
    else:
        return {'error': 'no such image'}


@app.route('/destroy')
def destroy_vps():
    os.system('ssh eb@' + os.environ['HOST_SERV'] + ' sudo -u root cbsd bremove vm')


if __name__ == '__main__':
    app.run(debug=False, port=8080)