from flask import Flask, jsonify
import os
import fileinput

from tg import sendTele

app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.url_map.strict_slashes = False

teletoken=os.environ['TELETOKEN']


def sendAdmin(msg):
    admin_chat = os.environ['TELETOKEN']
    sendTele(admin_chat, msg)


@app.route('/create/<image>/<vmname>')
def create_vps(image, vmname):
    if image in ['linux']:
        vm_ip4addr = os.popen('ssh eb@' + os.environ['HOST_SERV'] + ' sudo cbsd dhcpd').read().rstrip()
        print(vm_ip4addr)
        vm_name = vmname

        jconf_template = '/root/api/jconfs/vm_linux.jconf'
        jconf_tmp = '/tmp/vm.jconf'

        os.system('cp ' + jconf_template + ' ' + jconf_tmp)

        with fileinput.FileInput(jconf_tmp, inplace=True) as file:
            for line in file:
                print(line.replace('#IP', vm_ip4addr), end='')

        with fileinput.FileInput(jconf_tmp, inplace=True) as file:
            for line in file:
                print(line.replace('dumb_linux', vm_name), end='')

        os.system('scp /tmp/vm.jconf eb@' + os.environ['HOST_SERV'] + ':/home/eb/vm.jconf')
        os.system('ssh eb@' + os.environ['HOST_SERV'] + ' sudo -u root cbsd bcreate jconf=/home/eb/vm.jconf')

        result = {
            "name": vm_name,
            "ip": vm_ip4addr
        }

        return jsonify(result)
    else:
        return {'error': 'no such image'}


@app.route('/destroy/<vmname>')
def destroy_vps(vmname):
    os.system('ssh eb@' + os.environ['HOST_SERV'] + ' sudo -u root cbsd bremove ' + vmname)

    result = {
        "status": "ok"
    }

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=False, port=8080)