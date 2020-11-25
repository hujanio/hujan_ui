from django.conf import settings


class GlobalConfigWriter:
    file_name = settings.CONFIG_DIR_GLOBAL_YML

    def __init__(self):
        self.entry = {}

    def add_entry(self, key: str, value):
        entry_value = value
        if type(value) == bool:
            entry_value = "yes" if value else "no"

        self.entry[key] = entry_value

    def set_entry(self, entry):
        for k, v in entry.items():
            self.add_entry(k, v)

    def save(self):
        with open(self.file_name, 'w') as f:
            for k, v in self.entry.items():
                if type(v) == int:
                    f.write("%s: %s\n" % (k, v))
                else:
                    f.write("%s: \"%s\"\n" % (k, v))

    def clear(self):
        open(self.file_name, 'w').close()

    @staticmethod
    def save_from_model(global_config):
        writer = GlobalConfigWriter()
        
        params = {
            "kolla_install_type": global_config.installation_type,
            "openstack_release": global_config.openstack_release,
            "kolla_internal_vip_address": global_config.internal_vip_address,
            "kolla_external_vip_address": global_config.external_vip_address,
            "kolla_enable_tls_external": global_config.enable_tls_on_external_api,
            "neutron_plugin_agent": global_config.neutron_plugin_agent,
            "enable_ceph": global_config.enable_ceph_service,
            "enable_cinder": global_config.enable_cinder_service,
            "enable_magnum": global_config.enable_magnum_service,
            "enable_neutron_fwaas": global_config.enable_fwaas,
            "enable_neutron_qos": global_config.enable_qos,
            "enable_neutron_agent_ha": global_config.enable_ha_agent,
            "enable_neutron_vpnaas": global_config.enable_vpnaas,
            "enable_octavia": global_config.enable_octavia_service,
            "ceph_pool_pg_num": global_config.ceph_pool_pg_num,
            "ceph_pool_pgp_num": global_config.ceph_pool_pgp_num,
            "glance_backend_ceph": global_config.glance_backend_using_ceph,
            "glance_backend_file": global_config.glance_backend_file
        }
        if global_config.storage_interface:
            params['storage_interface'] = global_config.storage_interface

        if global_config.network_interface:
            params['network_interface'] = global_config.network_interface

        writer.set_entry(params)
        writer.save()
