"use client"
import { Group } from "@/app/(interfaces)/common/Group";
import { Device } from "@/app/(interfaces)/device-management/Device";
import { DeviceType } from "@/app/(interfaces)/device-management/DeviceType";
import { InterfaceType } from "@/app/(interfaces)/device-management/InterfaceType";
import { revalidateDevices } from "@/app/(server-actions)/DevicesRevalifation";
import { updateDevice } from "@/app/(services)/DeviceManagementService";
import { redirect } from "next/navigation";
import { FieldError, useFieldArray, useForm } from "react-hook-form";
import { useEffect, useMemo } from "react";

import "./modifyDeviceForm.css";

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

interface Props {
  groups: Group[];
  deviceId: string;
  oldDevice: Device;
}

const ModifyDeviceForm = (props: Props) => {
  const form = useForm<FormValues>({
    resolver: async (data) => {
      const errors: Partial<Record<keyof FormValues, FieldError>> = {};

      if (!data.name) {
        errors.name = {type: "manula", message: "Device name is required."}
      } 
      
      else if (!data.interfaces || data.interfaces.length === 0) {
        errors.interfaces = {type: "manula", message: "At least one interface is required."}
      }
      return {
        values: data,
        errors
      }
    },
    defaultValues: useMemo(() => {
      return props.oldDevice;
    }, [props])
  });

  
  const { register, control, handleSubmit, formState, reset } = form;
  const { errors } = formState;
  
  const { fields, append, remove } = useFieldArray({
    name: "interfaces",
    control
  });
  
  useEffect(() => {
    reset(props.oldDevice);
  }, [props.oldDevice, reset]);

  const onSubmit = async (data: FormValues) => {
    let response = null;
    try {
      response = await updateDevice(props.deviceId, data);
    } catch (error) {
      console.error(`Error occured while creating new device: ${error}`);
    } finally {
      if (response) {
        revalidateDevices();
        redirect("/manage-devices");
      }
    }
  }

  return (
    <div className="form-container create-wrap">
      <h1 className="form-header">Modify device</h1>
      <form id="create-form" onSubmit={handleSubmit(onSubmit)}>
        <div className="input-container form-elem shorter">
          <label htmlFor="name-input">Device name</label>
          <input id="name-input" type="text" {...register("name")}/>
          <p style={{color: "red"}}>{errors.name?.message}</p>
        </div>

        <div className="input-container form-elem shorter">
          <label htmlFor="device-type-select">Device type</label>
          <select id="device-type-select" style={{cursor: "pointer"}} {...register("device_type")}>
            <option value={`${DeviceType.ROUTER}`}>{DeviceType.ROUTER}</option>
            <option value={`${DeviceType.SWITCH}`}>{DeviceType.SWITCH}</option>
          </select>
        </div>

        <div className="input-container form-elem shorter">
          <label htmlFor="rack-id-input">Rack id</label>
          <select id="rack-id-input" form="create-form" {...register("rack_id")}>
            {props.groups.map((group, i) => (
              <option key={i} value={group.lab_group_number}>
                {group.lab_group_number}
              </option>
            ))}
          </select>
        </div>

        <div className="add-interface form-elem shorter">
          <label>List of interfaces</label>
          <button type="button" className="add-iface-button add-button" onClick={() => append({
            type: InterfaceType.FA,
            value: ""
          })}>
            Add
          </button>
        </div>

        <div id="interfaces">
          {fields.map((field, i) => {
            return (
              <div key={i} className="interface-list">
                <select style={{cursor: "pointer"}} {...register(`interfaces.${i}.type`)}>
                  {Object.values(InterfaceType).map((iface, j) => (
                    <option key={j} value={iface}>{iface}</option>
                  ))}
                </select>
                <input type="text" {...register(`interfaces.${i}.value`)} required/>
                {i >= 0 && (
                  <button type="button" className="remove-button" onClick={() => remove(i)}>
                    Remove
                  </button>
                )}
              </div>
            );
          })}
          {<p className="iface-error" style={{color: "red"}}>{errors.interfaces?.message}</p>}
        </div>

        <div className="single-submit-container">
          <input type="submit" className="submit-button submit-device"/>
        </div>
      </form>
    </div>
  );
}

export default ModifyDeviceForm;