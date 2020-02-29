import requests

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from hujan_ui.maas.utils import maas_connect


@login_required
def machines(request):
    auth = maas_connect()
    headers = {'content-type': 'application/json', 'accept': 'application/json'}
    res = requests.get(settings.MAAS_URL + "api/2.0/machines/", headers=headers, auth=auth)
    context = {
        'title': 'Machines',
        'machines': res.json(),
        'menu_active': 'machines',
    }
    return render(request, 'maas/machines.html', context)
