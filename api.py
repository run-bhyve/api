from fastapi import FastAPI
from typing import Optional
import controller
from pydantic import BaseModel
from models import VM

app = FastAPI()

class VM(BaseModel):
    jname: Optional[str]
    vm_cpus: int
    vm_ram: int
    imgsize: int
    vm_os_profile: str

@app.post('/vm/')
def create_vm(vps: VM):
    return controller.bcreate(vps)

@app.delete('/vm/<jname>')
def destroy_vm(jname):
    return controller.bremove(jname)

@app.patch('/vm/<jname>/restart')
def restart_vm(jname):
    return controller.brestart(jname)