import time
from selenium import webdriver
from selenium.webdriver.common.by import By


# ==== Настройки: меняем здесь — меняется везде ====
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

# Пауза между шагами (одно место вместо десяти)
PAUSE = 5


def fill_and_submit(driver, field, value):
    """Заполняет поле, жмёт submit, проверяет, что значение попало в output."""
    driver.find_element(*field).send_keys(value)
    time.sleep(PAUSE)

    driver.find_element(*SUBMIT_BUTTON).click()
    time.sleep(PAUSE)

    result_box = driver.find_element(*OUTPUT_BOX)
    assert value in result_box.text, f"Не найдено '{value}' в выводе: {result_box.text}"
    print(f"OK: {value}")


driver = webdriver.Chrome()
try:
    driver.get(URL)
    driver.maximize_window()
    time.sleep(PAUSE)

    fill_and_submit(driver, FULL_NAME_FIELD, FULL_NAME)
    fill_and_submit(driver, EMAIL_FIELD, EMAIL)
    fill_and_submit(driver, CURRENT_ADDRESS_FIELD, CURRENT_ADDRESS)
    fill_and_submit(driver, PERMANENT_ADDRESS_FIELD, PERMANENT_ADDRESS)

finally:
    driver.quit()