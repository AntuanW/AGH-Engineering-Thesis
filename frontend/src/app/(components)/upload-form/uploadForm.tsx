"use client"
import { Group } from "@/app/(interfaces)/common/Group";
import { downloadInstruction, extractTopologyDetails, mapDevicesForGroups, uploadTopologyFile } from "@/app/(services)/TopologyUploadService";
import { ExtractResponse, UploadResponse } from "./responses";
import { revalidateIndexDto } from "@/app/(server-actions)/IndexDtoRevalidation";
import { ProgressState } from "@/app/(interfaces)/common/ProgressState";
import { useState } from "react";

import "./uploadForm.css";

interface Props {
  groups: Group[];
}

const UploadForm = (props: Props) => {
  const {NOT_READY, IN_PROGRESS, READY} = ProgressState;
  const [color, setColor] = useState(NOT_READY);

  const [file, setFile] = useState<File | null>(null);
  const [isMapped, setIsMapped] = useState(false);

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
        setColor(IN_PROGRESS);
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
        setIsMapped(true);
        setColor(READY);
        revalidateIndexDto();
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

  const onCheckBoxChange = () => {
    if (isMapped) {
      setIsMapped(false);
      setColor(NOT_READY);
    }
  }

  return (
    <div className="form-container">
      <h1 className="form-header">Upload topology</h1>
      <form id="upload-pkt" onSubmit={handleFormSubmit}>
        <input type="file" onChange={handleFileChange}/>
        <ul className="check-box-group">
        {props.groups.map((group, i) => {
          return (
            <li key={i} className="group-item">
              <input
                id={`checkbox-group-${group.lab_group_number}`} 
                type="checkbox" value={group.lab_group_number}
                name="lab-group" className="checkbox" 
                onChange={onCheckBoxChange} defaultChecked
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

export default UploadForm;