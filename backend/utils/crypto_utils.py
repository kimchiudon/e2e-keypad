from pathlib import Path
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

BASE_DIR = Path(__file__).resolve().parent.parent
PRIVATE_KEY_PATH = BASE_DIR / "private_key.pem"

def decrypt_rsa_base64(encrypted_data: str) -> str:
    with open(PRIVATE_KEY_PATH, "rb") as f:
        private_key = RSA.import_key(f.read())

    cipher_rsa = PKCS1_OAEP.new(private_key)
    decrypted_bytes = cipher_rsa.decrypt(base64.b64decode(encrypted_data))

    return decrypted_bytes.decode("utf-8")