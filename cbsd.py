from helpers import scp, hostcmd

# Create virtual machine with config `jconfig`
def bcreate(jconf):
	hostcp(jconf,'/tmp/vm.jconf')
	hostcmd('sudo -u root cbsd bcreate jconf=/tmp/vm.jconf')

# Start virtual machine
def bstart(vm_name):
	hostcmd('sudo -u root cbsd bstart ' + vm_name)

# Destroy virtual machine
def bremove(vm_name):
	hostcmd('sudo -u root cbsd bremove ' + vm_name)

# Restart virtual machine
def brestart(vm_name):
	hostcmd('sudo -u root cbsd brestart ' + vm_name)
