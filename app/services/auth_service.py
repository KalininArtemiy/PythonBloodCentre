import logging
import time
from app.config import settings

logger = logging.getLogger("donor_bot")


class AuthService:
    def __init__(self, page):
        self.page = page
        self.login = settings.USER_EMAIL
        self.password = settings.USER_PASSWORD
        self.url = settings.LOGIN_URL
        self.headless = settings.HEADLESS

    async def login_service(self) -> str:
        t_total = time.perf_counter()
        logger.info("login: start url=%s", self.url)

        t = time.perf_counter()
        await self.page.goto(self.url, wait_until="commit")
        logger.debug("login: goto took=%.2fs", time.perf_counter() - t)

        await self.page.wait_for_selector("#user_login", state="attached")
        await self.page.fill("#user_login", self.login)
        await self.page.fill("#user_password", self.password)

        t = time.perf_counter()
        await self.page.click("#wp-submit")
        logger.debug("login: click submit took=%.2fs", time.perf_counter() - t)

        t = time.perf_counter()
        await self.page.wait_for_selector(
            settings.TABLE_WRAP_SELECTOR,
            state="visible",
            timeout=settings.LOGIN_TABLE_TIMEOUT_MS,
        )
        logger.debug("login: wait table took=%.2fs", time.perf_counter() - t)

        logger.info("login: ok, total took=%.2fs", time.perf_counter() - t_total)
        return await self.page.content()