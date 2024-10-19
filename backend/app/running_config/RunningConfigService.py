from pathlib import Path
from BasicConfigExtractor import BasicConfigExtractor


class RunningConfigService:
    def __init__(self, extractor: BasicConfigExtractor):
        self.extractor: BasicConfigExtractor = extractor

    def get_configs_for_upload(self, decrypted_xml_path: str | Path):
        raise NotImplementedError()