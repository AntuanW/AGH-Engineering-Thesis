from pathlib import Path
import xmltodict
from app.running_config.running_config_service import RunningConfigService
from app.running_config.basic_config_extractor import BasicConfigExtractor
from app.running_config.utils.device_config_constants import XmlConfigConstants
from app.config_upload.config_upload_service import ConfigUploadService

IP = '172.17.145.20'
PORTS = [2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008]
XML_PATH = Path(__file__).parent.joinpath("lab-22_11_24.xml")


xml_dict = xmltodict.parse(open(XML_PATH).read())

constants = XmlConfigConstants()
basic_config_extractor = BasicConfigExtractor(constants)

config_service = RunningConfigService(basic_config_extractor)
configs = config_service.get_configs_for_upload(xml_dict)

upload_service = ConfigUploadService()
devices = upload_service.build_netmiko_devices(configs.topology)

print(devices)
# upload_service.upload_configs(devices)


"""
TODO:

1. Make the script work with fastapi DI, as now it does not

2. Deal with 'Would you like to cośtam dialog? [yes/no]':
    - Update NetmikoDevice.__enter__() with something like
        ```
        retval.write_channel('\r')
        time.sleep(1)
        retval.write_channel('no')
        time.sleep(1)
        retval.write_channel('\r')
        time.sleep(1)
        ```
    but shorter and better. 
    - Execute 'conf t' next:
        ```
        cli.send_command('conf t', expect_string='#')
        ```
    we need expect_string here to send the command after the CLI prints 'Router#'
    
3. Hope that the network creates without issues
"""