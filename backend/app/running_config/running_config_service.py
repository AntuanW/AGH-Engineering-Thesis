import logging
from fastapi import Depends

from pathlib import Path
from .basic_config_extractor import BasicConfigExtractor
from .util.device_config_types import DeviceConfigInfo
from .exceptions.config_extraction_exceptions import (
    XmlOpenException,
    InvalidDecryptedCmlFormatException,
    DeviceJsonParseException
)


class RunningConfigService:
    def __init__(self, extractor: BasicConfigExtractor = Depends(BasicConfigExtractor)):
        self.extractor: BasicConfigExtractor = extractor

    def get_configs_for_upload(self, decrypted_xml_path: str | Path) -> list[DeviceConfigInfo]:
        topology_config: list[DeviceConfigInfo] = []

        try:
            topology_config = self.extractor.get_topology_config_from_xml(decrypted_xml_path)
        except (XmlOpenException, InvalidDecryptedCmlFormatException, DeviceJsonParseException) as exc:
            logging.error(str(exc))
        except Exception as exc:
            logging.error(f"Error occurred while extracting configs from xml: {str(exc)}")

        logging.info(f"Successfully extracted and saved configs for {len(topology_config)} devices.")

        return topology_config
