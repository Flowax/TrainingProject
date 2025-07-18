import allure

from config.utils.reporter import ReportPage

from page.base_page import BASE_URL

@allure.epic("Тренировка автотестов")
class TestSaucedemo:

    @allure.title("Тест SAUCEDEMO")
    def test_saucedemo(self, page):
        report_page = ReportPage(page)
        # Открываем страницу, проверяем тайтл
        page.goto(BASE_URL, timeout=10000)
        with allure.step("Проверка открытия страницы"):
            try:
                assert page.title() == "Swag Labs"
            except AssertionError:
                report_page.attach_screenshot()
                raise

        # Авторизация
        page.fill("#user-name", "standard_user")
        page.fill("#password", "secret_sauce")
        page.click("#login-button")

        # Проверка авторизации
        with allure.step("Проверка авторизации"):
            try:
                assert page.locator("#header_container > div.header_secondary_container > span").is_visible()
                assert page.title() == "Swag Lab"
            except AssertionError:
                report_page.attach_screenshot()
                raise

        # Добавление товара в корзину
        page.click("#item_4_title_link > div")
        page.click("#add-to-cart")

        # Проверка добавления товара в корзину
        with allure.step("Проверка добавления товара в корзину"):
            try:
                assert page.locator("#remove").is_visible()
                report_page.attach_screenshot()
            except AssertionError:
                report_page.attach_screenshot()
                raise
