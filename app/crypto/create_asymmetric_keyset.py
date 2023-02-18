from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from app import app_config

def main():
    """
    _summary_
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    pem_private = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open(f"{app_config.config_paths['config_base_path']}/{app_config.config_paths['asymmetric_keyset']['private_key']}", 'wb') as f:
        f.write(pem_private)

    pem_public = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(f"{app_config.config_paths['config_base_path']}/{app_config.config_paths['asymmetric_keyset']['public_key']}", 'wb') as f:
        f.write(pem_public)
    return

if __name__ == '__main__':
    main()