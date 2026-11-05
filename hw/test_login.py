import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait




URL = "https://qa-guru.github.io/one-page-form/login.html"
LOGIN_FIELD = (By.ID, "login-input")
PASSWORD_FIELD = (By.ID, "password-input")
LOGIN_BUTTON = (By.ID, "submit-button")
LOGOUT_BUTTON = (By.ID, "logout-button")
WELCOME_MESSAGE = (By.ID, "welcome-message")
ERROR_MESSAGE = (By.ID, "error-message")
LOGIN_FORM = (By.ID, "login-form")
SUCCESS_PANEL = (By.ID, "success-panel")

VALID_LOGIN = "user1"
VALID_PASSWORD = "password1"
WRONG_CREDENTIALS = "Wrong login or password"

# Пауза для наблюдения за действиями.
PAUSE = 3

def open_login_page(driver):
    driver.get(URL)
    time.sleep(PAUSE)
    # После успешного входа сайт запоминает пользователя даже при перезагрузке.
    # Выходим через интерфейс, чтобы следующий сценарий начал с чистой формы.
    logout_button = driver.find_element(*LOGOUT_BUTTON)
    if logout_button.is_displayed():
        click_button(driver, LOGOUT_BUTTON)
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(LOGIN_FORM))


def click_button(driver, locator):
    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(locator))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
    button.click()
    time.sleep(PAUSE)


def fill_login_form(driver, login, password):
    login_field = driver.find_element(*LOGIN_FIELD)
    password_field = driver.find_element(*PASSWORD_FIELD)
    login_field.clear()
    password_field.clear()
    login_field.send_keys(login)
    time.sleep(PAUSE)
    password_field.send_keys(password)
    time.sleep(PAUSE)


def check_successful_login(driver):
    message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(WELCOME_MESSAGE)
    )
    assert message.text == f"Welcome, {VALID_LOGIN}!", "Неверное приветствие"
    assert not driver.find_element(*LOGIN_FORM).is_displayed(), "Форма входа не скрыта"
    assert driver.find_element(*LOGOUT_BUTTON).is_displayed(), "Нет кнопки выхода"


def test_valid_login(driver):
    open_login_page(driver)
    fill_login_form(driver, VALID_LOGIN, VALID_PASSWORD)
    click_button(driver, LOGIN_BUTTON)
    check_successful_login(driver)
    print("OK: успешный вход")


def test_invalid_login(driver, login, password, expected_error, scenario):
    open_login_page(driver)
    fill_login_form(driver, login, password)
    click_button(driver, LOGIN_BUTTON)
    message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(ERROR_MESSAGE)
    )
    assert message.text == expected_error, (
        f"{scenario}: ожидали {expected_error!r}, получили {message.text!r}"
    )
    assert driver.find_element(*LOGIN_FORM).is_displayed(), "Форма входа скрыта"
    assert not driver.find_element(*SUCCESS_PANEL).is_displayed(), (
        f"{scenario}: пользователь не должен войти"
    )
    print(f"OK: {scenario}")


def test_logout(driver):
    open_login_page(driver)
    fill_login_form(driver, VALID_LOGIN, VALID_PASSWORD)
    click_button(driver, LOGIN_BUTTON)
    check_successful_login(driver)
    click_button(driver, LOGOUT_BUTTON)
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(LOGIN_FORM))
    assert not driver.find_element(*SUCCESS_PANEL).is_displayed()
    assert driver.find_element(*LOGIN_FIELD).get_property("value") == ""
    assert driver.find_element(*PASSWORD_FIELD).get_property("value") == ""
    # Выход должен сохраняться после перезагрузки страницы.
    driver.refresh()
    time.sleep(PAUSE)
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(LOGIN_FORM))
    assert not driver.find_element(*SUCCESS_PANEL).is_displayed()
    print("OK: выход из аккаунта")


def main():
    driver = webdriver.Chrome()
    try:
        driver.maximize_window()
        test_valid_login(driver)

        # Данные и ожидаемые результаты отделены от повторяющихся шагов.
        invalid_cases = [
            ("user2", VALID_PASSWORD, WRONG_CREDENTIALS, "неверный логин"),
            (VALID_LOGIN, "password2", WRONG_CREDENTIALS, "неверный пароль"),
            ("", "", "Login and password are required (minimum 3 and 6 characters)", "пустые поля"),
            ("", VALID_PASSWORD, "Login is required (minimum 3 characters)", "пустой логин"),
            (VALID_LOGIN, "", "Password is required (minimum 6 characters)", "пустой пароль"),
            ("ab", VALID_PASSWORD, "Login must be at least 3 characters", "короткий логин"),
            (VALID_LOGIN, "12345", "Password must be at least 6 characters", "короткий пароль"),
        ]
        for login, password, error, scenario in invalid_cases:
            test_invalid_login(driver, login, password, error, scenario)

        test_logout(driver)
        print("Все 9 сценариев прошли")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()

