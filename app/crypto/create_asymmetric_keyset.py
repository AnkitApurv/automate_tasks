from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from app import app_config, logging_config

def main():
    """
    _summary_
    """
    logging_config.log.info('Generate Asymmetric Key-pair: Begin')
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

    pem_public = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    logging_config.log.info('Generate Asymmetric Key-pair: Done')
    logging_config.log.info('Save Asymmetric Key-pair to disk: Begin')
    with open(f"{app_config.config_paths['config_base_path']}/{app_config.config_paths['asymmetric_keyset']['private_key']}", 'wb') as f:
        f.write(pem_private)

    with open(f"{app_config.config_paths['config_base_path']}/{app_config.config_paths['asymmetric_keyset']['public_key']}", 'wb') as f:
        f.write(pem_public)
    logging_config.log.info('Save Asymmetric Key-pair to disk: Done')
    return

if __name__ == '__main__':
    main()