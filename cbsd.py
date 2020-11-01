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
	cmd = {"Command": subcmd, "CommandArgs": params}
	cmd = json.dumps(cmd)
	return cmd
	#return client.put(cmd)

# Create virtual machine
def bcreate(conf):
	conf = conf.dict()
	return cbsd_exec('bcreate', conf)

# Start virtual machine
def bstart(jname):
	return cbsd_exec('bstart', {"jname": jname})

# Restart virtual machine
def brestart(jname):
	cbsd_exec('brestart', {"jname": jname})

# Destroy virtual machine
def bremove(jname):
	return cbsd_exec('bremove', {"jname": jname})