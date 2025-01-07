"use client"
import { Group } from "@/app/(interfaces)/common/Group"
import { Topolgy } from "@/app/(interfaces)/common/Topology";
import { downloadInstruction } from "@/app/(services)/TopologyUploadService";

import "./instructionForm.css";

interface Props {
  groups: Group[];
  topologies: Topolgy[];
}

const InstructionForm = (props: Props) => {
  const handleDownload = async (topologyId: string) => {
    try {
      const blobResponse = await downloadInstruction(topologyId);
      const url = window.URL.createObjectURL(blobResponse);
      const link = document.createElement('a');
      link.href = url;
      link.download = `instruction-${topologyId}`;
      link.click();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error(`Failed to download instructions: ${error}`);
    }
  }

  const handleFormSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const topologyId = formData.get(`instruction-select`)?.toString();
    console.log(topologyId);
    if (topologyId) {
      handleDownload(topologyId);
    }
  }

  return (
    <div className="form-container">
      <h1 className="form-header">Download instruction</h1>
      <form id="instruction-form" onSubmit={handleFormSubmit}>
        <select name="instruction-select" id="instruction-select" form="instruction-form">
          {props.topologies.map((topology, i) => (
            <option key={i} className="instruction-option" value={topology._id}>
              {topology.name}
            </option>
          ))}
        </select>

        <div className="submit-container only-submit">
          <input type="submit" className="submit-button"/>
        </div>
      </form>
    </div>
  );
}

export default InstructionForm;