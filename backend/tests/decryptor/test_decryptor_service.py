import xml.etree.ElementTree as ET
from pathlib import Path
from app.decryptor.decryptor_service import PktDecryptor

DIR_PATH = Path(__file__).parent

def test_decrypt():
        PktDecryptor.decrypt_file(DIR_PATH.joinpath("tracer822.pkt"), DIR_PATH.joinpath("result.xml"), verbose=False)

        tree = ET.parse(DIR_PATH.joinpath("result.xml"))
        root = tree.getroot()

def test_decrypt_corrupt():
        PktDecryptor.decrypt_file(DIR_PATH.joinpath("tracer822_corrupt.pkt"), DIR_PATH.joinpath("result.xml"), verbose=False)
        # TODO: AssertRaises()


def test_encrypt():
        PktDecryptor.encrypt_file(DIR_PATH.joinpath("xml822.xml"), DIR_PATH.joinpath("result.pkt"), verbose=False)

def test_clean():
    try:
        Path(DIR_PATH.joinpath("result.xml")).unlink()
        Path(DIR_PATH.joinpath("result.pkt")).unlink()
    except FileNotFoundError:
        pass