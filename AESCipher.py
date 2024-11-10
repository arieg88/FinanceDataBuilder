import base64
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes

SALT_LEN = 16  # Length of the salt used for key derivation

class AESCipher(object):
    """
    A class for AES encryption and decryption using CBC mode with salted password-based key derivation.
    """

    def __init__(self, password, salt=None):
        """
        Initializes the AESCipher object with the provided password and an optional salt.

        Args:
            password (str): The password used to derive the encryption key.
            salt (bytes, optional): A salt for key derivation. If not provided, a random salt will be generated.
        """
        self.bs = AES.block_size  # Block size for AES encryption (typically 16 bytes)

        # If no salt is provided, generate a random salt
        if salt is None:
            self.salt = get_random_bytes(SALT_LEN)
        else:
            self.salt = salt
        
        # Derive the key using the scrypt KDF (Password-Based Key Derivation Function)
        self.key = scrypt(password.encode(), self.salt, 16, N=2**14, r=self.bs, p=1)

    def encrypt(self, raw):
        """
        Encrypts the provided data using AES in CBC mode.

        Args:
            raw (bytes): The plaintext data to be encrypted.

        Returns:
            bytes: The base64-encoded encrypted data with the IV and salt prepended.
        """
        raw = self._pad(raw)  # Pad the data to ensure it's a multiple of the block size
        iv = Random.new().read(AES.block_size)  # Generate a random initialization vector (IV)
        
        # Create an AES cipher object in CBC mode with the derived key and IV
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        
        # Encrypt the data and return the IV + encrypted data encoded in base64
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        """
        Decrypts the provided encrypted data using AES in CBC mode.

        Args:
            enc (bytes): The base64-encoded encrypted data (with the IV and salt prepended).

        Returns:
            bytes: The decrypted plaintext data.
        """
        enc = base64.b64decode(enc)  # Decode the base64-encoded encrypted data
        iv = enc[:AES.block_size]  # Extract the initialization vector (IV) from the start of the data
        
        # Create an AES cipher object in CBC mode with the derived key and IV
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        
        # Decrypt the data and return the unpadded plaintext
        return AESCipher._unpad(cipher.decrypt(enc[AES.block_size:]))

    def _pad(self, s):
        """
        Pads the input data to ensure it's a multiple of the AES block size.

        Args:
            s (bytes): The data to be padded.

        Returns:
            bytes: The padded data.
        """
        # Calculate the padding size and append it to the original data
        pad = ((self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)).encode()
        return s + pad

    @staticmethod
    def _unpad(s):
        """
        Removes padding from the decrypted data.

        Args:
            s (bytes): The padded decrypted data.

        Returns:
            bytes: The unpadded data.
        """
        return s[:-ord(s[len(s)-1:])]  # Remove the padding based on the last byte
