import logging
from fastapi import Depends

from ..models.topology import TopologyModel
from .basic_config_extractor import BasicConfigExtractor
from .util.device_config_types import DeviceConfigInfo
from .exceptions.config_extraction_exceptions import (
    InvalidDecryptedXmlFormatException,
    DeviceJsonParseException
)
from ..models.xml import XMLModel


class RunningConfigService:
    def __init__(self, extractor: BasicConfigExtractor = Depends(BasicConfigExtractor)):
        self.extractor: BasicConfigExtractor = extractor

    #TODO: Allow the user to provide a name for the topology as a parameter
    def get_configs_for_upload(self, xml_model: XMLModel) -> TopologyModel:
        topology_config: list[DeviceConfigInfo] = []

        try:
            topology_config = self.extractor.get_topology_config_from_xml(xml_model.xml)
            logging.info(f"Successfully extracted and saved configs for {len(topology_config)} devices.")
        except (InvalidDecryptedXmlFormatException, DeviceJsonParseException) as exc:
            logging.error(str(exc))
        except Exception as exc:
            logging.error(f"Error occurred while extracting configs from xml: {str(exc)}")

        return TopologyModel(topology=topology_config, name=xml_model.name)
