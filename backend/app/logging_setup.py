import logging
import logging.config as log_cfg
from pathlib import Path
import yaml


def read_yaml_file(path: str, encoding: str = "utf-8") -> dict:
    default_dict = {"version": 1}   # Needs investigation
    try:
        with open(path, "r", encoding=encoding) as input_file:
            input_data = yaml.safe_load(input_file)
    except yaml.YAMLError as exc:
        print(str(exc))
        return default_dict
    except OSError as exc:
        print(str(exc))
        return default_dict
    return input_data


def setup_logging(logging_file_cfg: str | Path):
    config = read_yaml_file(logging_file_cfg)
    logging.config.dictConfig(config)