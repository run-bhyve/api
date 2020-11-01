from models import VM

# Create virtual machine
def create_vm(config):
	# Создать объект ВМ (автоматически присваивается GID)
	vm = VM(config)
	# Определить, где можно разместить данную машину
	# И создать ее 
	return vm.create()

# Start virtual machine
def start_vm(gid):
	# Получить объект машины по gid
	vm = VM.objects.get(gid)
	return vm.start()

# Restart virtual machine
def restart_vm(gid):
	vm = VM.objects.get(gid)
	return vm.restart()

# Destroy virtual machine
def destroy_vm(gid):
	vm = VM.objects.get(gid)
	return vm.delete()