from pathlib import Path
import tempfile


class FileService:
    TEMP_PATH = Path(tempfile.gettempdir())

    def save_file(self, content: bytes, name: str, force_overwrite=False) -> None:
        path = self.TEMP_PATH.joinpath(name)
        if path.is_file() and not force_overwrite:
            raise FileExistsError(f"File {name} already exists.")
        with open(path, "wb") as file:
            file.write(content)

    def read_file(self, name: str) -> bytes:
        path = self.TEMP_PATH.joinpath(name)
        if not path.is_file():
            raise FileNotFoundError(f"File {name} does not exist.")
        with open(path, "rb") as file:
            return file.read()

    def check_file_exists(self, name: str):
        path = self.TEMP_PATH.joinpath(name)
        return path.is_file()

    def get_file_path(self, name: str):
        return self.TEMP_PATH.joinpath(name)
