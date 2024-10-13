import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from backend.app.parser.PktDecryptor import PktDecryptor

DIR_PATH = Path(__file__).parent

class TestPktDecryptor(unittest.TestCase):
    def test_decrypt(self):
        PktDecryptor.decrypt_file(DIR_PATH.joinpath("tracer822.pkt"), DIR_PATH.joinpath("result.xml"), verbose=False)

        tree = ET.parse(DIR_PATH.joinpath("result.xml"))
        root = tree.getroot()

    def test_decrypt_corrupt(self):
        PktDecryptor.decrypt_file(DIR_PATH.joinpath("tracer822_corrupt.pkt"), DIR_PATH.joinpath("result.xml"), verbose=False)
        # TODO: AssertRaises()

    def test_encrypt(self):
        PktDecryptor.encrypt_file(DIR_PATH.joinpath("xml822.xml"), DIR_PATH.joinpath("result.pkt"), verbose=False)