import logging
from fastapi import Depends

from ..models.topology import TopologyModel
from .basic_config_extractor import BasicConfigExtractor
from .dto.topology_response_dto import DeviceConfigInfo
from .exceptions.config_extraction_exceptions import (
    InvalidDecryptedXmlFormatException,
    DeviceJsonParseException
)


class RunningConfigService:
    def __init__(self, extractor: BasicConfigExtractor = Depends(BasicConfigExtractor)):
        self.extractor: BasicConfigExtractor = extractor

    def get_configs_for_upload(self, decrypted_xml: dict) -> TopologyModel:
        topology_config: list[DeviceConfigInfo] = []

        try:
            topology_config = self.extractor.get_topology_config_from_xml(decrypted_xml)
            logging.info(f"Successfully extracted and saved configs for {len(topology_config)} devices.")
        except (InvalidDecryptedXmlFormatException, DeviceJsonParseException) as exc:
            logging.error(str(exc))
        except Exception as exc:
            logging.error(f"Error occurred while extracting configs from xml: {str(exc)}")

        return TopologyModel(topology=topology_config)
