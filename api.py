from flask import Flask, jsonify
import os
import fileinput
import uuid
from tg import sendTele

app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.url_map.strict_slashes = False

teletoken=os.environ['TELETOKEN']


def sendAdmin(msg):
    admin_chat = os.environ['TELETOKEN']
    sendTele(admin_chat, msg)


def randstr(string_length=10):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4())
    random = random.replace("-","")
    return random[0:string_length]


@app.route('/create/<image>/<vmname>')
def create_vps(image, vmname):
    if image in ['linux']:
        vm_ip4addr = os.popen('ssh eb@' + os.environ['HOST_SERV'] + ' sudo cbsd dhcpd').read().rstrip()
        print(vm_ip4addr)
        vm_name = vmname

        vm_user_name = 'linux'
        vm_user_pwd = randstr()
        vm_root_pwd = randstr()

        jconf_template = '/root/api/jconfs/vm_linux.jconf'
        jconf_tmp = '/tmp/vm.jconf'

        os.system('cp ' + jconf_template + ' ' + jconf_tmp)

        with fileinput.FileInput(jconf_tmp, inplace=True) as file:
            for line in file:
                print(line.replace('#IP', vm_ip4addr), end='')

        with fileinput.FileInput(jconf_tmp, inplace=True) as file:
            for line in file:
                print(line.replace('#VMNAME', vm_name), end='')

        with fileinput.FileInput(jconf_tmp, inplace=True) as file:
            for line in file:
                print(line.replace('#VMUSER', vm_user_name), end='')

        with fileinput.FileInput(jconf_tmp, inplace=True) as file:
            for line in file:
                print(line.replace('#VMUPWD', vm_user_pwd), end='')

        with fileinput.FileInput(jconf_tmp, inplace=True) as file:
            for line in file:
                print(line.replace('#VMRPWD', vm_root_pwd), end='')

        os.system('scp /tmp/vm.jconf eb@' + os.environ['HOST_SERV'] + ':/home/eb/vm.jconf')
        os.system('ssh eb@' + os.environ['HOST_SERV'] + ' sudo -u root cbsd bcreate jconf=/home/eb/vm.jconf')
        os.system('ssh eb@' + os.environ['HOST_SERV'] + ' sudo -u root cbsd bstart ' + vm_name)

        result = {
            "name": vm_name,
            "ip": vm_ip4addr,
            "user": vm_user_name,
            "root_pwd": vm_root_pwd,
            "user_pwd": vm_user_pwd
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