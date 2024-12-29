"use client"
import { Group } from "@/app/(interfaces)/common/Group";
import { Mapping } from "@/app/(interfaces)/common/Mapping";
import { Topolgy } from "@/app/(interfaces)/common/Topology";
import { configureDevices } from "@/app/(services)/TopologyUploadService";

interface Props {
  groups: Group[];
  mappings: Mapping[];
  topologies: Topolgy[];
}

const ConfigurationForm = (props: Props) => {
  const handleFormSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const groupId = formData.get("lab-group")?.toString();
    const topologyId = formData.get("config-select")?.toString();

    if (topologyId && groupId) {
      await configureDevices(topologyId, groupId)
    }
    return;
  }
  
  return (
    <form id="config-form" onSubmit={handleFormSubmit}>
      <select id="config-select" name="config-select" form="config-form">
      {props.mappings.map((mapping, i) => {
        return (
          <option key={i} value={mapping._id}>{mapping.name}</option>
        );
      })}
      </select>
      <ul>
      {props.groups.map((group, i) => {
        return (
          <li key={i}>
            <span>{group.lab_group_number}</span>
            <input type="radio" value={group.lab_group_number} name="lab-group"/>
          </li>
        );
      })}
      </ul>
      <input type="submit" className="button"/>
    </form>
  );
}

export default ConfigurationForm;