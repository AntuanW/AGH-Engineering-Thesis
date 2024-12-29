import UploadForm from "../(components)/upload-form/uploadForm";
import { Group } from "../(interfaces)/common/Group";
import { IndexDto } from "../(interfaces)/common/IndexDto";
import { getIndexDto } from "../(services)/IndexDtoService";

const UploadTopology = async () =>  {
  const indexDto: IndexDto = await getIndexDto();
  const sortedGroups: Group[] = indexDto.groups.sort((a, b) => (a.lab_group_number - b.lab_group_number));

  return (
    <UploadForm groups={sortedGroups}/>
  );
}

export default UploadTopology;