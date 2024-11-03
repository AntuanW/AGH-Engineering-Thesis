from .netmiko_config_builder import NetmikoConfigBuilder


class ConfigUploadService:
    def __init__(self, netmiko_config_builder: NetmikoConfigBuilder):
        self.netmiko_config_builder = netmiko_config_builder

    def upload_all_configs(self):
        pass