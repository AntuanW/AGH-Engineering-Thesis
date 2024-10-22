from enum import Enum
from pathlib import Path


class FileType(Enum):
    XML = 1
    PKT = 2
    OTHER = 3


class FileService:
    RESOURCES_PATH = Path(__file__).parent

    def strip_name(self, name: str):
        """
        Removes the .pkt or .xml extension from the filename
        """
        if name.endswith(".pkt") or name.endswith(".xml"):
            return name[:-4]
        return name

    def check_file_exists(self, name: str, file_type: FileType):
        """
        Checks if the file with given name and type exists.
        """
        path = self.get_path(name, file_type)
        return path.is_file()

    def get_path(self, name: str, file_type: FileType):
        """
        Returns the full path to a file with given name and type.
        The files are stored under resources/[xml | pkt | configs | ...]
        """
        name = self.strip_name(name)
        match file_type:
            case FileType.XML:
                return self.RESOURCES_PATH.joinpath("xml").joinpath(name + ".xml")
            case FileType.PKT:
                return self.RESOURCES_PATH.joinpath("pkt").joinpath(name + ".pkt")
            case _:
                return self.RESOURCES_PATH.joinpath("configs").joinpath(name)

    def save_xml(self, name: str, content: str) -> None:
        path = self.get_path(name, FileType.XML)
        with open(path, "w") as file:
            file.write(content)

    def read_xml(self, name: str) -> str:
        path = self.get_path(name, FileType.XML)
        with open(path, "r") as file:
            return file.read()

    def save_pkt(self, name: str, content: bytes) -> None:
        path = self.get_path(name, FileType.PKT)
        with open(path, "wb") as file:
            file.write(content)

    def read_pkt(self, name: str) -> bytes:
        path = self.get_path(name, FileType.PKT)
        with open(path, "rb") as file:
            return file.read()
