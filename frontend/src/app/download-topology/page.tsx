import DownloadTopologyForm from "../(components)/download-form/downloadForm";
import { Group } from "../(interfaces)/common/Group";
import { IndexDto } from "../(interfaces)/common/IndexDto";
import { getIndexDto } from "../(services)/IndexDtoService";

import "./page.css";

const DownloadTopology = async () =>  {
  const indexDto: IndexDto = await getIndexDto();
  const sortedGroups: Group[] = indexDto.groups.sort((a, b) => (a.lab_group_number - b.lab_group_number));


  return (
    <div className="forms-wrapper">
      <DownloadTopologyForm groups={sortedGroups}/>
    </div>
  );
}

export default DownloadTopology;