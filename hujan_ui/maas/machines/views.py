import json
import sweetify

from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string

from hujan_ui.maas.utils import MAAS
from hujan_ui import maas
from .forms import AddMachineForm, PowerTypeIPMIForm, PhysicalForm
from django.template.defaultfilters import filesizeformat


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
    machine = maas.get_machines(system_id)
    events = maas.get_events()
    
    if request.is_ajax():
        return JsonResponse({'machine': machine, 'events': events})


    context = {
        'title': f"Machines - {machine['fqdn']}",
        'machine': machine,
        'events': events,
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


def load_machine(request):
    
    m = MAAS()
    machines = maas.get_machines()
    html = ''
    for m in machines:
        power = "<i class='text-success fas fa-power-off'></i> <small>ON</small>" if m['power_state'] == 'on' else "<i class='text-success fas fa-power-off'></i> <small>OFF</small>"
        html += '<tr><td><a href="{}">{}</a></td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(
            reverse('maas:machines:details', args=[m['system_id']]),
            m['fqdn'], 
            power, 
            m['status_name'], 
            m['owner'], 
            m['cpu_count'], 
            filesizeformat(m['memory']), 
            filesizeformat(m['storage'])
            )

    return JsonResponse({'data': html})


def edit_physical(request, system_id, id=None):
    physical = maas.get_physicals(system_id, id)
    form = PhysicalForm(data=request.POST or None, initial=physical)
    if form.is_valid():
        data = form.clean()
        data.update({
            'system_id': system_id, 
            'id': id
        })
        
        m = MAAS()
        resp = m.put(f'nodes/{system_id}/interfaces/{id}/', data=data)
        if resp.status_code in m.ok:
            return JsonResponse({
                'status': 'success', 
                'message': _('Edit Interfaces Successfully'), 
                'urlhref': reverse('maas:machines:index')
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': _('Failed Edit Interface')
            })
    
    context = {
        'form': form,
        'url': reverse('maas:machines:edit_physical', args=[system_id, id])
    }

    html = render_to_string('partials/form_core.html', request=request, context=context)
    return JsonResponse({'html': html}, safe=False)

def mark_disconnect(request, system_id, id):
    m = MAAS()
    resp = m.post(f'nodes/{system_id}/interfaces/{id}/?op=disconnect', data={'system_id': system_id, 'id': id})
    if resp.status_code in m.ok:
        return JsonResponse({'status': 'success', 'message': _('Interfaces Disconnected Successfully'), 'urlhref': reverse('maas:machines:index') })
    return JsonResponse({'status': 'error', 'message': _(resp.text) })
    
    
