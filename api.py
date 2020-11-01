from flask import render_template
from fastapi import FastAPI
from helpers import hostreadcmd, randstr
import cbsd
from pydantic import BaseModel


app = FastAPI()

class VPS(BaseModel):
    name: str
    price: float
    cpu: int
    ram: int
    drive: int
    profile: str

@app.post('/vps/')
def create_vps(vps: VPS):
    if vps.profile in ['debian', 'centos']:
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
        return conf
    else:
        return {'error': 'no such image'}

@app.delete('/vps/<vm_name>')
def destroy_vps(vm_name):
    cbsd.bremove(vm_name)
    return {"status": "ok"}

@app.patch('/vps/<vm_name>/restart')
def restart_vps(vm_name):
    cbsd.brestart(vm_name)
    return {"status": "ok"}