import requests
import json
import sweetify

from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from hujan_ui.maas.utils import MAAS
from .forms import AddDomainForm, EditDomainForm


@login_required
def index(request):
    if settings.WITH_EX_RESPONSE:
        with open(settings.DIR_EX_RESPONSE + "domains.json") as readfile:
            domains = json.load(readfile)
    else:
        maas = MAAS()
        domains = maas.get("domains/").json()
        machine_file = open("hujan_ui/maas/ex_response/domains.json", "w")
        json.dump(domains, machine_file)
        machine_file.close()

    form = AddDomainForm(request.POST or None)
    if form.is_valid():
        form.save()
        sweetify.success(request, _('Successfully added domain'), button='Ok', timer=2000)
        return redirect("maas:dns:index")

    context = {
        'title': 'DNS',
        'domains': domains,
        'menu_active': 'domains',
        'form': form
    }
    return render(request, 'maas/dns/index.html', context)


@login_required
def add(request):
    form = AddDomainForm(request.POST or None)
    if form.is_valid():
        form.save()
        sweetify.success(request, _('Successfully added domain'), button='Ok', timer=2000)
        return redirect("maas:dns:index")

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
    maas = MAAS()
    domain = maas.get(f"domains/{id}/").json()

    form = EditDomainForm(request.POST or None, initial=domain)
    if form.is_valid():
        form.save(domain['id'])
        sweetify.success(request, _('Successfully edited domain'), button='Ok', timer=2000)
        return redirect("maas:dns:index")

    context = {
        'title': 'Edit Domain',
        'menu_active': 'domains',
        'form': form,
        'title_submit': 'Save Domain',
        'col_size': '4'
    }
    return render(request, 'maas/form.html', context)


@login_required
def delete(request, id):
    maas = MAAS()
    maas.delete(f"domains/{id}/")
    sweetify.success(request, _('Successfully deleted domain'), button='Ok', timer=2000)
    return redirect("maas:dns:index")
