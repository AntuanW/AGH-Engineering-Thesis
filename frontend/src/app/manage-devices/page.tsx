import Link from "next/link";
import { Device } from "../(interfaces)/device-management/Device";
import { getAllDevices } from "../(services)/DeviceManagementService";
import { DeviceType } from "../(interfaces)/device-management/DeviceType";

import "./page.css";

const ManageDevices = async () =>  {
  const getFilteredDevices = async () => {
    const allDevices: Device[] = await getAllDevices();
    return allDevices
      .filter((device) => device.device_type !== DeviceType.PC)
      .sort((a, b) => (a.rack_id - b.rack_id));
  }

  const devices: Device[] = await getFilteredDevices();

  return (
    <div>
      <div className="add-device-container">
        <Link href="/manage-devices/add-device" className="add-device">
          Add new device
        </Link>
      </div>
      <div className="devices-container">
        {devices.map((device, i) => {
          return (
            <div key={i} className="device-card">
              <h2 className="device-name">{device.name}</h2>
              <div className="device-basic-info">
                <p>{device.device_type}</p>
                <p>Rack id: {device.rack_id}</p>
              </div>
              <div className="device-link-container">
                <Link href={`/manage-devices/${device._id}`} className="device-link submit-button">
                  Details
                </Link>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default ManageDevices;