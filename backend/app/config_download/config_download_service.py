import tempfile
import os

from zipfile import ZipFile
from fastapi import Depends

from .netmiko_client import NetmikoClient
from .dto.download_request_dto import SingleDeviceConfigDtoV2, DownloadConfigsDto


class ConfigDownloadService:
    def __init__(self, netmiko_client: NetmikoClient = Depends(NetmikoClient)):
        self.netmiko_client = netmiko_client

    def get_physical_configs(self, config_to_download: DownloadConfigsDto) -> str:
        zip_archive, zip_path, tmpdir_path = self._create_tmp_zip_archive(config_to_download.lab_name,
                                                                          config_to_download.device_name)

        for config in config_to_download.devices:
            self._download_and_save_configs(config, zip_archive, tmpdir_path)

        zip_archive.close()
        return zip_path

    def get_physical_neighbors(self, config_to_download: DownloadConfigsDto) -> list[str]:
        pass

    def _create_tmp_zip_archive(self, lab_name: str, lab_group: str) -> tuple[ZipFile, str, str]:
        archive_name: str = f'{lab_name}-{lab_group}.zip'
        tmpdir: str = tempfile.mkdtemp()
        zip_path: str = os.path.join(tmpdir, archive_name)
        return ZipFile(zip_path, 'w'), zip_path, tmpdir

    def _download_and_save_configs(self, device_info: SingleDeviceConfigDtoV2, zip_archive: ZipFile, tmpdir_path: str):
        running_config: str = self.netmiko_client.download_config_from_device(device_info)

        config_filename: str = f'{device_info.name}-config.txt'
        config_filepath: str = os.path.join(tmpdir_path, config_filename)
        with open(config_filepath, 'w') as config_file:
            config_file.write(running_config)
        zip_archive.write(config_filepath, os.path.basename(config_filepath))
