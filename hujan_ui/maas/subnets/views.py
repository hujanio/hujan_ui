import json
import sweetify

from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from hujan_ui.maas.utils import MAAS
from hujan_ui import maas


@login_required
def index(request):
    if request.is_ajax():
        return JsonResponse({'subnets': maas.get_subnets()})

    context = {
        'title': 'Subnets',
        'subnets': maas.get_subnets(),
        'menus_active': 'subnets_active'
    }
    return render(request, 'maas/subnets/index.html', context)

@login_required
def detail(request, subnet_id):
    if settings.WITH_EX_RESPONSE:
        with open(settings.DIR_EX_RESPONSE + "subnet_details.json") as readfile:
            subnet = json.load(readfile)
    else:
        maas = MAAS()
        respose = maas.get(f"subnets/{subnet_id}/")
        if respose.ok:
            subnet = respose.json()
        else:
            subnet = []

    if request.is_ajax():
        return JsonResponse({'subnet': subnet})

    context = {
        'title': f"Subnet - {subnet['name']}",
        'subnet': subnet,
        'menu_active': 'subnets',
    }
    return render(request, 'maas/subnets/subnet_detail.html', context)

@login_required
def fabric_detail(request, fabric_id):
    context = {}
    return render(request, 'maas/subnets/fabric_detail.html', context)

@login_required
def vlan_detail(request, vlan_id):
    context = {}
    return render(request, 'maas/subnets/vlan_detail.html', context)

@login_required
def add(request):
    context = {}
    return render(request, 'maas/subnets/add.html', context)
