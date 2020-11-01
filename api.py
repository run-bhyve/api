from fastapi import FastAPI
import controller
from models import VM

app = FastAPI()

@app.post('/vm/')
def create_vm(config: VM):
    return controller.create_vm(config)

@app.delete('/vm/<jname>')
def destroy_vm(gid):
    return controller.destroy_vm(jname)

@app.patch('/vm/<jname>/restart')
def restart_vm(gid):
    return controller.restart_vm(jname)