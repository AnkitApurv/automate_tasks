from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey

from app import app_config


def encrypt(message: bytes) -> bytes:
    with open(f"{app_config.paths['asymmetric_keyset']['public_key']}", "rb") as key_file:
        public_key: RSAPublicKey = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    encrypted: bytes = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted

def decrypt(encrypted: bytes) -> bytes:
    with open(f"{app_config.paths['asymmetric_keyset']['private_key']}", "rb") as key_file:
        private_key: RSAPrivateKey = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    message: bytes = private_key.decrypt(
        encrypted,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return message