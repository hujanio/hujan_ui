import sweetify
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from hujan_ui.maas.utils import MAAS
from hujan_ui import maas
from .forms import SubnetForm, SubnetAddForm
from hujan_ui.maas.exceptions import MAASError


@login_required
def index(request):
    try:
        if request.is_ajax():
            return JsonResponse({'subnets': maas.get_subnets()})
        subnets = maas.get_subnets()
        fabrics = maas.get_fabrics()
        spaces = maas.get_spaces()
        group_subnet = maas.get_subnet_byfabric()
        context = {
            'title': 'Subnet By Fabric',
            'subnets': subnets,
            'fabrics': fabrics,
            'spaces': spaces,
            'group_subnet': group_subnet,
            'menus_active': 'subnets_active'
        }
    except (MAASError) as e:
        sweetify.sweetalert(request, 'Warning', text=str(e), icon='error', timer=5000)
        context = None

    return render(request, 'maas/subnets/index.html', context)


@login_required
def detail(request, subnet_id):
    try:
        subnet = maas.get_subnets(subnet_id)
        # unr = maas.get_subnets(subnet_id,op='unreserved_ip_ranges')
        # stat = maas.get_subnets(subnet_id,op='statistics')
        # TODO untuk data unreserved dan statistic masih belum sesuai antara api dan maas yang ada
        rir = maas.get_subnets(subnet_id, op='reserved_ip_ranges')

        if request.is_ajax():
            return JsonResponse({'subnet': subnet})

        context = {
            'title': f"Subnet - {subnet['name']}",
            'subnet': subnet,
            # 'unr': unr,
            # 'stat': stat,
            # TODO untuk data unreserved dan statistic masih belum sesuai antara api dan maas yang ada
            'rir': rir,
            'menu_active': 'subnets',
        }
    except (MAASError) as e:
        sweetify.sweetalert(request, 'Warning', text=str(e), icon='error', timer=5000)

    return render(request, 'maas/subnets/subnet_detail.html', context)


@login_required
def add(request):
    form = SubnetAddForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        try:
            m = MAAS()
            data = form.clean()
            resp = m.post('subnets/', data=data)
            if resp.status_code in m.ok:
                sweetify.sweetalert(request, 'Success', text=_('Subnet Added Successfully'), icon='success', timer=2000)
                return redirect('maas:subnets:index')
            sweetify.sweetalert(request, 'Warning', text=_(resp.text), icon='warning', timer=5000)
        except (MAASError) as e:
            sweetify.sweetalert(request, 'Error', text=str(e), button='OK', icon='error', timer=5000)
    context = {
        'title': _('Form Add Subnet'),
        'form': form
    }
    return render(request, 'maas/subnets/add.html', context)


@login_required
def edit(request, subnet_id):
    try:
        subnet = maas.get_subnets(subnet_id)
        if not subnet:
            return redirect('maas:subnets:index')
        form = SubnetForm(request.POST or None, initial=subnet)
        if form.is_valid():
            m = MAAS()
            data = form.clean()
            if data['vlan']:
                vl = maas.get_vlans(int(data['vlan']))
                data['vid'] = vl['vid']
                data['fabric'] = vl['fabric_id']
            resp = m.put(f'subnets/{subnet_id}/', data=data)
            if resp.status_code in m.ok:
                sweetify.sweetalert(request, 'Success', text=_('Subnet Update Successfully'), icon='success', timer=2000)
                return redirect('maas:subnets:index')
            sweetify.sweetalert(request, 'Warning', text=_(resp.text), icon='warning', timer=5000)
    except (MAASError) as e:
        sweetify.sweetalert(request, 'Warning', text=str(e), icon='error', timer=5000)
        form = None

    context = {
        'title': _('Form Edit Subnet'),
        'form': form
    }
    return render(request, 'maas/subnets/add.html', context)


@login_required
def delete(request, subnet_id):
    try:
        subnets = maas.get_subnets()
        subnet = [s for s in subnets if s['id'] == subnet_id]
        if subnet[0] is not None:
            m = MAAS()
            resp = m.delete(f'subnets/{subnet_id}/')
            if resp.status_code in m.ok:
                sweetify.success(request, _('Subnet Deleted Successfully'), timer=2000)
                return redirect('maas:subnets:index')
            sweetify.warning(request, _(resp.text), timer=5000)
    except (MAASError) as e:
        sweetify.sweetalert(request, 'Warning', text=str(e), icon='error', timer=5000)

    return redirect('maas:subnets:index')
