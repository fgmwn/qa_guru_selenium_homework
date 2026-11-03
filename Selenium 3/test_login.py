import time

import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Локаторы элементов формы на странице
LOGIN_INPUT     = (By.ID, "login-input")
PASSWORD_INPUT  = (By.ID, "password-input")
SUBMIT_BUTTON   = (By.ID, "submit-button")
STATUS_MESSAGE  = (By.ID, "error-message")


@pytest.fixture
def driver():
    """Фикстура для инициализации и закрытия браузера."""
    #options = webdriver.ChromeOptions()
    #options.add_argument("--headless")  # Фоновый режим для CI/CD
    #options.add_argument("--window-size=1920,1080")    
    #driver = webdriver.Chrome(options=options)

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(5)

    yield driver

    driver.quit()


# Реализация DDT подхода через параметризацию pytest
@pytest.mark.parametrize(
    "email, password, scenario_type, expected_text",
    [
        # --- ПОЗИТИВНЫЕ СЦЕНАРИИ ---
        ("qaguru@qa.guru", "qaguru", "positive", "Вы успешно вошли"),
        ("QAGURU@QA.GURU", "qaguru", "positive", "Вы успешно вошли"), 
        
        # --- НЕГАТИВНЫЕ СЦЕНАРИИ ---
        ("qaguru@qa.guru", "wrong_pass", "negative", "Неверный пароль"),
        ("unknown@qa.guru", "qaguru", "negative", "Такого пользователя не существует"),
        ("", "qaguru", "negative", "Заполните поле Email"),
        ("qaguru@qa.guru", "", "negative", "Заполните поле Пароль"),
        ("", "", "negative", "Заполните поля"),
        ("qaguruqa.guru", "qaguru", "negative", "Email должен содержать символ @"),
        ("qaguru@", "qaguru", "negative", "Введен некорректный Email"),
        ("@qa.guru", "qaguru", "negative", "Введен некорректный Email"),
        ("qaguru' OR '1'='1", "' OR '1'='1", "negative", "Некорректные данные"),
    ]
)
def test_login_form(driver, email, password, scenario_type, expected_text):
    """Тест кейс, принимающий наборы данных (DDT)."""
    
    # 1. Открытие тестируемой страницы
    driver.get("https://qa-guru.github.io/one-page-form/login.html")
    
    # 2. Поиск элементов формы
    email_field = driver.find_element(*LOGIN_INPUT)    
    password_field = driver.find_element(*PASSWORD_INPUT)    
    submit_button = driver.find_element(*SUBMIT_BUTTON)
    
    # 3. Очистка полей и ввод тестовых данных
    email_field.clear()
    email_field.send_keys(email)
    
    password_field.clear()
    password_field.send_keys(password)
    
    # 4. Клик по кнопке отправки формы
    submit_button.click()
    
    # 5. Ожидание появления ответа
    actual_result = driver.find_element(*STATUS_MESSAGE).text

    time.sleep(5)

    # NOTE: как минимум по трем причинам это анти подход 
    # 5. Ожидание появления ответа (алерта или текста на экране)
    # ПРИМЕЧАНИЕ: Данный блок адаптируется под логику страницы (JS-alert или блок текста).
    try:
        # Проверяем, появился ли браузерный alert
        alert = WebDriverWait(driver, 2).until(EC.alert_is_present())
        alert_text = alert.text
        print(f"Allert is present with test: {alert_text}")
        alert.accept()
        actual_result = alert_text
    except:
        # Если алерта нет, ищем текст ошибки на самой странице
        actual_result = driver.find_element(*STATUS_MESSAGE).text
        print(f"Allert-а нет, поэтому мы ищем тест с ошибкой комментарием на странице, текст: {actual_result}")

    # 6. Проверка результата (Assertion)
    if scenario_type == "positive":
        assert expected_text in actual_result, f"Ожидался успешный вход, но получено: '{actual_result}'" #"Wrong login or password"
    else:
        assert expected_text in actual_result or driver.current_url != "success_url",  f"Форма пропустила некорректные данные: Email='{email}', Pass='{password}'"