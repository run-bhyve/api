import greenstalk
import json

client = greenstalk.Client(('10.0.0.1', 11300))
client.use('cbsd_zroot')

# Run any command on cluster
def send(cmd, params={}):
	real_cmd = {"Command": cmd, "CommandArgs": params}
	real_cmd = json.dumps(real_cmd)
	return real_cmd
	#return client.put(cmd)