import asyncio
import logging
import time
from playwright.async_api import async_playwright
from app.config import settings
from app.logger import setup_logger
from app.services.auth_service import AuthService
from app.services.booking_service import booking_loop
from app.services.time_service import sleep_until_msk, now_msk

logger = logging.getLogger("donor_bot")


async def main() -> None:
    setup_logger()
    t_total_start = time.perf_counter()
    logger.info("main: start at %s (MSK)", now_msk().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])
    logger.info("main: config login_at=%s refresh_at=%s timeout_min=%d",
                settings.LOGIN_AT, settings.REFRESH_AT, settings.TIMEOUT_MIN)

    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=settings.HEADLESS)
        page = await browser.new_page()
        try:
            logger.info("main: waiting until %s MSK for login", settings.LOGIN_AT)
            sleep_until_msk(settings.LOGIN_AT)

            auth = AuthService(page)
            await auth.login_service()

            t_session_start = time.perf_counter()
            logger.info("main: logged in at %s, session timer started",
                        now_msk().strftime("%H:%M:%S.%f")[:-3])

            logger.info("main: waiting until %s MSK for refresh start", settings.REFRESH_AT)
            sleep_until_msk(settings.REFRESH_AT, roll_to_next_day=False)

            logger.info("main: starting booking_loop at %s",
                        now_msk().strftime("%H:%M:%S.%f")[:-3])
            result = await booking_loop(page)
            logger.info("main: booking_loop finished result=%s", result)
        finally:
            session_lifetime = time.perf_counter() - t_session_start if 't_session_start' in locals() else 0
            total_lifetime = time.perf_counter() - t_total_start
            logger.info("main: session_lifetime=%.2fs, total_lifetime=%.2fs",
                        session_lifetime, total_lifetime)
            await browser.close()
            logger.info("main: done")


if __name__ == "__main__":
    asyncio.run(main())