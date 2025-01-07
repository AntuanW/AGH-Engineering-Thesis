from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from bson.objectid import ObjectId
from bson.errors import InvalidId

from app.repository.device_repository import DeviceRepository
from app.repository.exceptions.repository_exceptions import DatabaseException
from app.models.device import DeviceModel


router = APIRouter(prefix="/devices_management", tags=["device-management"])


@router.get("/devices")
async def get_devices(device_repository: DeviceRepository = Depends(DeviceRepository)) -> JSONResponse:
    try:
        response: list = device_repository.find({})
    except DatabaseException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong with database connection.")

    response = [{**device, "_id": str(device["_id"])} for device in response]
    return JSONResponse(status_code=status.HTTP_200_OK, content=response)


@router.get("/devices/{device_id}")
async def get_single_device(
        device_id: str,
        device_repository: DeviceRepository = Depends(DeviceRepository)
) -> JSONResponse:
    try:
        device_id = ObjectId(device_id)
        response: DeviceModel = device_repository.find_object({"_id": device_id})
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="device_id has invalid format.")
    except DatabaseException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong with database connection.")

    return JSONResponse(status_code=status.HTTP_200_OK, content=response.model_dump())


@router.put("/devices/{device_id}")
async def update_device(
        device_id: str,
        new_device: DeviceModel,
        device_repository: DeviceRepository = Depends(DeviceRepository)
) -> JSONResponse:
    try:
        device_id = ObjectId(device_id)
        response = device_repository.update({"_id": device_id}, new_device.model_dump())
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="device_id has invalid format.")
    except DatabaseException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong with database connection.")

    return JSONResponse(status_code=status.HTTP_200_OK, content=new_device.model_dump())


@router.post("/devices")
async def create_device(
        new_device: DeviceModel,
        device_repository: DeviceRepository = Depends(DeviceRepository)
) -> JSONResponse:
    try:
        device_repository.insert(new_device)
    except DatabaseException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong with database connection.")

    return JSONResponse(status_code=status.HTTP_200_OK, content=new_device.model_dump())


@router.delete("/devices/{device_id}")
async def delete_device(
        device_id: str,
        device_repository: DeviceRepository = Depends(DeviceRepository)
) -> JSONResponse:
    try:
        device_id = ObjectId(device_id)
        n_affected: int = device_repository.delete({"_id": device_id})
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="device_id has invalid format.")
    except DatabaseException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong with database connection.")

    if not n_affected:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no device with id: {device_id} in database.")

    response = {"affected": n_affected}
    return JSONResponse(status_code=status.HTTP_200_OK, content=response)
