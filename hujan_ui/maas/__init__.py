import json
from django.conf import settings
from .utils import MAAS


def get_machines(machine_id=None):
    if settings.WITH_EX_RESPONSE:
        machines = load_document('machines.json')
        if machine_id:
            temp_machine = [machine for machine in machines if machine['system_id'] == machine_id]
            machines = temp_machine[0] if temp_machine else []
    else:
        maas = MAAS()
        if machine_id:
            machines = maas.get(f'machines/{machine_id}/').json()
            write_document(machines, 'machine_details.json')
        else:
            machines = maas.get("machines/").json()
            write_document(machines, 'machines.json')

    return machines


def get_physicals(system_id, id=None):
    if settings.WITH_EX_RESPONSE:
        if system_id and id:
            physicals = load_document('interface_detail.json')

    else:
        m = MAAS()
        if system_id and id:
            physicals = m.get(f'nodes/{system_id}/interfaces/{id}/').json()
            write_document(physicals, 'interface_detail.json')
        else:
            physicals = m.get(f'nodes/{system_id}/').json()
            write_document(physicals, 'interface.json')

    return physicals


def get_subnets(subnet_id=None, op=None):
    if op and subnet_id:
        m = MAAS()
        res = m.get(f'subnets/{subnet_id}/?op={op}').json()

        return res

    if settings.WITH_EX_RESPONSE:
        subnets = load_document('subnets.json')
        if subnet_id:
            sub = [subnet for subnet in subnets if subnet['id'] == subnet_id]
            subnets = sub[0] if sub else []

    else:
        maas = MAAS()
        if subnet_id:
            subnets = maas.get("subnets/{subnet_id}/").json()
        else:
            subnets = maas.get("subnets/").json()
            write_document(subnets, 'subnets.json')

    return subnets


def get_fabrics(fabric_id=None):
    if settings.WITH_EX_RESPONSE:

        fabrics = load_document('fabrics.json')
        if fabric_id:
            fab = [f for f in fabrics if f['id'] == fabric_id]
            fabrics = fab[0] if fab else []
        vlans = load_document('vlans.json')
        store = []
        for f in fabrics:
            for g in f['vlans']:
                store.append(g)
        write_document(store, 'vlans.json')

    else:
        maas = MAAS()
        if fabric_id:
            fabrics = maas.get(f"fabrics/{fabric_id}/").json()
        else:
            fabrics = maas.get("fabrics/").json()
            write_document(fabrics, 'fabrics.json')

    return fabrics


def get_spaces(space_id=None):
    if settings.WITH_EX_RESPONSE:
        spaces = load_document('spaces.json')
        if space_id:
            s = [space for space in spaces if space['id'] == space_id]
            spaces = s[0] if s else []

    else:
        m = MAAS()
        if space_id:
            spaces = m.get('spaces/{space_id}/').json()
        else:
            spaces = m.get('spaces/').json()
            write_document(spaces, 'spaces.json')

    return spaces


def get_subnet_byfabric():
    def check_vlan(subnet, vlan_id):
        subnets = subnet()
        for subnet in subnets:
            if vlan_id == subnet['vlan']['id']:
                return subnet
        return None

    store = []
    fabrics = get_fabrics()
    for fabric in fabrics:
        for vlan in fabric['vlans']:
            fabric['subnet'] = check_vlan(get_subnets, vlan['id'])
        store.append(fabric)
    return store


def get_vlans(id=None):
    vlans = load_document('vlans.json')
    if not vlans:
        vlans = []
    else:
        if id:
            vlan = [i for i in vlans if i['id'] == id]
            vlans = vlan[0] if vlan else []
    return vlans


def load_document(data):
    with open(settings.DIR_EX_RESPONSE + data) as readfile:
        return json.load(readfile)


def write_document(data, store):
    file = open(settings.DIR_EX_RESPONSE + store, 'w')
    json.dump(data, file)
    file.close()


def get_events():
    if settings.WITH_EX_RESPONSE:
        events = load_document('events.json')
    else:
        m = MAAS()
        events = m.get('events/?op=query').json()
        write_document(events, 'events.json')

    return events
