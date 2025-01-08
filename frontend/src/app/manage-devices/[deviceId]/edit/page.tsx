"use client"
import ModifyDeviceForm from "@/app/(components)/device-forms/modify-device-form/modifyDeviceForm";
import { Group } from "@/app/(interfaces)/common/Group";
import { IndexDto } from "@/app/(interfaces)/common/IndexDto";
import { Device } from "@/app/(interfaces)/device-management/Device";
import { DeviceType } from "@/app/(interfaces)/device-management/DeviceType";
import {  getSingleDevice } from "@/app/(services)/DeviceManagementService";
import { getIndexDto } from "@/app/(services)/IndexDtoService";
import { useEffect, useState } from "react";

interface DeviceDetailsParams {
  params: Promise<{ deviceId: string }>
}

const EmptyDevice = {
  _id: "",
  name: "",
  device_type: DeviceType.UNKNOWN,
  interfaces: [],
  commands: [],
  rack_id: -1
}

const DeviceDetails = ({ params }: DeviceDetailsParams) => {
  const [device, setDevice] = useState<Device>(EmptyDevice);
  const [deviceId, setDeviceId] = useState("");
  const [groups, setGroups] = useState<Group[]>([]);

  useEffect(() => {
    const getSortedGroups = async () => {
      try {
        const indexDto: IndexDto = await getIndexDto();
        setGroups(indexDto.groups.sort((a, b) => (a.lab_group_number - b.lab_group_number)));
      } catch (error) {
        console.error(`Failed to fetch IndexDto: ${error}`);
      }
    }

    const fetchDevice = async () => {
      try {
        const _id = (await params).deviceId;
        const fetchedDevice: Device = await getSingleDevice(_id);
        setDevice(fetchedDevice);
        setDeviceId(_id);
      } catch (error) {
        console.error(`Failed to fetch device data: ${error}`);
      }
    }
    fetchDevice();
    getSortedGroups();
  }, [params, setDevice, setGroups]);
  
  return (
    <ModifyDeviceForm 
      groups={groups}
      deviceId={deviceId}
      oldDevice={device}
    />
  );
}

export default DeviceDetails;