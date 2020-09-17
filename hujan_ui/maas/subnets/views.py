import json
import sweetify

from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from hujan_ui.maas.utils import MAAS
from hujan_ui import maas


@login_required
def index(req):
    if req.is_ajax():
        return JsonResponse({'subnets': maas.get_subnets()})

    ctx = {
        'title': 'Subnets',
        'subnets': maas.get_subnets(),
        'menus_active': 'subnets_active'
    }
    tpl = 'maas/subnets/index.html'
    return render(req, tpl, ctx)


def detail(req, *args, **kwargs):
    tpl = 'maas/subnets/subnet_detail.html'
    if settings.WITH_EX_RESPONSE:
        with open(settings.DIR_EX_RESPONSE + "subnet_details.json") as readfile:
            subnets = json.load(readfile)
    else:
        maas = MAAS()
        subnets = maas.get(f"subnets/{kwargs['subnet_id']}/").json()

    if req.is_ajax():
        return JsonResponse({'subnet': subnets})

    ctx = {
        'title': f"Subnet - {subnets['name']}",
        'subnets': subnets,
        'menu_active': 'machines',
    }
    return render(req, tpl, ctx)


def fabric_detail(req,*args, **kwargs):
    tpl = 'maas/subnets/fabric_detail.html'
    return render(req, tpl, {})


def vlan_detail(req,*args, **kwargs):
    tpl = 'maas/subnets/vlan_detail.html'
    return render(req, tpl, {})


def add(req):
    tpl = 'maas/subnets/add.html'

    return render(req, tpl, {})
