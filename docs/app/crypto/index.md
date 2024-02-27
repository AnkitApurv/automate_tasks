# Scheduled Login : Tradetron

## app/crypto

Helper module to facilitate encrypting sensetive config files.

### Python modules with command line usability:

#### change_assymmetric_keyset.py

Useful for generating new RSA keyset which will be used in encryption, decryption.

#### make_encrypted_config.py

Writes a new config file to disk which will be encrypted.

#### read_encrypted_config.py

Reads encrypted config file.

#### change_password_in_config.py

Modifies the key-value pair for key "password" in the encrypted config file.

### Helper Python modules:

#### crypto_interface.py

Easy encryption and decryption functionality.
