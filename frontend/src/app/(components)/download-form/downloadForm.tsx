"use client"
import { Group } from "@/app/(interfaces)/common/Group";
import { useForm, useFieldArray } from "react-hook-form";
import { downloadTopology } from "@/app/(services)/TopologyDownloadService";
import { ProgressState } from "@/app/(interfaces)/common/ProgressState";
import { useState } from "react";

import "./downloadForm.css";

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
  const { NOT_READY, IN_PROGRESS, READY } = ProgressState;
  const [color, setColor] = useState(NOT_READY);

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
    setColor(NOT_READY);
  }

  const onSubmit = async (data: FormValues) => {
    try {
      setColor(IN_PROGRESS);
      const blobResponse = await downloadTopology(data);
      setColor(READY);
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
        <div className="form-elem shorter">
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
        </div>
        
        <div className="form-elem shorter">
          <label htmlFor="lab-name">Lab name</label>
          <input id="lab-name" type="text" {...register("lab_name", {
            required: "Lab name is required!"
          })}/>
          <p style={{color: "red"}}>{errors.lab_name?.message}</p>
        </div>

        <div className="form-elem connections">
          <div className="add-connection">
            <label>List of connected devices</label>
            <button type="button" className="add-button" onClick={() => append({
              ip_address: getCurrentGroup()?.rack.config_port_ip_address,
              port: getCurrentGroup()?.rack.config_ports[0]
            })}>Add</button>
          </div>
          <div id="connections">
            {fields.map((field, i) => {
              const currentGroup: Group | undefined = getCurrentGroup();
              return (
                <div key={field.id} className="form-control">
                  <input
                    style={{cursor: "not-allowed", width: "45%", textAlign: "center"}}
                    type="text" {...register(`devices.${i}.ip_address`)}
                    value={currentGroup?.rack.config_port_ip_address}
                    disabled/>
                  <select style={{cursor: "pointer", width: "30%"}} {...register(`devices.${i}.port`)}>
                    {currentGroup?.rack.config_ports.map((port, j) => (
                      <option key={j} value={port}>{port}</option>
                    ))}
                  </select>
                </div>
              );
            })}
          </div>
        </div>

        <div className="submit-container">
          <input type="submit" className="submit-button"/>
          <div className="circle" style={{background: color}}></div>
        </div>
      </form>
    </div>
  );  
}

export default DownloadTopologyForm;