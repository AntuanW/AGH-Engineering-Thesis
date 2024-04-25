import { PythonMessage } from "../interfaces/DemoInterface";

export const fetchMessageService = async ()  => {
  const tmpUrl = "http://127.0.0.1:8000/";
  
  try {
    const response = await fetch(tmpUrl);
    const data: PythonMessage = await response.json();
    return data;
  } catch {
    console.error("Error occured while fetching hello message!");
  }

  const data: PythonMessage = {Hello: ""};
  return data;
}