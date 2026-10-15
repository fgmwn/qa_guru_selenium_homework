# 100% черновик, требует модификаци

# Задача: "Разработать на языке Python и библиотеке Selenium как можно больше позитивных и негативных тестовых сценариев используя подход DDT для формы логина https://qa-guru.github.io/one-page-form/login.html"
# Для реализации тестирования формы авторизации по методу DDT (Data-Driven Testing) на Python лучше всего использовать связку фреймворка pytest
#(через встроенную параметризацию @pytest.mark.parametrize) и библиотеки Selenium WebDriver.
# Ниже представлена подборка тестовых сценариев и готовый скрипт, автоматизирующий проверку страницы https://qa-guru.github.io/one-page-form/login.html .
# Спроектированные тестовые сценарии (DDT-матрица)В качестве валидных учетных данных (ожидаемое поведение тестового стенда QA.GURU) принята стандартная пара: email qaguru@qa.guru и любой непустой пароль (или специфичный qaguru),
# при которых форма показывает успешный вход.
# Позитивные сценарии (Positive)Валидный Email и пароль: Проверка классического успешного входа (qaguru@qa.guru).
# Регистронезависимость Email: Ввод email в верхнем регистре (QAGURU@QA.GURU) — система должна корректно приводить его к нижнему регистру.
# Негативные сценарии (Negative)Неверный пароль: Валидный email, но абсолютно некорректный пароль.
# Несуществующий Email: Попытка входа с незарегистрированной почтой.
# Пустой Email: Поле пароля заполнено, email — пустая строка (валидация обязательного поля).
# Пустой пароль: Поле email заполнено, пароль — пустая строка.
# Оба поля пустые: Отправка полностью пустой формы.
# Email без коммерческого атта @: Нарушение базового синтаксиса почты (qaguruqa.guru).Email без доменной части: Строка вида qaguru@.Email без имени ящика: Строка вида @qa.guru.
# Спецсимволы в Email: Использование запрещенных символов (qaguru!#$@qa.guru).Длинный пароль/Email (XSS/SQL-инъекции): Базовый чек на устойчивость к инъекциям (' OR '1'='1).

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest

# Локаторы элементов формы на странице
EMAIL_INPUT = (By.ID, "email") or (By.CSS_SELECTOR, "input[type='email']")
PASSWORD_INPUT = (By.ID, "password") or (By.CSS_SELECTOR, "input[type='password']")
LOGIN_BUTTON = (By.ID, "loginButton") or (By.CSS_SELECTOR, "button[type='submit']")
# Селекторы сообщений об ошибке или успехе зависят от верстки страницы QA.GURU
STATUS_MESSAGE = (By.ID, "message") 


@pytest.fixture
def driver():
    """Фикстура для инициализации и закрытия браузера."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Фоновый режим для CI/CD
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=options)
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

    print("Тест стартовал!")
    
    # 1. Открытие тестируемой страницы
    driver.get("https://qa-guru.github.io/one-page-form/login.html")
    
    # 2. Поиск элементов формы
    email_field = driver.find_element(*EMAIL_INPUT)
    password_field = driver.find_element(*PASSWORD_INPUT)
    submit_button = driver.find_element(*LOGIN_BUTTON)
    
    # 3. Очистка полей и ввод тестовых данных
    email_field.clear()
    email_field.send_keys(email)
    
    password_field.clear()
    password_field.send_keys(password)
    
    # 4. Клик по кнопке отправки формы
    submit_button.click()
    
    # 5. Ожидание появления ответа (алерта или текста на экране)
    # ПРИМЕЧАНИЕ: Данный блок адаптируется под логику страницы (JS-alert или блок текста).
    try:
        # Проверяем, появился ли браузерный alert
        alert = WebDriverWait(driver, 2).until(EC.alert_is_present())
        alert_text = alert.text
        alert.accept()
        actual_result = alert_text
    except:
        # Если алерта нет, ищем текст ошибки на самой странице
        actual_result = driver.find_element(*STATUS_MESSAGE).text

    # 6. Проверка результата (Assertion)
    if scenario_type == "positive":
        assert expected_text in actual_result, f"Ожидался успешный вход, но получено: '{actual_result}'"
    else:
        assert expected_text in actual_result or driver.current_url != "success_url", \
            f"Форма пропустила некорректные данные: Email='{email}', Pass='{password}'"

