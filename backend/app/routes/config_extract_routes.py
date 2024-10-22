from fastapi import APIRouter, Depends

from app.running_config.RunningConfigService import RunningConfigService
from app.running_config.BasicConfigExtractor import BasicConfigExtractor
from app.running_config.util.DeviceConfigTypes import DeviceConfigInfo

router = APIRouter(
    prefix="/config"
)


@router.post("/xml-extract")
async def extract_config(
        running_config_service: RunningConfigService = Depends(RunningConfigService),
        basic_config_extractor: BasicConfigExtractor = Depends(BasicConfigExtractor)
) -> list[DeviceConfigInfo]:
    raise NotImplementedError()
