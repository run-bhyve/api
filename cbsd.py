from helpers import hostcp, hostcmd
import greenstalk
import json

try:
	client = greenstalk.Client(('10.0.0.1', 11300))
	client.use('cbsd_zroot')
except Exception:
	True

def exec(subcmd, params):
	cmd = {"Command": subcmd, "CommandArgs": params}
	cmd = json.dumps(cmd)
	client.put(cmd)

# Create virtual machine with config `jconfig`
def bcreate(jconf):
	hostcp(jconf,'/tmp/vm.jconf')
	hostcmd('sudo cbsd bcreate jconf=/tmp/vm.jconf')

# Start virtual machine
def bstart(vm_name):
	hostcmd('sudo cbsd bstart ' + vm_name)

# Destroy virtual machine
def bremove(vm_name):
	hostcmd('sudo cbsd bremove ' + vm_name)

# Restart virtual machine
def brestart(vm_name):
	hostcmd('sudo cbsd brestart ' + vm_name)