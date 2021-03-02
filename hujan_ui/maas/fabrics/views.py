import sweetify

from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, redirect
from django.http import JsonResponse
from hujan_ui import maas
from hujan_ui.maas.utils import MAAS
from .forms import FabricForm


def index(request):
    if request.is_ajax():
        return JsonResponse({'fabrics': maas.get_fabrics()})

    context = {
        'title': 'Fabrics',
        'fabrics': maas.get_fabrics(),
        'menus_active': 'fabrics_active'
    }
    return render(request, 'maas/fabrics/index.html', context)


def detail(request, fabric_id):
    fabrics = maas.get_fabrics(fabric_id)
    context = {
        'title': 'Fabric',
        'fabric': fabrics
    }
    return render(request, 'maas/fabrics/detail.html', context)


def add(request):
    form = FabricForm(request.POST or None)

    if form.is_valid():
        data = form.clean()
        m = MAAS()
        resp = m.post('fabrics/', data=data)
        if resp.status_code in m.ok:
            sweetify.success(request, _(
                'Successfully added fabric'), button='Ok', timer=2000)
            return redirect("maas:fabrics:index")
        sweetify.warning(request, _(resp.text), button='Ok', timer=5000)

    context = {
        'title': 'Add Fabric',
        'form': form,
    }
    return render(request, 'maas/fabrics/add.html', context)


def edit(request, fabric_id):
    fabrics = maas.get_fabrics(fabric_id)

    form = FabricForm(request.POST or None, initial=fabrics)
    if form.is_valid():
        m = MAAS()
        data = form.clean()
        data.update({'id': fabric_id})
        resp = m.put(f'/fabrics/{fabric_id}/', data=data)
        if resp.status_code in m.ok:
            sweetify.success(request, _('Successful'), button='OK', timer=2000)
            return redirect('maas:fabrics:index')
        sweetify.warning(request, _(resp.text), button='Ok', timer=5000)
    context = {
        'title': 'Edit Fabric',
        'form': form
    }
    return render(request, 'maas/fabrics/add.html', context)


def delete(request, fabric_id):
    fabrics = maas.get_fabrics(fabric_id)

    if not fabrics:
        sweetify.info(request, _('Data Fabric not Found...'), timer=5000)
        return redirect('maas:fabrics:index')
    m = MAAS()
    fabric_id = fabrics[0]['id']
    resp = m.delete(f'/fabrics/{fabric_id}/')
    if resp.status_code in m.ok:
        sweetify.success(request, _(
            'Data Successfully Deleted'), button='OK', timer=200)
        return redirect('maas:fabrics:index')
    sweetify.warning(request, 'Warning', text=_(resp.text), timer=5000)

    return redirect('maas:fabrics:index')
