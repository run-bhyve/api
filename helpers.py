import os
import fileinput
import uuid

def hostcmd(cmd):
	os.system('ssh ' + os.environ['HOST_USER'] + '@' + os.environ['HOST_SERV'] + ' ' + cmd)

def scp(orig,dest):
	os.system('scp ' + orig + ' ' + os.environ['HOST_USER'] + '@' + os.environ['HOST_SERV'] + ':' + dest)

def hostreadcmd(cmd):
	return os.popen('ssh ' + os.environ['HOST_USER'] + '@' + os.environ['HOST_SERV'] + ' ' + cmd).read().rstrip()

def replace_in_file(jconf_tmp,what,to):
    with fileinput.FileInput(jconf_tmp, inplace=True) as file:
    for line in file:
        print(line.replace(what, to), end='')

def randstr(string_length=10):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4())
    random = random.replace("-","")
    return random[0:string_length]