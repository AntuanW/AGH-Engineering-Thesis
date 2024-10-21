from pathlib import Path
from .util.DeviceConfigTypes import DeviceConfigInfo



class ConfigFileWriter:
    RESOURCES_PATH: Path = Path(__file__).parent.joinpath('resources/configs')

    def write_config_to_file(self, dev_config: DeviceConfigInfo, id_: int):
        # TODO: implement this shit
        raise NotImplementedError()