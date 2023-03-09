from app.tasks.tradetron.manage_tasks.tradetron_utils import Credentials


def verify_login(received_credentials: Credentials, stored_credentials: Credentials) -> bool:
    return received_credentials == stored_credentials