from app.repository.decrypted_xml_repository import DecryptedXMLRepository
from app.resources.FileService import *
import os
import logging
import xmltodict
from pathlib import Path
from fastapi import Depends

from app.running_config.exceptions.config_extraction_exceptions import XmlOpenException


class PktDecryptor:
    # TODO: Error management
    JAR_PATH = Path(__file__).parent.joinpath("PktDecryptor/PktDecryptor.jar")

    @staticmethod
    def encrypt_file(xml_file_path: str | Path, output_file_path: str | Path, verbose=True):
        cmd = f"java -jar {PktDecryptor.JAR_PATH} -e {str(xml_file_path)} {str(output_file_path)}"
        if verbose:
            logging.info(cmd)
        os.system(cmd)

    @staticmethod
    def decrypt_file(pkt_file_path: str | Path, output_file_path: str | Path, verbose=True):
        cmd = f"java -jar {PktDecryptor.JAR_PATH} -d {str(pkt_file_path)} {str(output_file_path)}"
        if verbose:
            logging.info(cmd)
        os.system(cmd)


class DecryptorService:
    def __init__(
            self,
            decryptor: PktDecryptor = Depends(PktDecryptor),
            file_service: FileService = Depends(FileService),
            decrypted_xml_repository: DecryptedXMLRepository = Depends(DecryptedXMLRepository)
    ):
        self.decryptor = decryptor
        self.file_service = file_service
        self.decrypted_xml_repository = decrypted_xml_repository

    def decrypt_pkt(self, name: str):
        input_path = self.file_service.get_path(name, FileType.PKT)
        output_path = self.file_service.get_path(name, FileType.XML)
        self.decryptor.decrypt_file(input_path, output_path)

    def encrypt_xml(self, name: str):
        input_path = self.file_service.get_path(name, FileType.XML)
        output_path = self.file_service.get_path(name, FileType.PKT)
        self.decryptor.encrypt_file(input_path, output_path)

    def save_xml_to_database(self, xml_path: str | Path) -> str:
        try:
            with open(xml_path, "r") as file:
                xml = file.read()
        except OSError as exc:
            logging.error(f"Failed to read {xml_path}")
            raise XmlOpenException(f"Failed to open/read {xml_path} - {exc}")

        xml_dict: dict = xmltodict.parse(xml)
        xml_id: str = self.decrypted_xml_repository.insert(xml_dict)

        return xml_id
