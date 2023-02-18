import argparse
from app.crypto import make_encrypted_config, read_encrypted_config

def update_config(config: dict) -> dict:
    """
    _summary_

    :return: _description_
    :rtype: _type_
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("password")
    config_new = parser.parse_args().__dict__
    config_updated = config | config_new # new in Python 3.9, see https://peps.python.org/pep-0584/
    return config_updated

def main():
    """
    _summary_
    """
    encrypted_old = read_encrypted_config.read_config()
    config_old = read_encrypted_config.decrypt_config(encrypted_old)
    config_updated = update_config(config_old)
    encrypted_new = make_encrypted_config.encrypt_config(config_updated)
    make_encrypted_config.save_config(encrypted_new)
    return

if __name__ == '__main__':
    main()