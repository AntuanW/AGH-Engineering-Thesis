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

