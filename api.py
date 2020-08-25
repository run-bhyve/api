from flask import Flask, jsonify
import os
import fileinput
from helpers import replace_in_file, hostcmd, hostreadcmd, scp, randstr
from shutil import copyfile as cp
import cbsd

app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.url_map.strict_slashes = False

@app.route('/create/<image>/<vm_name>')
def create_vps(image, vm_name):
    if image in ['debian', 'centos']:
        vm_ip4addr = hostreadcmd('sudo cbsd dhcpd')
        print(vm_ip4addr)

        vm_user_name = 'linux'
        vm_user_pwd = randstr()
        vm_root_pwd = randstr()

        jconf_template = '/root/api/jconfs/vm_linux.jconf'
        jconf_tmp = '/tmp/vm.jconf'

        cp(jconf_template, jconf_tmp)
        replace_in_file(jconf_tmp,'#IP',vm_ip4addr)
        replace_in_file(jconf_tmp,'#VMNAME',vm_name)
        replace_in_file(jconf_tmp,'#VMUSER',vm_user_name)
        replace_in_file(jconf_tmp,'#VMUPWD',vm_user_pwd)
        replace_in_file(jconf_tmp,'#VMRPWD',vm_root_pwd)

        if image == 'debian':
            replace_in_file(jconf_tmp,'#VMPROFILE','cloud-Debian-x86-10')
        elif image == 'centos':
            replace_in_file(jconf_tmp,'#VMPROFILE','cloud-CentOS-8.2-x86_64')

        # Create from *local* configuration file
        cbsd.bcreate('/tmp/vm.jconf')
        cbsd.bstart(vm_name)

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


@app.route('/destroy/<vm_name>')
def destroy_vps(vm_name):
    cbsd.bremove(vm_name)

    result = {
        "status": "ok"
    }

    return jsonify(result)


@app.route('/restart/<vm_name>')
def restart_vps(vm_name):
    cbsd.brestart(vm_name)

    result = {
        "status": "ok"
    }

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=False, port=8080)
