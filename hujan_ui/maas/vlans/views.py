from django.shortcuts import render, redirect
from hujan_ui import maas
from django.http import HttpResponseNotFound

def index(request):
    context = {
        'title': 'Vlan List',
        'vlans': maas.get_vlans()

    }
    return render(request, 'maas/vlans/index.html', context)

def add(request):
    pass

def edit(request, vlan_id):
    return HttpResponseNotFound()

def detail(request, vlan_id):

    vlan = maas.get_vlans(vlan_id)
    print(vlan)
    if vlan:   
        context = {
            'title': 'Detail Vlan - {}'.format(vlan['fabric']),
            'vlan': vlan
        }
        return render(request, 'maas/vlans/detail.html', context)
    return redirect('maas:vlans:index')
    
def delete(request, vlan_id):
    return redirect('maas:vlans:index')