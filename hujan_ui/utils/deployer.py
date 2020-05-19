from hujan_ui.installers.models import Server, Inventory, GlobalConfig
from hujan_ui.utils.global_config_writer import GlobalConfigWriter
from hujan_ui.utils.host_editor import HostEditor
from hujan_ui.utils.multinode_writer import MultiNodeWriter


class Deployer:
    def prepare_files(self):
        HostEditor.save_from_model(Server.objects.all())
        MultiNodeWriter.save_from_model(Inventory.objects.all())
        GlobalConfigWriter.save_from_model(GlobalConfig.objects.first())

    def deploy(self):
        self.prepare_files()
        # TODO Execute kolla-ansible
