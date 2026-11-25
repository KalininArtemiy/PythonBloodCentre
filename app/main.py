import asyncio
from playwright.async_api import async_playwright
from app.services.auth_service import AuthService
from app.config import settings
import time


async def main():
    
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=settings.HEADLESS)
        page = await browser.new_page()

        auth = AuthService(page)
        html = await auth.login_service()

        # --- Reload'ы ---
        for i in range(1, 5):
            t = time.perf_counter()
            await page.reload(wait_until="commit")
            await page.wait_for_selector("div.needs-tableWrap", state="visible", timeout=15000)
            print(f"reload {i}: {time.perf_counter() - t:.2f}s")


asyncio.run(main())