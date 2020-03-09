import requests
import json

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from hujan_ui.maas.utils import MAAS


@login_required
def machines(request):
    if settings.WITH_EX_RESPONSE:
        with open(settings.DIR_EX_RESPONSE + "machines.json") as readfile:
            machines = json.load(readfile)
    else:
        maas = MAAS()
        machines = maas.get("machines/").json()
        machine_file = open("hujan_ui/maas/ex_response/machines.json", "w")
        json.dump(machines, machine_file)
        machine_file.close()

    context = {
        'title': 'Machines',
        'machines': machines,
        'menu_active': 'machines',
    }
    return render(request, 'maas/machines.html', context)


@login_required
def machine_details(request, system_id):
    if settings.WITH_EX_RESPONSE:
        with open(settings.DIR_EX_RESPONSE + "machine_details.json") as readfile:
            machine = json.load(readfile)
    else:
        maas = MAAS()
        machine = maas.get(f"machines/{system_id}/").json()

    context = {
        'title': f"Machines - {machine['fqdn']}",
        'machine': machine,
        'menu_active': 'machines',
    }
    return render(request, 'maas/machine_details.html', context)
