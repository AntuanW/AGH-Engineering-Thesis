interface FormValues {
  lab_group: number;
  lab_name: string;
  devices: {
    ip_address?: string;
    port?: number;
  }[];
  }

export const downloadTopology = async (requestBody: FormValues) => {
  return await fetch("http://localhost:8000/config_download/download_configs", {
    method: "POST",
    body: JSON.stringify(requestBody),
    headers: {
			'content-type': 'application/json;charset=UTF-8',
		}
  })
  .then((response) => response.blob())
  .catch((error) => {
    throw new Error(`HTTP POST error while downloading configurations. Status: ${error}`)
  });
}