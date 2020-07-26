from django.conf import settings


class MultiNodeWriter:
    """
    Multinode file writer Utility
    """

    file_name = "/home/kolla/multinode"
    ansible_user = settings.ANSIBLE_USER

    def __init__(self):
        self.entry = {}

    def add_entry(self, group: str, server_name: str):
        if self.entry.get(group, None):
            self.entry[group].append(server_name)
        else:
            self.entry[group] = [server_name]

    def add_entry_list(self, group: str, server_names: list):
        for s in server_names:
            self.add_entry(group, s)

    def save(self):
        with open(self.file_name, 'w') as f:
            for k, v in self.entry.items():
                f.write("[%s]\n" % k)
                for x in v:
                    f.write("%s ansible_user=%s\n" % (x, self.ansible_user))
                f.write("\n")

    @staticmethod
    def save_from_model(inventories):
        writer = MultiNodeWriter()
        for inv in inventories:
            writer.add_entry(inv.group, inv.server.name)

        writer.save()
