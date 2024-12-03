import tempfile
import os
import re

from zipfile import ZipFile
from fastapi import Depends

from .netmiko_client import NetmikoClient
from .dto.download_request_dto import DownloadConfigsDto


class ConfigDownloadService:
    def __init__(self, netmiko_client: NetmikoClient = Depends(NetmikoClient)):
        self.netmiko_client = netmiko_client

    # TODO: it should return tuple: zip_path and connections for creating instructions
    def get_physical_configs(self, config_to_download: DownloadConfigsDto) -> str:
        zip_archive, zip_path, tmpdir_path = self._create_tmp_zip_archive(config_to_download.lab_name,
                                                                          config_to_download.device_name)

        for device in config_to_download.devices:
            running_config, neighbors = self.netmiko_client.download_config_from_device(device)
            neighbors = self._parse_neighbors_string(neighbors)
            self._add_configs_to_zip(running_config, device.name, zip_archive, tmpdir_path)

        zip_archive.close()
        return zip_path

    def _create_tmp_zip_archive(self, lab_name: str, lab_group: str) -> tuple[ZipFile, str, str]:
        archive_name: str = f'{lab_name}-{lab_group}.zip'
        tmpdir: str = tempfile.mkdtemp()
        zip_path: str = os.path.join(tmpdir, archive_name)
        return ZipFile(zip_path, 'w'), zip_path, tmpdir

    def _add_configs_to_zip(self, running_config: str, device_name: str, zip_archive: ZipFile, tmpdir_path: str):
        config_filename: str = f'{device_name}-config.txt'
        config_filepath: str = os.path.join(tmpdir_path, config_filename)

        with open(config_filepath, 'w') as config_file:
            config_file.write(running_config)
        zip_archive.write(config_filepath, os.path.basename(config_filepath))

    def _parse_neighbors_string(self, neighbors_string: str) -> list[list[str]]:
        neighbors: list[list[str]] = []
        split_regex = r'\s{2,}'

        split_neighbors = neighbors_string.split('\n')[3:-1]
        for record in split_neighbors:
            neighbors.append(re.split(split_regex, record))

        # returns list of lists where elements are: Device ID, Local Intrfce, Holdtime, Capability, Platform, Port ID
        # TODO: better parsing after we'll see cdp in lab
        return neighbors
