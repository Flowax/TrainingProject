from playwright.sync_api import sync_playwright, expect
import allure
import pytest

from page.base_page import BASE_URL

@allure.epic("Тренировка автотестов")
class TestSmoke:

    @allure.title("Тест SAUCEDEMO")
    def test_saucedemo(self):
        playwright = sync_playwright().start()
        browser = playwright.firefox.launch(headless=False)
        page = browser.new_page()

        try:
            # Открываем страницу, проверяем тайтл
            page.goto(BASE_URL, timeout=10000)
            expect(page).to_have_title("Swag Labs")

            # Авторизация
            page.fill("#user-name", "standard_user")
            page.fill("#password", "secret_sauce")
            page.click("#login-button")

            # Проверка авторизации
            assert page.locator("#header_container > div.header_secondary_container > span").is_visible()
            assert page.title() == "Swag Labs"
            # Добавление товара в корзину
            page.click("#item_4_title_link > div")
            page.click("#add-to-cart")

            # Проверка добавления товара в корзину
            assert page.locator("#remove").is_visible()

        finally:
            # Закрытие
            browser.close()
            playwright.stop()