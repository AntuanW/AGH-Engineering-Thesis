import React, {useState, useEffect} from "react";
import { PythonMessage } from "../interfaces/DemoInterface";
import { fetchMessageService } from "../services/DemoService";


const DemoComponent = () => {
  const [pythonMessage, setPythonMessage] = useState<PythonMessage>();

  useEffect(() => {
    const fetchMessage = async () => {
      try {
        const data: PythonMessage = await fetchMessageService();
        setPythonMessage(data);
      } catch(error) {
        console.error(error);
      }
    }

    fetchMessage();
  }, [setPythonMessage]);

  return (
    <div>
      <h1>Ale to będzie hulać</h1>
      <p>Wiadomość od FastApi: {pythonMessage?.Hello}</p>
    </div>
  );
}


export default DemoComponent;