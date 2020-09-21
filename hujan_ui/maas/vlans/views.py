from django.shortcuts import render, redirect
from hujan_ui import maas

def index(request):
    context = {
        'title': 'Vlan List',
        'vlans': maas.get_vlan()

    }
    return render(request, 'maas/vlans/index.html', context)

def add(request):
    pass

def edit(request):
    pass

def detail(request, vlan_id):
    vlan = maas.get_vlan(vlan_id)
    context = {
        'vlan': vlan
    }
    return render(request, 'maas/vlans/detail.html', context)
    
def delete(request, vlan_id):
    pass