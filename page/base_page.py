from playwright.sync_api import Page
from config.utils.logger import get_logger
from config.actions import ActionPage
from config.asserts import AssertPage


# Константы страницы:
BASE_URL = "https://www.saucedemo.com/"


class BasePage:

    def __init__(self, page: Page):
        """Инициализация страницы браузера и зависимости."""
        self.page = page
        self.logger = get_logger(self.__class__.__name__)
        self.actions = ActionPage(page)
        self.asserts = AssertPage(page)