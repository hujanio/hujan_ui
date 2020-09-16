import json
from django.conf import settings
from .utils import MAAS


def get_machines():
    if settings.WITH_EX_RESPONSE:
        with open(settings.DIR_EX_RESPONSE + "machines.json") as readfile:
            machines = json.load(readfile)
    else:
        maas = MAAS()
        machines = maas.get("machines/").json()
        machine_file = open("hujan_ui/maas/ex_response/machines.json", "w")
        json.dump(machines, machine_file)
        machine_file.close()

    return machines

def get_subnets():
    if  settings.WITH_EX_RESPONSE:
        with open(settings.DIR_EX_RESPONSE + "subnets.json") as readfile:
            subnets = json.load(readfile)
    else:
        maas = MAAS()
        subnets = maas.get("subnets").json()
        subnet_file = open('hujan_ui/maas/ex_response/subnets.json','w')
        json.dump(subnets,subnet_file)
        subnet_file.close()
    return subnets
