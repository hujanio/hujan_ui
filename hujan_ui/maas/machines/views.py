import requests
import json
import sweetify

from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from hujan_ui.maas.utils import MAAS
from .forms import AddMachineForm, PowerTypeIPMIForm


@login_required
def index(request):
    if settings.WITH_EX_RESPONSE:
        with open(settings.DIR_EX_RESPONSE + "machines.json") as readfile:
            machines = json.load(readfile)
    else:
        maas = MAAS()
        machines = maas.get("machines/").json()
        machine_file = open("hujan_ui/maas/ex_response/machines.json", "w")
        json.dump(machines, machine_file)
        machine_file.close()

    context = {
        'title': 'Machines',
        'machines': machines,
        'menu_active': 'machines',
    }
    return render(request, 'maas/machines/index.html', context)


@login_required
def details(request, system_id):
    if settings.WITH_EX_RESPONSE:
        with open(settings.DIR_EX_RESPONSE + "machine_details.json") as readfile:
            machine = json.load(readfile)
    else:
        maas = MAAS()
        machine = maas.get(f"machines/{system_id}/").json()

    context = {
        'title': f"Machines - {machine['fqdn']}",
        'machine': machine,
        'menu_active': 'machines',
    }
    return render(request, 'maas/machines/details.html', context)


@login_required
def add(request):
    form = AddMachineForm(request.POST or None)
    form_ipmi = PowerTypeIPMIForm(request.POST or None)

    if form.is_valid() and form_ipmi.is_valid():
        data = form.clean()
        ipmi_data = form_ipmi.clean()
        data.update({
            'commission': True,
            'power_parameters': ipmi_data}
        )
        maas = MAAS()
        resp = maas.post("machines/", data=data)
        print(resp.text)
        if resp.status_code in maas.ok:
            sweetify.success(request, _('Successfully added domain'), button='Ok', timer=2000)
            return redirect("maas:machines:index")

        sweetify.warning(request, _(resp.text), button='Ok', timer=5000)

    context = {
        'title': 'Add Machine',
        'form': form,
        'form_ipmi': form_ipmi
    }
    return render(request, "maas/machines/add-form.html", context)
