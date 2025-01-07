"use client"
import { Group } from "@/app/(interfaces)/common/Group";
import { Mapping } from "@/app/(interfaces)/common/Mapping";
import { Topolgy } from "@/app/(interfaces)/common/Topology";
import { configureDevices } from "@/app/(services)/TopologyUploadService";
import { ProgressState } from "@/app/(interfaces)/common/ProgressState";
import { useState } from "react";

import "./configurationForm.css";

interface Props {
  groups: Group[];
  mappings: Mapping[];
  topologies: Topolgy[];
}

const ConfigurationForm = (props: Props) => {
  const { NOT_READY, IN_PROGRESS, READY } = ProgressState;
  const [color, setColor] = useState(NOT_READY);

  const [areConfigured, setAreConfigured] = useState(false);

  const onRadioChange = () => {
    if (areConfigured) {
      setAreConfigured(false);
      setColor(NOT_READY);
    }
  }

  const handleFormSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const groupId = formData.get("lab-group")?.toString();
    const mappingId = formData.get("config-select")?.toString();

    if (mappingId && groupId) {
      try {
        setColor(IN_PROGRESS);
        await configureDevices(mappingId, groupId)
        setAreConfigured(true);
        setColor(READY);
      } catch (error) {
        console.log(`Something went wrong with upload: ${error}`);
      }
    }
    return;
  }
  
  return (
    <div className="form-container">
      <h1 className="form-header">Configure devices</h1>
      <form id="config-form" onSubmit={handleFormSubmit}>
        <select id="config-select" name="config-select" form="config-form">
        {props.mappings.map((mapping, i) => {
          return (
            <option key={i} className="config-option" value={mapping._id}>{mapping.name}</option>
          );
        })}
        </select>
        <ul className="check-box-group">
        {props.groups.map((group, i) => {
          return (
            <li key={i} className="group-item">
              <input 
                id={`group${group.lab_group_number}`} 
                type="radio" value={group.lab_group_number} 
                name="lab-group" className="radio"
                onClick={onRadioChange}
              />
              <label htmlFor={`group${group.lab_group_number}`}>{group.lab_group_number}</label>
            </li>
          );
        })}
        </ul>
        <div className="submit-container">
          <input type="submit" className="submit-button"/>
          <div className="circle" style={{background: color}}></div>
        </div>
      </form>
    </div>
  );
}

export default ConfigurationForm;