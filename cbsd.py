from helpers import hostcp, hostcmd
import sqlite3

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

# Get list of nodes
# https://docs.python.org/2/library/sqlite3.html
def get_nodes():
	conn = sqlite3.connect('/db/nodes.sqlite')
	c = conn.cursor()
	c.execute("SELECT * FROM nodelist")
	return c