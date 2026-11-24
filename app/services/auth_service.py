from app.config import settings

class AuthService:
    def __init__(self, page):
        self.page = page
        self.login = settings.USER_EMAIL
        self.password= settings.USER_PASSWORD
        self.url =  settings.LOGIN_URL
        self.headless= settings.HEADLESS

    async def login_service(self)->str:
        await self.page.goto(self.url, wait_until="domcontentloaded")
        
        await self.page.wait_for_selector("#user_login", state="visible")
        
        await self.page.fill("#user_login", self.login)
        
        await self.page.fill("#user_password", self.password)

        await self.page.click("#wp-submit")
        
        await self.page.wait_for_selector("a.logout", timeout=20000)
        
        await self.page.wait_for_load_state("domcontentloaded")
        
        return await self.page.content()