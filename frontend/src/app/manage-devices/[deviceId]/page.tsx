"use client"
import { Device } from "@/app/(interfaces)/device-management/Device";
import { DeviceType } from "@/app/(interfaces)/device-management/DeviceType";
import { deleteSingleDevice, getSingleDevice } from "@/app/(services)/DeviceManagementService";
import { redirect } from "next/navigation";
import { useEffect, useState } from "react";

import "./page.css";
import Link from "next/link";

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
  const [deviceId, setDeviceId] = useState("");
  const [device, setDevice] = useState<Device>(EmptyDevice);
  const [showInterfaces, setShowInterfaces] = useState(false);
  const [showIntefracesTxt, setShowInterfacesTxt] = useState(SHOW);

  useEffect(() => {
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
      console.error(`Error occured while deleting device with di ${(await params).deviceId}. Status: ${error}`);
    } finally {
      if (response) {
        redirect("/manage-devices");
      }
    }
  }

  const onBack = () => {
    redirect("/manage-devices");
  }

  const getClassName = () => {
    return showInterfaces ? "hide" : "show";
  }
  
  return (
    <div className="device-details-card">
      <div className="device-name-info">
        <h1>{device.name}</h1>
      </div>
      <div className="device-basic-info">
        <p>Device type: {device.device_type}</p>
        <p>Rack id: {device.rack_id}</p>
      </div>
      
      <div className="show-hide-container">
        <button className={`show-hide ${getClassName()}`} onClick={onShowIntefaces}>
          {showIntefracesTxt}
        </button>
      </div>

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
        <button className="back" onClick={onBack}>Back</button>
        <Link href={`/manage-devices/${deviceId}/edit`} className="edit">Edit</Link>
        <button className="delete" onClick={onDelete}>Delete</button>
      </div>
    </div>
  );
}

export default DeviceDetails;