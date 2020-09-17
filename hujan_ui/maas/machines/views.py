import json
import sweetify

from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from hujan_ui.maas.utils import MAAS
from hujan_ui import maas
from .forms import AddMachineForm, PowerTypeIPMIForm


@login_required
def index(request):
    if request.is_ajax():
        return JsonResponse({'machines': maas.get_machines()})

    context = {
        'title': 'Machines',
        'machines': maas.get_machines(),
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

    if request.is_ajax():
        return JsonResponse({'machine': machine})

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
        if resp.status_code in maas.ok:
            sweetify.success(request, _(
                'Successfully added domain'), button='Ok', timer=2000)
            return redirect("maas:machines:index")

        sweetify.warning(request, _(resp.text), button='Ok', timer=5000)

    context = {
        'title': 'Add Machine',
        'form': form,
        'form_ipmi': form_ipmi
    }
    return render(request, "maas/machines/add-form.html", context)
