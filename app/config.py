import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    LOGIN_URL: str = "https://donor-mos-sab.online/account/"
    USER_EMAIL: str = os.getenv("DONOR_EMAIL", "")
    USER_PASSWORD: str = os.getenv("USER_PASSWORD", "")
    HEADLESS: bool = os.getenv("HEADLESS", "True").lower() == "true"
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")

settings = Settings()