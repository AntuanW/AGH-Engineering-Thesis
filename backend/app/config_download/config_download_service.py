import tempfile

from fastapi import Depends

from .netmiko_client import NetmikoClient
from .dto.download_request_dto import ConfigDownloadDto


class ConfigDownloadService:
    def __init__(self, netmiko_client: NetmikoClient = Depends(NetmikoClient)):
        self.netmiko_client = netmiko_client

    def get_physical_configs(self, config_to_download: list[ConfigDownloadDto]) -> str:
        tmpdir = tempfile.mkdtemp()
        for config in config_to_download:
            self._download_and_save_configs(config)

        # TODO: shit to get created zip file
        return tmpdir


    def _create_tmp_zip_archive(self) -> str:
        pass


    def _download_and_save_configs(self, device_info: ConfigDownloadDto):
        running_config: str = self.netmiko_client.download_config_from_device(device_info)
