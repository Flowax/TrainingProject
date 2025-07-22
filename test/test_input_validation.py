import random
import time
from asyncio import timeout

import allure
import pytest
from playwright.sync_api import sync_playwright, expect
import  requests
from config.utils.reporter import ReportPage

from page.base_page import BASE_URL

@allure.epic("Тренировка автотестов")
class TestPetstore:
    BASE_URL = "https://petstore.swagger.io"
    @allure.title("Тест PETSTORE")
    @pytest.fixture(scope="session")
    def api_context(self):
        with sync_playwright() as playwright:
            # Создаем контекст API
            api_context = playwright.request.new_context(
                base_url=self.BASE_URL,
                extra_http_headers={"Content-Type": "application/json"}
            )
            yield api_context  

            # Закрытие после всех тестов
            api_context.dispose()

    def test_create_user(self, api_context):
        # создаем юзера
        user_data = {
            "id": 95666,
            "username": "goga",
            "firstName": "George",
            "lastName": "Flowax",
            "email": "test@test.ru",
            "password": "test123",
            "phone": "89104894412",
            "userStatus": 0
        }
        create_response = api_context.post("/v2/user", data = user_data)
        expect(create_response).to_be_ok()

        response_data = create_response.json()
        print(response_data)

        #Получаем созданного юзера
        get_response = api_context.get(f"/v2/user/{user_data["username"]}")
        expect(get_response).to_be_ok()

        response_data = get_response.json()
        print(response_data)

    def test_auth_user(self, api_context):
         # Шаг авторизации
        auth_data = {
            "username": "goga1",
            "password": "test123"
        }
        auth_response = api_context.get("/v2/user/login", params=auth_data)
        print(auth_response.json())
        # Проверка успешности
        expect(auth_response).to_be_ok()  # status 200


    @pytest.fixture
    def pet_data(self):
        gen_id = random.randint(600, 700)
        return {
                "id": gen_id,
                "category": {
                    "id": gen_id,
                    "name": "pet"
                },
                "name": "Fiona",
                "photoUrls": [
                    "string"
                ],
                "tags": [
                    {
                        "id": gen_id,
                        "name": "cat"
                    }
                ],
                "status": "available"
        }

    @pytest.fixture
    def created_pet(self, api_context, pet_data):
        """Фикстура создает питомца и возвращает его ID"""
        response = api_context.post("/v2/pet", data=pet_data)
        expect(response).to_be_ok()
        yield pet_data["id"]
        # Очистка после теста
        api_context.delete(f"/pet/{pet_data['id']}")

    @allure.title("Тест с использованием session_id")
    def test_find_pet(self, api_context, pet_data):
        """Тест, создает питомца"""
        add_response = api_context.post("/v2/pet", data=pet_data)
        print(add_response.json())
        # Проверки
        expect(add_response).to_be_ok()
        assert add_response.json()["name"] == "Fiona"
        pet_id = add_response.json()["id"]
        print(pet_id)
        time.sleep(20)
        #Ищем созданного петомца
        find_pet = api_context.get(f"/v2/pet/{pet_id}")
        print(find_pet.json())
    #
    # def test_find_pet(self, api_context, created_pet):
    #     pet_id = created_pet
    #     print(pet_id)
    #     time.sleep(20)
    #     with expect(api_context.get(f"/v2/pet/{pet_id}")).to_be_ok() as response_info:
    #         response = response_info.value
    #         assert response.json()["name"] == "Fiona"
    #         print(response.json())
