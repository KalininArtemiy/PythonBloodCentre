import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    LOGIN_URL: str = os.getenv("LOGIN_URL", "")
    USER_EMAIL: str = os.getenv("USER_EMAIL", "")
    USER_PASSWORD: str = os.getenv("USER_PASSWORD", "")
    HEADLESS: bool = os.getenv("HEADLESS", "True").lower() == "true"
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")

    TZ_NAME: str = os.getenv("TZ_NAME", "Europe/Moscow")
    LOGIN_AT: str = os.getenv("LOGIN_AT", "11:58:55")
    REFRESH_AT: str = os.getenv("REFRESH_AT", "11:59:00")
    TIMEOUT_MIN: int = int(os.getenv("TIMEOUT_MIN", "10"))
    REFRESH_SLEEP_MIN: float = float(os.getenv("REFRESH_SLEEP_MIN", "0.1"))
    REFRESH_SLEEP_MAX: float = float(os.getenv("REFRESH_SLEEP_MAX", "0.3"))
    RESERVATION_SELECTOR: str = os.getenv("RESERVATION_SELECTOR", 'button[data-src="#modal-reservation"]')
    ROWS_SELECTOR: str = os.getenv("ROWS_SELECTOR", "tr.dates-table__item")
    TABLE_WRAP_SELECTOR: str = os.getenv("TABLE_WRAP_SELECTOR", "div.needs-tableWrap")
    TABLE_WAIT_TIMEOUT_MS: int = int(os.getenv("TABLE_WAIT_TIMEOUT_MS", "15000"))
    DATE_SELECTOR: str = os.getenv("DATE_SELECTOR", "td.table-item__date")
    LOGIN_TABLE_TIMEOUT_MS: int = int(os.getenv("LOGIN_TABLE_TIMEOUT_MS", "20000"))
settings = Settings()