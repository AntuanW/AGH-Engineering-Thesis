import { ExtractResponse, UploadResponse } from "../(components)/upload-form/responses";

export const uploadTopologyFile = async (fileData: FormData): Promise<UploadResponse> => {
  return await fetch("http://localhost:8000/config_upload/upload_pkt", {
    method: "POST",
    body: fileData
  })
    .then((response) => response.json())
    .then((data: UploadResponse) => data)
    .catch((error) => {
      throw new Error(`HTTP POST error while uploading pkt file. Status: ${error}`)
    });
}

export const extractTopologyDetails = async (topologyId: string): Promise<ExtractResponse> => {
  return await fetch(`http://localhost:8000/config_upload/extract_xml/${topologyId}`)
    .then((response) => response.json())
    .then((data: ExtractResponse) => data)
    .catch((error) => {
      throw new Error(`HTTP GET error while extracting topology details. Status: ${error}`)
    });
}

export const mapDevicesForGroups = async (topologyId: string, labGroups: FormDataEntryValue[]) => {
  let groupIds: string = "";
  if (labGroups) {
    labGroups = labGroups.map((id) => `group_id=${id}`);
    groupIds = `?${labGroups.join("&")}`; 
  }

  return await fetch(`http://localhost:8000/config_upload/topologies/${topologyId}/mapping${groupIds}`)
    .then((response) => response.json())
    .then((data) => data)
    .catch((error) => {
      throw new Error(`HTTP GET error while mapping topology. Status: ${error}`)
    });
}