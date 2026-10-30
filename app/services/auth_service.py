from config import settings

class AuthService:
    def __init__(self, page):
        self.page = page
        self.login = settings.USER_EMAIL
        self.password= settings.USER_PASSWORD
        self.url =  settings.LOGIN_URL
        self.headless= settings.HEADLESS