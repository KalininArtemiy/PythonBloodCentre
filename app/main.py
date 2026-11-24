import asyncio
from playwright.async_api import async_playwright
from app.services.auth_service import AuthService
from app.config import settings


async def main():
    
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=settings.HEADLESS)
        page = await browser.new_page()
        auth = AuthService(page)
        print("EMAIL:", auth.login)
        print("PASSWORD len:", auth.password)
        html = await auth.login_service()
        with open("account_page.html", "w", encoding="utf-8") as f:
            f.write(html)
        await browser.close()


asyncio.run(main())