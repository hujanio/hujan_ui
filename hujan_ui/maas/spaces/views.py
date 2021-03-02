import sweetify
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, redirect
from django.http import JsonResponse
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
        m = MAAS()
        resp = m.post('spaces/', data=data)
        if resp.status_code in m.ok:
            sweetify.success(request, _(
                'Spaces Successfully Added'), timer=2000)
        sweetify.warning(request, _(resp.text), timer=5000)
        return redirect('index')
    context = {
        'title': _('Form Space'),
        'form': form,
    }
    return render(request, 'maas/spaces/add.html', context)


def edit(request, space_id):
    spaces = maas.get_spaces(space_id)
    form = forms.SpacesForm(request.POST or None, initial=spaces)

    if form.is_valid():
        data = form.clean()
        m = MAAS()
        resp = m.put(f'/spaces/{space_id}/', data=data)
        if resp.status_code in m.ok:
            sweetify.success(request, _(
                'Space Successfully Updated'), timer=2000)
        sweetify.warning(request, _(resp.text), timer=5000)
        return redirect('maas:spaces:index')
    context = {
        'title': _('Edit Space'),
        'form': form
    }
    return render(request, 'maas/spaces/add.html', context)


def delete(request, space_id):
    spaces = maas.get_spaces(space_id)
    if not spaces:
        sweetify.warning(request, _('Data Space not Found..'), timer=5000)
        return redirect('maas.spaces.index')

    space_id = spaces[0]['id']
    m = MAAS()
    resp = m.delete(f'spaces/{space_id}/')
    if resp.status_code in m.ok:
        sweetify.success(request, _('Spaces Deteled Successfully'), timer=2000)
    sweetify.warning(request, _(resp.text), timer=5000)
    return redirect('maas:spaces:index')


def detail(request, space_id):
    spaces = maas.get_spaces(space_id)
    context = {
        'title': _('Detail Space'),
        'space': spaces,
        'subnets': maas.get_subnets()
    }
    return render(request, 'maas/spaces/detail.html', context)
