import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://qa-guru.github.io/one-page-form/text-box.html"

# Локаторы
FULL_NAME_FIELD = (By.ID, "userName")
EMAIL_FIELD = (By.ID, "userEmail")
CURRENT_ADDRESS_FIELD = (By.ID, "currentAddress")
PERMANENT_ADDRESS_FIELD = (By.ID, "permanentAddress")
SUBMIT_BUTTON = (By.ID, "submit")
OUTPUT_BOX = (By.ID, "output")

# Тестовые данные
FULL_NAME = "Петя Иванов"
EMAIL = "petya@yandex.com"
CURRENT_ADDRESS = "ул. Пушкина, д. Калатушкино"
PERMANENT_ADDRESS = "ул. Пушкина, д. Калатушкино"

# Пауза между шагами
PAUSE = 5


def submit_form(driver):
    # Фиксированный подвал страницы может перекрыть кнопку в небольшом окне.
    button = driver.find_element(*SUBMIT_BUTTON)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
    button.click()


def fill_and_submit(driver, field, value):
    # Заполняет поле, жмёт submit, проверяет, что значение попало в output.
    driver.find_element(*field).send_keys(value)
    time.sleep(PAUSE)

    submit_form(driver)
    time.sleep(PAUSE)

    result_box = driver.find_element(*OUTPUT_BOX)
    assert value in result_box.text, f"Не найдено '{value}' в выводе: {result_box.text}"
    print(f"OK: {value}")



def check_invalid_email(driver):
    # Email без @ должен блокировать отправку новой формы.
    driver.get(URL)  # Новая страница: результат предыдущего теста очищен.
    driver.find_element(*FULL_NAME_FIELD).send_keys(FULL_NAME)
    email_field = driver.find_element(*EMAIL_FIELD)
    email_field.send_keys("ivan.example.com")
    submit_form(driver)

    assert email_field.get_property("validity")["typeMismatch"], (
        "Браузер должен распознать неверный формат email"
    )
    assert not driver.find_element(*OUTPUT_BOX).is_displayed(), (
        "При неверном email результат не должен отображаться"
    )
    print("OK: email без @ отклонён")


def check_unusual_name(driver, name, scenario):
    # Проверяет приём и точный вывод необычного имени как текста.
    driver.get(URL)
    name_field = driver.find_element(*FULL_NAME_FIELD)
    name_field.send_keys(name)
    assert name_field.get_property("value") == name, (
        f"{scenario}: введённое имя изменилось или обрезалось"
    )
    driver.find_element(*EMAIL_FIELD).send_keys(EMAIL)
    submit_form(driver)

    result = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#output #name"))
    )
    assert result.text == f"Name:{name}", (
        f"{scenario}: имя в результате изменилось или обрезалось"
    )
    assert not result.find_elements(By.XPATH, "./*"), (
        f"{scenario}: внутри результата появились HTML-элементы"
    )
    print(f"OK: {scenario}")


driver = webdriver.Chrome()
try:
    driver.get(URL)
    driver.maximize_window()
    time.sleep(PAUSE)

    fill_and_submit(driver, FULL_NAME_FIELD, FULL_NAME)
    fill_and_submit(driver, EMAIL_FIELD, EMAIL)
    fill_and_submit(driver, CURRENT_ADDRESS_FIELD, CURRENT_ADDRESS)
    fill_and_submit(driver, PERMANENT_ADDRESS_FIELD, PERMANENT_ADDRESS)


    # Каждый сценарий открывает чистую форму.
    check_invalid_email(driver)
    check_unusual_name(driver, "A" * 5000, "имя длиной 5000 символов")
    check_unusual_name(driver, '!@#$%^&*()_+{}|:"<>?~`', "спецсимволы в имени")
    # Это проверка вывода строки, а не доказательство защиты базы от SQL-инъекций.
    check_unusual_name(
        driver, "' OR '1'='1'; DROP TABLE users;--", "SQL-строка в имени"
    )

finally:
    driver.quit()