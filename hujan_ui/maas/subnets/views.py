import json
import sweetify
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from hujan_ui.maas.utils import MAAS
from hujan_ui import maas
from .forms import SubnetForm, SubnetAddForm


@login_required
def index(request):
    if request.is_ajax():
        return JsonResponse({'subnets': maas.get_subnets()})

    context = {
        'title': 'Subnets',
        'subnets': maas.get_subnets(),
        'fabrics': maas.get_fabrics(),
        'spaces': maas.get_spaces(),
        'group_subnet': maas.get_subnet_infabric(),
        'menus_active': 'subnets_active'
    }
    return render(request, 'maas/subnets/index.html', context)


@login_required
def detail(request, subnet_id):
    
    subnet = maas.get_subnets(subnet_id)
    # unr = maas.get_subnets(subnet_id,op='unreserved_ip_ranges')
    # stat = maas.get_subnets(subnet_id,op='statistics')
    # TODO untuk data unreserved dan statistic masih belum sesuai antara api dan maas yang ada 
    rir = maas.get_subnets(subnet_id,op='reserved_ip_ranges')

    if request.is_ajax():
        return JsonResponse({'subnet': subnet})

    context = {
        'title': f"Subnet - {subnet['name']}",
        'subnet': subnet,
        # 'unr': unr,
        # 'stat': stat,
        # TODO untuk data unreserved dan statistic masih belum sesuai antara api dan maas yang ada 
        'rir': rir,
        'menu_active': 'subnets',
    }
    return render(request, 'maas/subnets/subnet_detail.html', context)


@login_required
def add(request):
    form = SubnetAddForm(request.POST or None)
    if form.is_valid():
        m = MAAS()
        data = form.clean()
        resp = m.post('subnets/', data=data)
        if resp.status_code in m.ok:
            sweetify.success(request, _('Subnet Added Successfully'), timer=2000)
            return redirect('maas:subnets:index')
        sweetify.warning(request, _(resp.text), timer=5000)
    context = {
        'title': 'Form Add Subnet',
        'form': form
    }
    return render(request, 'maas/subnets/add.html', context)


@login_required
def edit(request, subnet_id):
    subnet = maas.get_subnets(subnet_id)
    if not subnet:
        return redirect('maas:subnets:index')
    form = SubnetForm(request.POST or None, initial=subnet)
    if form.is_valid():
        m = MAAS()
        data = form.clean()
        if data['vlan']:
            vl = maas.get_vlans(int(data['vlan']))
            data['vid'] =  vl['vid']
            data['fabric'] = vl['fabric_id'] 
        
        resp = m.put(f'subnets/{subnet_id}/', data=data)
        if resp.status_code in m.ok:
            sweetify.success(request, _('Subnet Update Successfully'), timer=2000)
            return redirect('maas:subnets:index')
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
        resp = m.delete(f'subnets/{subnet_id}/')
        if resp.status_code in m.ok:
            sweetify.success(request, _('Subnet Deleted Successfully'), timer=2000)
            return redirect('maas:subnets:index')
        sweetify.warning(request, _(resp.text), timer=5000)
    
    return redirect('maas:subnets:index')


    
