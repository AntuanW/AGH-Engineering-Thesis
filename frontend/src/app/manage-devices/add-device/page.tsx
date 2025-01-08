import DeviceForm from "@/app/(components)/device-forms/add-device-form/deviceForm";
import { Group } from "@/app/(interfaces)/common/Group";
import { IndexDto } from "@/app/(interfaces)/common/IndexDto";
import { getIndexDto } from "@/app/(services)/IndexDtoService";

const AddDevice = async () => {
  const getSortedGroups = async () => {
    const indexDto: IndexDto = await getIndexDto();
    return indexDto.groups.sort((a, b) => (a.lab_group_number - b.lab_group_number));
  }

  const sortedGroups: Group[] = await getSortedGroups();

  return (
    <DeviceForm groups={sortedGroups}/>  
  );
}

export default AddDevice;