from hujan_ui.installers.models import Server
from hujan_ui.utils.host_editor import HostEditor


def save_server_to_hosts():
    servers = Server.objects.all()

    editor = HostEditor()
    editor.clear()
    for s in servers:
        editor.add(address=s.ip_address, names=[s.name])

    editor.save()
