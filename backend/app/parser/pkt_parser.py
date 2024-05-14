import twofish


class TwoFishKeyVectorPair:
    """
    Wraps a Key - Initialization Vector pair used in Step 2 of PacketTracer file decryption.
    The keys are 16 copies of the same byte in every case.
    """
    key: bytes
    vector: bytes

    def __init__(self, key_seed: int, vector_seed: int):
        self.key = bytes([key_seed]) * 16
        self.vector = bytes([vector_seed]) * 16


class TwoFishCBC:
    """
    A CBC (Cipher Block Chaining) extension for the TwoFish block encryption algorithm
    """
    BLOCK_SIZE = 16

    """
    :param key: Encryption key
    :param init_vector: Initialization Vector (a seed for the blockchain)
    """
    def __init__(self, key_vector_pair: TwoFishKeyVectorPair):
        self.encryptor = twofish.Twofish(key_vector_pair.key)
        self.init_vector = key_vector_pair.vector

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
        # Add padding so that len(plain) % 16 == 0
        plain += bytearray([0]) * (self.BLOCK_SIZE - len(plain) % self.BLOCK_SIZE)
        start_index = 0
        # Set previous output to IV
        cipher_block = self.init_vector
        while start_index < len(plain):
            # Cut out 16 bytes of plaintext
            plain_block = plain[start_index: start_index + self.BLOCK_SIZE]
            # XOR it with previous output
            xor_plain_block = self._xor(plain_block, cipher_block)
            # Encrypt it with TwoFish, this is the new output
            cipher_block = self._encrypt_block(xor_plain_block)
            # Put encrypted block back into the array
            self._replace(plain, start_index, cipher_block)
            # Move to the next block
            start_index += self.BLOCK_SIZE

    """
    Decrypts an array in-place using TwoFish algorithm by CBC scheme
    :param cipher: Ciphertext array of bytes to decrypt
    """
    def decrypt(self, cipher: bytearray):
        # Reverse the encryption process, start from the back
        start_index = len(cipher) - self.BLOCK_SIZE
        while start_index >= self.BLOCK_SIZE:
            # Cut out a block of ciphertext
            cipher_block = bytes(cipher[start_index: start_index + self.BLOCK_SIZE])
            # Decrypt using TwoFish
            xor_plain_block = self._decrypt_block(cipher_block)
            # Un-XOR using the previous ciphered block
            plain_block = self._xor(xor_plain_block, cipher[start_index - self.BLOCK_SIZE: start_index])
            # Put the plaintext block back into array
            self._replace(cipher, start_index, plain_block)
            start_index -= self.BLOCK_SIZE

        # Perform last iteration using IV as "previous" ciphertext
        cipher_block = bytes(cipher[0: self.BLOCK_SIZE])
        xor_plain_block = self._decrypt_block(cipher_block)
        plain_block = self._xor(xor_plain_block, self.init_vector)
        self._replace(cipher, start_index, plain_block)


class PktParser:
    """
    A wrapper for an algorithm, which decrypts and encrypts various types of
    PacketTracer files to and from XML format
    """

    STAGE_TWO_KEYS = {
        "pta": TwoFishKeyVectorPair(0xAB, 0xCD),
        "pkc": TwoFishKeyVectorPair(0xAB, 0x23),
        "pts": TwoFishKeyVectorPair(0x89, 0x10),
        "pkt": TwoFishKeyVectorPair(0x89, 0x10),
        "log1": TwoFishKeyVectorPair(0xAB, 0xBE),
        "log2": TwoFishKeyVectorPair(0xBA, 0xBE),
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
    fish = TwoFishCBC(TwoFishKeyVectorPair(0x69, 0x42))
    s = """
My first thought was, he lied in every word,
That hoary cripple, with malicious eye
Askance to watch the working of his lie
On mine, and mouth scarce able to afford
Suppression of the glee, that purs'd and scor'd
Its edge, at one more victim gain'd thereby
    """
    b = bytearray(s.encode("ascii"))
    fish.encrypt(b)
    print(b.hex())
    fish.decrypt(b)
    print(b.decode("ascii"))

    s = b"CBC Mode Test\x03\x03\x03"
    s = TwoFishCBC._xor(s, bytes.fromhex("05C9428085EE3F34D7ECE73C5628F605"))
    print(s)
    fish = twofish.Twofish(bytes.fromhex("6B990E620635B4C36A1B737487CEAD8D"))
    enc = fish.encrypt(s)
    print(enc)  # should be 0xBCD4...