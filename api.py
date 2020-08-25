from flask import Flask, jsonify, render_template
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

        jconf_template = 'vm_linux.jconf'
        jconf_tmp = '/tmp/vm.jconf'

        if image == 'debian':
            vm_profile = 'cloud-Debian-x86-10'
        elif image == 'centos':
            vm_profile = 'cloud-CentOS-8.2-x86_64'

        conf = {
            'vm_name': vm_name,
            'ip': vm_ip4addr,
            'vm_user_name': 'linux',
            'vm_user_pwd': randstr(),
            'vm_root_pwd': randstr(),
            'vm_profile': vm_profile,
        }

        with open(jconf_tmp, "w") as f:
            f.write(render_template(jconf_template,**conf))


        # Create from *local* configuration file
        cbsd.bcreate(jconf_tmp)
        cbsd.bstart(vm_name)

        return jsonify(conf)
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
