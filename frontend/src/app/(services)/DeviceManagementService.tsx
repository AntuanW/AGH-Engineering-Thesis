import { Device } from "../(interfaces)/device-management/Device";
import { DeviceType } from "../(interfaces)/device-management/DeviceType";
import { InterfaceType } from "../(interfaces)/device-management/InterfaceType";

interface FormValues {
  name: string;
  device_type: DeviceType;
  rack_id: number;
  commands: string[];
  interfaces: {
    type?: InterfaceType;
    value: string;
  }[];
}

export const getAllDevices = async (): Promise<Device[]> => {
  return await fetch("http://localhost:8000/devices_management/devices", {
    next: {
      tags: ["all-devices"]
    }
  })
    .then((response) => response.json())
    .then((data: Device[]) => data)
    .catch((error) => {
      throw new Error(`HTTP GET error while retrieving devices. Status: ${error}`)
    });  
}

export const getSingleDevice = async (deviceId: string): Promise<Device> => {
  return await fetch(`http://localhost:8000/devices_management/devices/${deviceId}`)
    .then((response) => response.json())
    .then((data: Device) => data)
    .catch((error) => {
      throw new Error(`HTTP GET error while retriving device with id ${deviceId}. Status: ${error}`)
    });
}

export const deleteSingleDevice = async (deviceId: string) => {
  return await fetch(`http://localhost:8000/devices_management/devices/${deviceId}`, {
    method: "DELETE"
  })
    .then((response) => response.json())
    .then((data) => data)
    .catch((error) => {
      throw new Error(`HTTP DELETE error while deleting device with id ${deviceId}. Status: ${error}`)
    });
}

export const createNewDevice = async (requestBody: FormValues) => {
  return await fetch(`http://localhost:8000/devices_management/devices`, {
    method: "POST",
    body: JSON.stringify(requestBody),
    headers: {
			'content-type': 'application/json;charset=UTF-8'
		}
  })
    .then((response) => response.json())
    .then((data) => data)
    .catch((error) => {
      throw new Error(`HTTP POST error while creating new device. Status: ${error}`)
    });
}

export const updateDevice = async (deviceId: string, requestBody: FormValues) => {
  return await fetch(`http://localhost:8000/devices_management/devices/${deviceId}`, {
    method: "PUT",
    body: JSON.stringify(requestBody),
    headers: {
			'content-type': 'application/json;charset=UTF-8'
		}
  })
    .then((response) => response.json())
    .then((data) => data)
    .catch((error) => {
      throw new Error(`HTTP POST error while creating new device. Status: ${error}`)
    });
}