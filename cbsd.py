import greenstalk
import json

try:
	client = greenstalk.Client(('10.0.0.1', 11300))
	client.use('cbsd_zroot')
except Exception:
	True

visual_params={"header":0}

# Run any command on cluster
def cbsd_exec(subcmd, params={}):
	if params.jname:
		# Operate only with VMs with prefix 'api_'
		params.jname = 'api_' + params.jname
	# Apply output format
	params.update(visual_params)
	cmd = {"Command": subcmd, "CommandArgs": params}
	cmd = json.dumps(cmd)
	return client.put(cmd)

# Get operation`s result
def get_result(id):
	True

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
