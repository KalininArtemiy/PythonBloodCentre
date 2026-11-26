import logging
import random
import time
from datetime import datetime, time as dtime, timedelta
from zoneinfo import ZoneInfo
from app.config import settings

logger = logging.getLogger("donor_bot")
TZ = ZoneInfo(settings.TZ_NAME)


def now_msk() -> datetime:
    return datetime.now(TZ)


def parse_hhmmss(value: str) -> dtime:
    return datetime.strptime(value, "%H:%M:%S").time()


def sleep_until_msk(hh_mm_ss: str, roll_to_next_day: bool = True) -> None:
    target_time = parse_hhmmss(hh_mm_ss)
    now = now_msk()
    target_dt = now.replace(
        hour=target_time.hour,
        minute=target_time.minute,
        second=target_time.second,
        microsecond=0,
    )
    if target_dt <= now:
        if roll_to_next_day:
            target_dt += timedelta(days=1)
        else:
            logger.debug("sleep_until_msk: target %s already passed, not sleeping", hh_mm_ss)
            return

    delta = (target_dt - now_msk()).total_seconds()
    logger.debug(
        "sleep_until_msk: now=%s, target=%s, sleep=%.2fs",
        now_msk().strftime("%H:%M:%S.%f")[:-3],
        target_dt.strftime("%H:%M:%S"),
        delta,
    )
    if delta > 0:
        time.sleep(delta)
    logger.debug("sleep_until_msk: woke up at %s", now_msk().strftime("%H:%M:%S.%f")[:-3])


def jitter_sleep() -> None:
    delay = random.uniform(settings.REFRESH_SLEEP_MIN, settings.REFRESH_SLEEP_MAX)
    time.sleep(delay)


def deadline_after(minutes: int) -> datetime:
    return now_msk() + timedelta(minutes=minutes)