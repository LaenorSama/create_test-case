import requests
import os
# библиотека для загрузки данных из env
from dotenv import load_dotenv

# функция для получения bearer-токена нужного инстанса для токена администратора
def get_bearer_token(testops_api_url, testops_token):
    # URL для получения токена
    url = f"{testops_api_url}uaa/oauth/token"

    # Данные для запроса (в формате x-www-form-urlencoded)
    data = {
        "grant_type": "apitoken",
        "scope": "openid",
        "token": testops_token
    }

    # Заголовки
    headers = {
        "Accept": "application/json"
    }

    # Отправляем POST-запрос
    response = requests.post(url, data=data, headers=headers)

    # Проверяем успешность запроса
    if response.status_code == 200:
        try:
            token = response.json().get("access_token")
            if token:
                print("Bearer-токен получен")
                return token
            else:
                print("Ответ не содержит access_token:", response.json())
        except requests.exceptions.JSONDecodeError:
            print("Ошибка парсинга JSON:", response.text)
    else:
        print("Ошибка получения токена:", response.status_code, response.text)

# функция формирует сценарий из списка шагов
# возвращает json
def create_testcase_scenario(steps):
    scenario = {
        "steps": [{"name": step} for step in steps]
                }
    return scenario

# функция создает новый тест-кейс,
# возвращает ID тест-кейса
def post_create_testcase(instance_name, project_id, testcase_name, scenario):
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "Content-Type": "application/json"  # Для корректной обработки JSON
    }
    # Формируем тело запроса
    payload = {
        "projectId": project_id,
        "name": testcase_name,
        "archived": False,
        "scenario": scenario
    }
    response = requests.post(f"https://{instance_name}/api/testcase", headers=headers, json=payload)
    data = response.json()
    testcase_id = data["id"]
    print(f'Создан тест-кейс. ID = {testcase_id}')
    return testcase_id

# объявляем нужные переменные
PROJECT_ID = 282
INSTANCE_NAME = "demo.qatools.cloud"

# Загружаем .env файл
load_dotenv()
# Получаем токен из .env файла
TESTOPS_TOKEN = os.getenv("TESTOPS_TOKEN")
BEARER_TOKEN = get_bearer_token(f"https://{INSTANCE_NAME}/api/", TESTOPS_TOKEN)

TESTCASE_NAME = "API Открыть меню пользователя"
STEPS = ["Зайти на портал", "Нажать на аватар пользователя", "Открылось меню пользователя"]

# получаем сценарий тест-кейса
TESTCASE_SCENARIO = create_testcase_scenario(STEPS)
# создаем тест-кейс
TESTCASE_ID = post_create_testcase(INSTANCE_NAME, PROJECT_ID, TESTCASE_NAME, TESTCASE_SCENARIO)
