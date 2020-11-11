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
from .forms import AddMachineForm, PowerTypeIPMIForm, PhysicalForm, CommissionForm, DeployForm, ConfirmForm
from django.template.defaultfilters import filesizeformat
from hujan_ui.maas.exceptions import MAASError


@login_required
def index(request):
	if request.is_ajax():
		return JsonResponse({'machines': maas.get_machines()})

	try:
		data = maas.get_machines()
	except (MAASError, ConnectionError, RuntimeError) as e:
		sweetify.error(request, str(e), button='Ok', timer=2000)
		data = None

	context = {
		'title': 'Machines',
		'machines': data,
		'menu_active': 'machines',
	}
	return render(request, 'maas/machines/index.html', context)


@login_required
def details(request, system_id):
	try:
		machine = maas.get_machines(system_id)
	except (MAASError, ConnectionError, RuntimeError) as e:
		sweetify.error(request, str(e), button='Ok', timer=2000)
		machine = {}

	try:
		events = maas.get_events()
	except (MAASError, ConnectionError, RuntimeError) as e:
		sweetify.error(request, str(e), button='Ok', timer=2000)
		events = {}

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
			'power_parameters': ipmi_data
		})

		try:
			maas = MAAS()
			resp = maas.post("machines/", data=data)

			if resp.status_code in maas.ok:
				sweetify.success(request, _(
					'Successfully added domain'), button='Ok', timer=2000)
				return redirect("maas:machines:index")

			sweetify.warning(request, _(resp.text), button='Ok', timer=10000)
		except (MAASError, ConnectionError, RuntimeError, TimeoutError) as e:
			sweetify.error(request, str(e), button='OK', timer=10000)
		

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
		power = f"<i class='text-success fas fa-power-off'></i> <small>ON</small>" if m['power_state'] == 'on' else "<i class='text-danger fas fa-power-off'></i> <small>OFF</small>"
		html += '<tr><td><label><input name="csi" value="{}" type="radio" /></label></td><td><a href="{}">{}</a></td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(
				m['system_id'],
				reverse('maas:machines:details', args=[m['system_id']]),
				m['fqdn'], 
				power, 
				m['status_name'], 
				m['owner'], 
				m['cpu_count'], 
				str(m['memory']) + ' GiB', 
				str(m['storage']) + ' GB' 
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
		try:
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
		except (MAASError, ConnectionError, RuntimeError) as identifier:
			return JsonResponse({
					'status': 'error',
					'message': _(str(e))
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
		return JsonResponse({
			'status': 'success',
			'message': _('Interfaces Disconnected Successfully'),
			'urlhref': reverse('maas:machines:index')
		})
	return JsonResponse({'status': 'error', 'message': _(resp.text)})


def machine_commission(request, system_id=None):
	form = CommissionForm(request.POST or None, initial={'system_id': system_id})
	if form.is_valid():
		data = form.clean()
		try:
			m = MAAS()
			resp = m.post(f'machines/{system_id}/?op=commission', data=data)
			if resp.status_code in m.ok:
				return JsonResponse({'status': 'success', 'message': _('Commission Succesfully') })
		except (MAASError, ConnectionError, TimeoutError, RuntimeError) as e:
			return JsonResponse({'status': 'error', 'message': str(e)})
	
	context = {
		'form': form,
		'url': reverse('maas:machines:machine_commission', args=[system_id])
	}

	html = render_to_string('partials/form_core.html', request=request, context=context)
	return JsonResponse({'html': html}, safe=False)
	

def delete_machine(request, system_id):
	try:
		m = MAAS()
		resp = m.post(f'machines/{system_id}/', {'system_id': system_id})
		if resp.status_code in m.ok:
			return JsonResponse({'status': 'success', 'message': _('Machine Delete Successfully')})
	except (MAASError, ConnectionError, TimeoutError, RuntimeError) as e:
		return JsonResponse({'status': 'error', 'message': str(e)})


def deploy_machine(request, system_id):
	form = DeployForm(request.POST or None, initial={'system_id': system_id})
	if form.is_valid():
		try:
			data = form.clean()
			m = MAAS()
			resp = m.post(f'machines/{system_id}/?op=deploy', data)
			if resp.status_code in m.ok:
				return JsonResponse({'status': 'success', 'message': _('Machine Deploy Successfully')})
		except (MAASError, ConnectionError, TimeoutError, RuntimeError) as e:
			return JsonResponse({'status': 'error', 'message': str(e)})
	context = {
		'form': form,
		'url': reverse('maas:machines:deploy_machine', args=[system_id])
	}
	html = render_to_string('partials/form_core.html', request=request, context=context)
	return JsonResponse({'html': html}, safe=False)
	

def onoff_machine(request, system_id):
	form = ConfirmForm(request.POST or None, initial={'system_id': system_id})
	if form.is_valid():
		try:
			cur_machine = maas.get_machines(system_id)
			m = MAAS()
			data = form.clean()
			if cur_machine['power_state'] == 'on':
				resp = m.post(f'machines/{system_id}/?op=power_off', data)
			else:
				resp = m.post(f'machines/{system_id}/?op=power_on', data)
			if resp.status_code in m.ok:
				print(resp.text)
				return JsonResponse({'status': 'success', 'message': _('Machine Change Power Successfully')})
 
		except (MAASError, ConnectionError, TimeoutError, RuntimeError) as e:
			return JsonResponse({'status': 'error', 'message': str(e)})
	context = {
		'form': form,
		'url': reverse('maas:machines:onoff_machine', args=[system_id])
	}
	html = render_to_string('partials/form_core.html', context, request)
	return JsonResponse({'html': html}, safe=False)


def delete_machine(request, system_id):
	form = ConfirmForm(request.POST or None, initial={'system_id': system_id})
	if form.is_valid():
		data = form.clean()

		m = MAAS()
		try:
			resp = m.delete(f'machines/{system_id}/', data)
			if resp.status_code in m.ok:
				return JsonResponse({'status': 'success', 'message': _('Delete Machine Successfully')})
		except (MAASError, ConnectionError, TimeoutError, RuntimeError) as e:
			return JsonResponse({'status': 'error', 'message': str(e)})

	context = {
		'title': 'Delete Machine',
		'url': reverse('maas:machines:delete_machine', args=[system_id]),
		'form': form
	}
	html = render_to_string('partials/form_core.html', context, request)
	return JsonResponse({'html': html}, safe=False)

		