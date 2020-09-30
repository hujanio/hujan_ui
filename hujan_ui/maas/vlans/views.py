from django.shortcuts import render, redirect
from hujan_ui import maas
from hujan_ui.maas.utils import MAAS
from .forms import VlanForm, VlanEditForm
from django.utils.translation import ugettext_lazy as _

import sweetify

def index(request):
    context = {
        'title': 'Vlan List',
        'vlans': maas.get_vlans()

    }
    return render(request, 'maas/vlans/index.html', context)


def add(request):
    form = VlanForm(request.POST or None)

    if form.is_valid():
        m = MAAS()
        data = form.clean()
        fabId = data['fabric_id']
        resp = m.post(f'fabrics/{fabId}/vlans/', data=data)
        if resp.status_code in m.ok:
            sweetify.success(request, _('Vlan Added Successful'), timer=3000)
            return redirect('maas:subnets:index')
        sweetify.warning(request, _(resp.text), timer=5000)
        
    context = {
        'title': 'Add Vlan',
        'form': form
    }

    return render(request, 'maas/vlans/add.html', context)


def edit(request, vlan_id):
    vlan = maas.get_vlans(vlan_id)
    form = VlanEditForm(request.POST or None, initial=vlan)
    if form.is_valid():
        m = MAAS()
        data = form.clean()
        fabId = data['fabric_id']
        vid = data['vid']
        resp = m.put(f'fabrics/{fabId}/vlans/{vid}/',data=data)
        if resp.status_code in m.ok:
            sweetify.success(request, _('Vlan Updated Successful'), timer=3000)
            return redirect('maas:subnets:index')
        sweetify.warning(request, _(resp.text), timer=5000)
        
    context = {
        'title': 'Edit Vlan',
        'form': form
    }

    return render(request, 'maas/vlans/add.html', context)


def detail(request, vlan_id):
    vlan = maas.get_vlans(vlan_id)
    if vlan:   
        context = {
            'title': 'Detail Vlan - {}'.format(vlan['fabric']),
            'vlan': vlan
        }
        return render(request, 'maas/vlans/detail.html', context)

    return redirect('maas:vlans:index')


def delete(request, vlan_id):
    vlan = maas.get_vlans(vlan_id)
    fid = vlan['fabric_id']
    vid = vlan['vid']
    m = MAAS()
    resp = m.delete(f'fabrics/{fid}/vlans/{vid}/')
    if resp.status_code in m.ok:
        sweetify.success(request, _('Vlan Deleted Successful'), timer=5000)
        return redirect('maas:subnets:index')
    return redirect('maas:subnets:index')

    

