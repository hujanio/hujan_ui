from django.conf import settings


class MultiNodeWriter:
    """
    Multinode file writer Utility
    """

    file_name = settings.CONFIG_DIR_MULTINODE
    file_template = settings.CONFIG_DIR_MULTINODE_TEMPLATE
    default_lines = []
    group_lines = []

    def __init__(self):
        self.ansible_user = settings.DEFAULT_ANSIBLE_USER
        self.entry = {}
        self.read_contents()

    def read_contents(self):
        with open(self.file_template, 'r') as f:
            lines = f.readlines()
        default_line, group_line = self.separate_lines(lines)
        self.default_lines = default_line
        self.group_lines = group_line

    def separate_lines(self, lines):
        default_lines = []
        multinode_lines = []
        group = None
        for l in lines:
            if "]\n" in l:
                group = l.rstrip("\n").replace('[', '').replace(']','')
                self.entry[group] = []
            else:
                if l != "\n":
                    self.add_entry(group, l)

        return default_lines, multinode_lines

    def add_entry(self, group: str, server_name: str):
        if self.entry.get(group, None):
            self.entry[group].append(server_name)
        else:
            self.entry[group] = [server_name]

    def add_entry_list(self, group: str, server_names: list):
        for s in server_names:
            self.add_entry(group, s)

    def save(self):
        inventories = ['control', 'network', 'compute', 'monitoring', 'storage']
        with open(self.file_name, 'w') as f:
            for k, v in self.entry.items():

                f.write("[%s]\n" % k)
                for x in v:
                    if x:
                        if k in inventories and '#' not in x:
                            f.write("%s ansible_user=%s\n" % (x, self.ansible_user))
                        else:
                            f.write("%s\n" % x)
                f.write("\n")
    
    def clear(self):
        open(self.file_name, 'w').close()

    @staticmethod
    def save_from_model(inventories):
        writer = MultiNodeWriter()
        for inv in inventories:
            writer.add_entry(inv.group, inv.server.name)

        writer.save()
