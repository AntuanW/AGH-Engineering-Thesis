"use client"
import { Device } from "@/app/(interfaces)/device-management/Device";
import { DeviceType } from "@/app/(interfaces)/device-management/DeviceType";
import { deleteSingleDevice, getSingleDevice } from "@/app/(services)/DeviceManagementService";
import { redirect } from "next/navigation";
import { useEffect, useState } from "react";

interface DeviceDetailsParams {
  params: Promise<{ deviceId: string }>
}

enum InterfacesState {
  SHOW = "Show interfaces",
  HIDE = "Hide interfaces"
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
  const { SHOW, HIDE } = InterfacesState;
  const [device, setDevice] = useState<Device>(EmptyDevice);
  const [showInterfaces, setShowInterfaces] = useState(false);
  const [showIntefracesTxt, setShowInterfacesTxt] = useState(SHOW);

  useEffect(() => {
    const fetchDevice = async () => {
      try {
        const fetchedDevice: Device = await getSingleDevice((await params).deviceId);
        setDevice(fetchedDevice);
      } catch (error) {
        console.error(`Failed to fetch device data: ${error}`);
      }
    }
    fetchDevice();
  }, [params, setDevice]);

  const onShowIntefaces = () => {
    setShowInterfaces(!showInterfaces);
    if (showInterfaces) {
      setShowInterfacesTxt(SHOW);
    } else {
      setShowInterfacesTxt(HIDE);
    }
  }

  const onDelete = async () => {
    let response = null;
    try {
      response = await deleteSingleDevice((await params).deviceId);
    } catch (error) {
      console.log(`Error occured while deleting device with di ${(await params).deviceId}. Status: ${error}`);
    } finally {
      if (response) {
        redirect("/manage-devices");
      }
    }
  }
  
  return (
    <div className="device-details-card">
      <h1>{device.name}</h1>
      <p>{device.device_type}</p>
      <p>{device.rack_id}</p>
      
      <button onClick={onShowIntefaces}>
        {showIntefracesTxt}
      </button>

      <div className="all-interfaces-container">
        {showInterfaces && device.interfaces.map((iface, i) => {
          return (
            <div key={i} className="interface-container">
              <p>{iface.type} {iface.value}</p>
            </div>
          );
        })}
      </div>

      <div className="details-actions-container">
        <button>Edit</button>
        <button onClick={onDelete}>Delete</button>
      </div>
    </div>
  );
}

export default DeviceDetails;