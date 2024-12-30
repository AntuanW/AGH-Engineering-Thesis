"use client"
import { Group } from "@/app/(interfaces)/common/Group";
import { useForm, useFieldArray } from "react-hook-form";

import "./downloadForm.css";
import { downloadTopology } from "@/app/(services)/TopologyDownloadService";

interface Props {
  groups: Group[];
}

interface FormValues {
  lab_group: number;
  lab_name: string;
  devices: {
    ip_address?: string;
    port?: number;
  }[];
}

const DownloadTopologyForm = (props: Props) => {
  const form = useForm<FormValues>();
  const { register, control, handleSubmit, formState, watch, resetField } = form;
  const { errors } = formState;

  const { fields, append } = useFieldArray({
    name: "devices",
    control
  });

  const getCurrentGroup = () => {
    return props.groups.find((group) => group.lab_group_number == watch("lab_group"));
  }

  const onGroupChange = () => {
    resetField("devices", {defaultValue: []});
  }

  const onSubmit = async (data: FormValues) => {
    try {
      const blobResponse = await downloadTopology(data);
      const url = window.URL.createObjectURL(blobResponse);
      const link = document.createElement('a');
      link.href = url;
      link.download = `topology-group-${data.lab_group}`;
      link.click();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error(`Failed to download configurations: ${error}`);
    }
  }

  return (
    <div className="form-container">
      <h1 className="form-header">Download topology</h1>
      <form id="download-form" onSubmit={handleSubmit(onSubmit)}>
        <label htmlFor="group-select">Lab group</label> 
        <select  id="group-select" form="download-form" {...register("lab_group")} onChange={onGroupChange}>
        {props.groups.map((group, i) => {
          return (
            <option key={i} className="group-option" value={group.lab_group_number}>
              {group.lab_group_number}
            </option>
          );
        })}
        </select>

        <label htmlFor="lab-name">Lab name</label>
        <input id="lab-name" type="text" {...register("lab_name", {
          required: "Lab name is required!"
        })}/>
        <p style={{color: "red"}}>{errors.lab_name?.message}</p>

        <div>
          <label>List of connected devices</label>
          <div>
            {fields.map((field, i) => {
              const currentGroup: Group | undefined = getCurrentGroup();
              return (
                <div key={field.id} className="form-control">
                  <input 
                    type="text" {...register(`devices.${i}.ip_address`)}
                    value={currentGroup?.rack.config_port_ip_address}
                    disabled/>
                  <select {...register(`devices.${i}.port`)}>
                    {currentGroup?.rack.config_ports.map((port, j) => (
                      <option key={j} value={port}>{port}</option>
                    ))}
                  </select>
                </div>
              );
            })}
            <button type="button" onClick={() => append({
              ip_address: getCurrentGroup()?.rack.config_port_ip_address,
              port: getCurrentGroup()?.rack.config_ports[0]
            })}>Add connection</button>
          </div>
        </div>

        <div className="submit-container">
          <input type="submit" className="submit-button" defaultValue="Submit"/>
        </div>
      </form>
    </div>
  );  
}

export default DownloadTopologyForm;