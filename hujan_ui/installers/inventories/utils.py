from hujan_ui.installers.models import Inventory
from hujan_ui.utils.multinode_writer import MultiNodeWriter


def save_inventory_multi_node():
    inventories = Inventory.objects.all()

    writer = MultiNodeWriter()
    for inv in inventories:
        writer.add_entry(inv.group, inv.server.name)

    writer.save()
