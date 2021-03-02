from hujan_ui.maas import load_document
from hujan_ui.maas.exceptions import MAASError
import requests
import json
import sweetify

from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from hujan_ui.maas.utils import MAAS
from .forms import AddDomainForm, EditDomainForm


@login_required
def index(request):
    try:
        if settings.WITH_EX_RESPONSE:
            domains = load_document('domains.json')
        else:
            maas = MAAS()
            domains = maas.get("domains/").json()
            machine_file = open("hujan_ui/maas/ex_response/domains.json", "w")
            json.dump(domains, machine_file)
            machine_file.close()
        
        context = {
            'title': 'DNS',
            'domains': domains,
            'menu_active': 'domains',
        }
    except (MAASError) as e:
        sweetify.sweetalert(request, 'Warning', text=str(e), button='OK', timer=5000)
        context = None

    return render(request, 'maas/dns/index.html', context)


@login_required
def add(request):
    form = AddDomainForm(request.POST or None)
    if form.is_valid():
        try:
            resp = form.save()
            if resp.status_code == requests.codes.ok:
                sweetify.success(request, _('Successfully added domain'), button='Ok', timer=2000)
                return redirect("maas:dns:index")
            sweetify.warning(request, _('Terjadi suatu kesalahan'), button='Ok', timer=2000)
        except (MAASError) as e:
            sweetify.sweetalert(request, 'Warning', text=str(e), button='Ok', timer=5000)

    context = {
        'title': 'Add Domain',
        'menu_active': 'domains',
        'form': form,
        'title_submit': 'Save Domain',
        'col_size': '4'
    }
    return render(request, 'maas/form.html', context)


@login_required
def edit(request, id):
    try:
        maas = MAAS()
        domain = maas.get(f"domains/{id}/").json()
        form = EditDomainForm(request.POST or None, initial=domain)
        if form.is_valid():        
            resp = form.save(domain['id'])
            if resp.status_code in maas.ok:
                sweetify.success(request, _('Successfully edited domain'), button='Ok', timer=2000)
                return redirect("maas:dns:index")
            sweetify.warning(request, _(resp.text), button='Ok', timer=2000)
        context = {
            'title': 'Edit Domain',
            'menu_active': 'domains',
            'form': form,
            'title_submit': 'Save Domain',
            'col_size': '4'
        }
    except (MAASError) as e:
        sweetify.sweetalert(request, 'Warning', text=str(e), button='Ok', timer=5000)
        context = None
    return render(request, 'maas/form.html', context)


@login_required
def delete(request, id):
    try:
        maas = MAAS()
        resp = maas.delete(f"domains/{id}/")
        if resp.status_code in maas.ok:
            sweetify.success(request, _('Successfully deleted domain'), button='Ok', timer=2000)
        else:
            sweetify.warning(request, _(resp.text), button='Ok', timer=2000)
    except (MAASError) as e:
        sweetify.sweetalert(request, 'Warning', text=str(e), button='Ok', timer=5000, icon='error')
    return redirect("maas:dns:index")
