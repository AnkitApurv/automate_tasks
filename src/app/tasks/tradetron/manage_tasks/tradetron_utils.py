from typing import TypedDict

class Credentials(TypedDict):
    username: str
    password: str
    otp: str

class WebSiteConfig(TypedDict):
    url: str
    username_id: str
    password_id: str
    otp_id: str
    submit_button_id: str

class TradetronTaskConfigFiles(TypedDict):
    credentials: str

class TradetronTaskConfig(TypedDict):
    name: str
    profile_path: str
    files: TradetronTaskConfigFiles