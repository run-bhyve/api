from fastapi import FastAPI
from typing import Optional
import cbsd
from pydantic import BaseModel

app = FastAPI()

class VM(BaseModel):
    jname: Optional[str]
    vm_cpus: int
    vm_ram: int
    imgsize: int
    vm_os_profile: str

@app.post('/vps/')
def create_vps(vps: VM):
    return cbsd.bcreate(vps)

@app.delete('/vps/<vm_name>')
def destroy_vps(vm_name):
    return cbsd.bremove(vm_name)

@app.patch('/vps/<vm_name>/restart')
def restart_vps(vm_name):
    return cbsd.brestart(vm_name)