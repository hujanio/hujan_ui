import sweetify


from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, redirect
from hujan_ui import maas
from hujan_ui.maas.utils import MAAS
from . import forms

def index(request):
    if request.is_ajax():
        return JsonResponse({'spaces': maas.get_spaces()})

    context = {
        'title': 'Spaces',
        'spaces': maas.get_spaces(),
        'menus_active': 'spaces_active'
    }
    return render(request, 'maas/spaces/index.html', context)

def add(request):
    form = forms.SpacesForm(request.POST or None)
    if form.is_valid():
        data = form.clean()
        maas = MAAS()
        resp = maas.post('spaces/',data=data)
        if resp.status_code in maas.ok:
            sweetify.success(request, _('Spaces Successfully Added'), timer=2000)
        sweetify.warning(request, _(resp.text), timer=5000)
        return redirect('maas.spaces.index')
    context = {
        'title': 'Form Space'
        'form': form,
    }
    return render(request, 'maas/spaces/add.html', )

def edit(request, space_id):
    spaces = maas.get_spaces()
    space = [s for s in space_id if s['id'] == space_id]
    form = forms.SpacesForm(request.POST or None,initial=space[0])

    if form.is_valid():
        data = form.clean()
        maas = MAAS()
        resp = maas.put(f'/spaces/{space_id}/',data=data)
        if resp.status_code in maas.ok:
            sweetify.success(request, _('Space Successfully Updated'), timer=2000)
        sweetify.warning(request, _(resp.text), timer=5000)
        return redirect('maas.spaces.index')
    context = {
        'title': 'Edit Space',
        'form': form
    }
    return render(request, 'maas/space/add.html', context)


def delete(request, space_id):
    spaces = maas.get_spaces()
    space = [s for s in space_id if s['id'] == space_id] 
    maas = MAAS()
    resp = maas.delete(f'spaces/{space_id}/')
    if resp.status_code in maas.ok:
        sweetify.success(request, _('Spaces Deteled Successfully'), timer=2000)
    sweetify.warning(request, _(resp.text), timer=5000)

    return redirect('maas.spaces.index')
    

def detail(request, space_id):
    spaces = maas.get_spaces()
    space = [s for s in space_id if s['id'] == space_id] 
    context = {
        'title': 'Detail Space',
        'space': space,
    }
    return render(request, 'maas/space/detail.html', context)

        