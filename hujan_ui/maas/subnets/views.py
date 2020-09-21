import json
import sweetify
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from hujan_ui.maas.utils import MAAS
from hujan_ui import maas

from .forms import SubnetForm


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

    return redirect('maas:fabric:detail',fabric_id)
    # context = {}
    # return render(request, 'maas/subnets/fabric_detail.html', context)

@login_required
def vlan_detail(request, vlan_id):
    context = {}
    return render(request, 'maas/subnets/vlan_detail.html', context)

@login_required
def add(request):
    form = SubnetForm(request.POST or None)
    if form.is_valid():
        m = MAAS()
        data = form.clean()
        resp = m.post('subnets/',data=data)
        if resp.status_code in m.ok:
            sweetify.success(request, _('Subnet Added Successfully'), timer=2000)
        sweetify.warning(request, _(resp.text), timer=5000)
    context = {
        'title': 'Form Add Subnet',
        'form': form
    }
    return render(request, 'maas/subnets/add.html', context)

@login_required
def edit(request, subnet_id):
    subnets = maas.get_subnets()
    subnet = [s for s in subnets if s['id'] == subnet_id]
    print(subnet)
    form = SubnetForm(request.POST or None,initial=subnet[0])
    if form.is_valid():
        m = MAAS()
        data = form.clean()
        resp = m.put(f'subnets/{subnet_id}/',data=data)
        if resp.status_code in m.ok:
            sweetify.success(request,_('Subnet Update Successfully'), timer=2000)
        sweetify.warning(request, _(resp.text), timer=5000)
    
    context = {
        'title': 'Form Edit Subnet',
        'form': form
    }
    return render(request, 'maas/subnets/add.html', context)

@login_required
def delete(request, subnet_id):
    subnets = maas.get_subnets()
    subnet = [s for s in subnets if s['id'] == subnet_id]
    if subnet[0] != None:
        m = MAAS()
        resp = mass.delete(f'subnets/{subnet_id}/')
        if resp.status_code in m.ok:
            sweetify.success(request, _('Subnet Deleted Successfully'), timer=2000)
        sweetify.warning(request, _(resp.text), timer=5000)
    
    return redirect('maas:subnets:index')


    
