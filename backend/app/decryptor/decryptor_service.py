from backend.app.resources.FileService import *
import os
from pathlib import Path


class PktDecryptor:
    # TODO: Error management
    JAR_PATH = Path(__file__).parent.joinpath("PktDecryptor/PktDecryptor.jar")

    @staticmethod
    def encrypt_file(xml_file_path: str | Path, output_file_path: str | Path, verbose=True):
        cmd = f"java -jar {PktDecryptor.JAR_PATH} -e {str(xml_file_path)} {str(output_file_path)}"
        if verbose:
            print(cmd)
        os.system(cmd)

    @staticmethod
    def decrypt_file(pkt_file_path: str | Path, output_file_path: str | Path, verbose=True):
        cmd = f"java -jar {PktDecryptor.JAR_PATH} -d {str(pkt_file_path)} {str(output_file_path)}"
        if verbose:
            print(cmd)
        os.system(cmd)


class DecryptorService:
    def __init__(self, decryptor: PktDecryptor, file_service: FileService):
        self.decryptor = decryptor
        self.file_service = file_service

    def decrypt_pkt(self, name: str):
        input_path = self.file_service.get_path(name, FileType.PKT)
        output_path = self.file_service.get_path(name, FileType.XML)
        self.decryptor.decrypt_file(input_path, output_path)

    def encrypt_xml(self, name: str):
        input_path = self.file_service.get_path(name, FileType.XML)
        output_path = self.file_service.get_path(name, FileType.PKT)
        self.decryptor.encrypt_file(input_path, output_path)