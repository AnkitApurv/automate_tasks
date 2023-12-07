import logging

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey

from app import app_config, logging_utils

logger: logging.Logger = logging.Logger(app_config.services['manage_task_secrets']['name'])
logging_extra_info: logging_utils.LoggingExtraInfo = {'service': app_config.services['manage_task_secrets']['name'], 'task': 'generic'}

def main() -> None:
    """
    _summary_
    """
    logger.info('Generate Asymmetric Key-pair: Begin', extra = logging_extra_info)
    private_key: RSAPrivateKey = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
        backend=default_backend()
    )
    public_key: RSAPublicKey = private_key.public_key()

    pem_private: bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    pem_public: bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    logger.info('Generate Asymmetric Key-pair: Done', extra = logging_extra_info)
    logger.info('Save Asymmetric Key-pair to disk: Begin', extra = logging_extra_info)
    with open(f"{app_config.paths['config_base_path']}/{app_config.paths['asymmetric_keyset']['private_key']}", 'wb') as f:
        f.write(pem_private)

    with open(f"{app_config.paths['config_base_path']}/{app_config.paths['asymmetric_keyset']['public_key']}", 'wb') as f:
        f.write(pem_public)
    logger.info('Save Asymmetric Key-pair to disk: Done', extra = logging_extra_info)
    return
    return
