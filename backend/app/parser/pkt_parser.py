import twofish


class TwoFishCBC:
    """
    A CBC (Cipher Block Chaining) extension for the TwoFish block encryption algorithm
    """
    BLOCK_SIZE = 16

    """
    :param key: Encryption key
    :param init_vector: Initialization Vector (a seed for the blockchain)
    """
    def __init__(self, key: bytes, init_vector: bytes):
        self.encryptor = twofish.Twofish(key)
        self.init_vector = init_vector

    """
    Bitwise XOR of two arrays
    """
    @staticmethod
    def _xor(b1: bytearray | bytes, b2: bytearray | bytes):
        return bytes(a ^ b for (a, b) in zip(b1, b2))

    """
    Replaces a fragment of arr with new at index start 
    """
    @staticmethod
    def _replace(arr: bytearray, start: int, new: bytearray | bytes):
        for i in range(len(new)):
            arr[start + i] = new[i]

    def _encrypt_block(self, block: bytes):
        return self.encryptor.encrypt(block)

    def _decrypt_block(self, block: bytes):
        return self.encryptor.decrypt(block)

    """
    Encrypts an array in-place using TwoFish algorithm by CBC scheme
    :param plain: Plaintext array of bytes to encrypt
    """
    def encrypt(self, plain: bytearray):
        plain += bytearray([0]) * (self.BLOCK_SIZE - len(plain) % self.BLOCK_SIZE)
        print(len(plain))
        start_index = 0
        cipher_block = self.init_vector
        while start_index < len(plain):
            xor_plain_block = self._xor(plain[start_index: start_index + self.BLOCK_SIZE], cipher_block)
            cipher_block = self._encrypt_block(xor_plain_block)
            self._replace(plain, start_index, cipher_block)
            start_index += self.BLOCK_SIZE

    """
    Decrypts an array in-place using TwoFish algorithm by CBC scheme
    :param cipher: Ciphertext array of bytes to decrypt
    """
    def decrypt(self, cipher: bytearray):
        start_index = len(cipher) - 16
        while start_index >= 16:
            cipher_block = bytes(cipher[start_index: start_index + 16])
            xor_plain_block = self._decrypt_block(cipher_block)
            plain_block = self._xor(xor_plain_block, cipher[start_index - 16: start_index])
            self._replace(cipher, start_index, plain_block)
            start_index -= 16

        cipher_block = bytes(cipher[0: 16])
        xor_plain_block = self._decrypt_block(cipher_block)
        plain_block = self._xor(xor_plain_block, self.init_vector)
        self._replace(cipher, start_index, plain_block)


class PktParser:
    """
    A wrapper for an algorithm, which decrypts and encrypts various types of
    PacketTracer files to and from XML format
    """

    class StageTwoKey:
        """
        Wraps a Key - Initialization Vector pair used in Step 2 of decryption.
        The keys are 16 copies of the same byte in every case.
        """
        key: bytes
        vector: bytes

        def __init__(self, key_seed: int, vector_seed: int):
            self.key = bytes(key_seed) * 16
            self.vector = bytes(vector_seed) * 16

    STAGE_TWO_KEYS = {
        "pta": StageTwoKey(0xAB, 0xCD),
        "pkc": StageTwoKey(0xAB, 0x23),
        "pts": StageTwoKey(0x89, 0x10),
        "pkt": StageTwoKey(0x89, 0x10),
        "log1": StageTwoKey(0xAB, 0xBE),
        "log2": StageTwoKey(0xBA, 0xBE),
    }

    buffer: bytearray

    """
    Stage 1 of decryption.
    The buffer is XORed with itself in a weird way.
    TODO: Test this
    """
    def unpack_stage_one(self):
        length = len(self.buffer)
        k = length % 256
        for i in range(len(self.buffer)):
            ch = self.buffer[-(1 + i)]
            a = (k * (i % 255)) % 255
            c = (length - a) % 255
            c ^= ch
            self.buffer[i] = c

    """
    Stage 2 of decryption
    The buffer is decrypted using the CBC-TwoFish algorithm
    """
    def unpack_stage_two(self):
        pass

    def decode(self, file_path: str):
        with open(file_path, "rb") as file:
            self.buffer = bytearray(file.read())


if __name__ == '__main__':
    fish = TwoFishCBC(b'xyxyxyxyxyxyxyxy', b'abababababababab')
    s = "tylko pis i konfederacja"
    b = bytearray(s.encode("ascii"))
    fish.encrypt(b)
    print(b)
    fish.decrypt(b)
    print(b)

    s = b"CBC Mode Test\x03\x03\x03"
    s = TwoFishCBC._xor(s, bytes.fromhex("05C9428085EE3F34D7ECE73C5628F605"))
    print(s)
    fish = twofish.Twofish(bytes.fromhex("6B990E620635B4C36A1B737487CEAD8D"))
    enc = fish.encrypt(s)
    print(enc)  # should be bcd4...