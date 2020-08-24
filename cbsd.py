from helpers import scp, hostcmd

def bcreate(jconf):
    scp('/tmp/vm.jconf','/home/eb/vm.jconf')
    hostcmd('sudo -u root cbsd bcreate jconf=/home/eb/vm.jconf')
def bstart(vm_name):
	hostcmd('sudo -u root cbsd bstart ' + vm_name)
def bremove(vm_name):
    hostcmd('sudo -u root cbsd bremove ' + vm_name)
def brestart(vm_name):
    hostcmd('sudo -u root cbsd brestart ' + vm_name)