import greenstalk
import json

try:
	client = greenstalk.Client(('10.0.0.1', 11300))
	client.use('cbsd_zroot')
except Exception:
	True

# Run any command on cluster
def cbsd_exec(subcmd, params={}):
	if (params.jname) {
		params.jname = 'api_' + params.jname
	}
	cmd = {"Command": subcmd, "CommandArgs": params}
	cmd = json.dumps(cmd)
	client.put(cmd)

# Create virtual machine
def bcreate(jconf):
	cbsd_exec('bcreate', jconf)

# Start virtual machine
def bstart(jname):
	cbsd_exec('bstart', {"jname"=jname})

# Destroy virtual machine
def bremove(jname):
	cbsd_exec('bstart', {"jname"=jname})

# Restart virtual machine
def brestart(jname):
	cbsd_exec('brestart', {"jname"=jname})
