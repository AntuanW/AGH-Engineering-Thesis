"use client"
import { Group } from "@/app/(interfaces)/common/Group";
import { downloadInstruction, extractTopologyDetails, mapDevicesForGroups, uploadTopologyFile } from "@/app/(services)/TopologyUploadService";
import { useState } from "react";
import { ExtractResponse, UploadResponse } from "./responses";

interface Props {
  groups: Group[];
}

const UploadForm = (props: Props) => {
  const [file, setFile] = useState<File | null>(null);

  const uploadFile = async (formData: FormData) => {
    if (!file) {
      return;
    }

    const fileData = new FormData();
    fileData.append("file", file);

    try {
      const fileResponse: UploadResponse = await uploadTopologyFile(fileData);
      if (fileResponse.xml_id) {
        extractTopology(formData, fileResponse.xml_id);
      }
    } catch (error) {
      console.error(`Failed to upload file: ${error}`);
    }
  }

  const extractTopology = async (formData: FormData, xmlId: string) => {
    try {
      const extractResponse: ExtractResponse = await extractTopologyDetails(xmlId);
      if (extractResponse.topology_id) {
        mapDevices(formData, extractResponse.topology_id);
      }
    } catch (error) {
      console.error(`Failed to extract topology details: ${error}`);
    }
  }

  const mapDevices = async (formData: FormData, topologyId: string) => {
    const labGroups: FormDataEntryValue[] = formData.getAll('lab-group');
    try {
      const mappingResponse = await mapDevicesForGroups(topologyId, labGroups);
      if (mappingResponse) {
        handleDownload(topologyId);
      }
    } catch (error) {
      console.error(`Failed to map topology: ${error}`);
    }
  }

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

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setFile(event.target.files[0]);
    }
  }

  const handleFormSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    uploadFile(formData);
  };

  return (
    <form id="upload-pkt" onSubmit={handleFormSubmit}>
      <input type="file" onChange={handleFileChange}/>
      <ul>
      {props.groups.map((group, i) => {
        return (
          <li key={i}>
            <span>{group.lab_group_number}</span>
            <input type="checkbox" value={group.lab_group_number} name="lab-group"/>
          </li>
        );
      })}
      </ul>
      <input type="submit" className="button"/>
    </form>
  );
}

export default UploadForm;