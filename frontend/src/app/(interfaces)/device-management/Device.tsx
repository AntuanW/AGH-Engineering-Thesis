import { DeviceType } from "./DeviceType";
import { Interface } from "./Interface";

export interface Device {
  _id: string;
  name: string;
  device_type: DeviceType;
  interfaces: Interface[];
  commands: string[];
  rack_id: number;
}