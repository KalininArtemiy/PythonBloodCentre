from app.config import settings
import time

class AuthService:
    def __init__(self, page):
        self.page = page
        self.login = settings.USER_EMAIL
        self.password= settings.USER_PASSWORD
        self.url =  settings.LOGIN_URL
        self.headless= settings.HEADLESS

    async def login_service(self) -> str:
        t = time.perf_counter()
        await self.page.goto(self.url, wait_until="commit")
        print(f"  goto: {time.perf_counter() - t:.2f}s")

        await self.page.wait_for_selector("#user_login", state="attached")
        await self.page.fill("#user_login", self.login)
        await self.page.fill("#user_password", self.password)

        t = time.perf_counter()
        await self.page.click("#wp-submit")
        print(f"  click submit: {time.perf_counter() - t:.2f}s")

        # Ждём появления нужной таблицы (самый надёжный и быстрый способ)
        t = time.perf_counter()
        await self.page.wait_for_selector("div.needs-tableWrap", state="visible", timeout=20000)
        print(f"  wait needs-tableWrap: {time.perf_counter() - t:.2f}s")

        return await self.page.content()