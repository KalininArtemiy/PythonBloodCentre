import logging
from pathlib import Path

LOG_PATH = Path(__file__).resolve().parent.parent / "bot.log"

def setup_logger()->logging.Logger:
    logger = logging.getLogger("donor_bot")
    if logger.handlers:
        return logger
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s.%(msecs)03d [%(levelname)s] %(name)s: %(message)s",
        "%Y-%m-%d %H:%M:%S",)
    handler = logging.FileHandler(LOG_PATH, mode="a", encoding="utf-8")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger