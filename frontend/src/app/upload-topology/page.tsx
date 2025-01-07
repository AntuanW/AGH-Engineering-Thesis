import ConfigurationForm from "../(components)/upload-forms/configuration-form/configurationForm";
import InstructionForm from "../(components)/instruction-form/instructionForm";
import UploadForm from "../(components)/upload-forms/upload-topology-form/uploadForm";
import { Group } from "../(interfaces)/common/Group";
import { IndexDto } from "../(interfaces)/common/IndexDto";
import { getIndexDto } from "../(services)/IndexDtoService";

import "./page.css";

const UploadTopology = async () =>  {
  const indexDto: IndexDto = await getIndexDto();
  const sortedGroups: Group[] = indexDto.groups.sort((a, b) => (a.lab_group_number - b.lab_group_number));

  return (
    <div className="forms-wrapper">
      <UploadForm groups={sortedGroups}/>
      <InstructionForm 
        topologies={indexDto.topologies}
        groups={indexDto.groups}
      />
      <ConfigurationForm
        groups={sortedGroups}
        mappings={indexDto.mappings}
        topologies={indexDto.topologies}
      />
    </div>
  );
}

export default UploadTopology;