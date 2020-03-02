import requests
import json

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from hujan_ui.maas.utils import maas_connect


@login_required
def machines(request):
    if settings.WITH_EX_RESPONSE:
        with open(settings.DIR_EX_RESPONSE + "machines.json") as readfile:
            machines = json.load(readfile)
    else:
        auth = maas_connect()
        headers = {'content-type': 'application/json', 'accept': 'application/json'}
        res = requests.get(settings.MAAS_URL + "api/2.0/machines/", headers=headers, auth=auth)
        machines = res.json()

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
        auth = maas_connect()
        headers = {'content-type': 'application/json', 'accept': 'application/json'}
        res = requests.get(settings.MAAS_URL + f"api/2.0/machines/{system_id}/", headers=headers, auth=auth)
        machine = res.json()

    context = {
        'title': f"Machines - {machine['fqdn']}",
        'machine': machine,
        'menu_active': 'machines',
    }
    return render(request, 'maas/machine_details.html', context)
