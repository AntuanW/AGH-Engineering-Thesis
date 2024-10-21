from fastapi import APIRouter, Depends
from app.running_config.RunningConfigService import RunningConfigService
from app.running_config.BasicConfigExtractor import BasicConfigExtractor
from app.running_config.ConfigFileWriter import ConfigFileWriter

router = APIRouter(
    prefix="/config",
    dependencies=[
        Depends(RunningConfigService),
        Depends(BasicConfigExtractor),
        Depends(ConfigFileWriter)
    ]
)


@router.post("/")
async def extract_config(running_config_service: RunningConfigService = Depends(RunningConfigService)):
    # TODO: implement this shit
    raise NotImplementedError()
