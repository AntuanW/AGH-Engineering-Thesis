from enum import Enum


class NetmikoAction(Enum):
    UPLOAD_COMMAND_SET = 1
    DOWNLOAD_RUNNING_CONFIG = 2
    SET_HOSTNAME_AND_CDP_TIMERS = 3
