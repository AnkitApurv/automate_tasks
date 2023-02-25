from app.crypto import read_encrypted_config

def verify_login(username: str, password: str) -> bool:
    login_success: bool = True
    credentials = read_encrypted_config.main()
    login_success =  credentials['username'] == username and credentials['password'] == password
    return login_success