import { IndexDto } from "../(interfaces)/common/IndexDto";

export const getIndexDto = async (): Promise<IndexDto> => {
  return await fetch("http://localhost:8000/config_upload/index_dto")
    .then((response) => response.json())
    .then((data: IndexDto) => data)
    .catch((error) => {
      throw new Error(`HTTP GET error while retrieving index dto. Status: ${error}`);
    });
}