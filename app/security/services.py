import base64

from bcrypt import checkpw, gensalt, hashpw
from cryptography.fernet import Fernet

class SecurityServices:
    def __init__(self, hash_key) -> None:
        self.hasher = Fernet(hash_key)

    def encrypt(self, value):
        return self.hasher.encrypt(value.encode())

    def decrypt(self, value):
        try:
            return self.hasher.decrypt(value).decode("utf-8")
        except Exception:
            return None

    async def hash(self, value):
        return hashpw(value.encode("utf8"), gensalt())

    async def validate_hash(self, value, hashed_value):
        if not checkpw(value.encode("utf-8"), hashed_value):
            return False
        return True

    def encode_text(self, text: str) -> str:
        # Encode the text into bytes, then convert to Base64
        encoded_bytes = base64.b64encode(text.encode("utf-8"))
        # Convert the Base64 bytes to a string
        password = encoded_bytes.decode("utf-8")
        return password

    def decode_text(self, text: str) -> str:
        # Decode the Base64 string back to bytes
        decoded_bytes = base64.b64decode(text.encode("utf-8"))
        # Convert the bytes back to the original text
        original_text = decoded_bytes.decode("utf-8")
        return original_text
