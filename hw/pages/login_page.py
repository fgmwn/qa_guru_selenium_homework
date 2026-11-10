import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class LoginPage:
    URL = "https://qa-guru.github.io/one-page-form/login.html"
    _LOGIN = (By.ID, "login-input")
    _PASSWORD = (By.ID, "password-input")
    _SUBMIT = (By.ID, "submit-button")
    _LOGOUT = (By.ID, "logout-button")
    _WELCOME = (By.ID, "welcome-message")
    _ERROR = (By.ID, "error-message")
    _FORM = (By.ID, "login-form")
    _SUCCESS = (By.ID, "success-panel")

    def __init__(self, driver, timeout=10, pause=0):
        self._driver = driver
        self._wait = WebDriverWait(driver, timeout)
        self._pause = pause

    def open(self):
        self._driver.get(self.URL)
        time.sleep(self._pause)
        # При повторном открытии сайт может помнить вход в этой сессии.
        if self.is_logout_visible():
            self.logout()
        self._wait.until(EC.visibility_of_element_located(self._FORM))
        print("ШАГ: открыта форма входа", flush=True)

    def _click(self, locator):
        button = self._wait.until(EC.element_to_be_clickable(locator))
        self._driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
        button.click()
        time.sleep(self._pause)

    def _fill(self, locator, value):
        field = self._wait.until(EC.element_to_be_clickable(locator))
        field.clear()
        field.send_keys(value)
        time.sleep(self._pause)

    def login(self, login, password):
        self._fill(self._LOGIN, login)
        print(f"ШАГ: введён логин {login!r}", flush=True)
        self._fill(self._PASSWORD, password)
        print("ШАГ: заполнено поле пароля", flush=True)
        self._click(self._SUBMIT)
        print("ШАГ: нажата кнопка входа", flush=True)

    def get_welcome_message(self):
        return self._wait.until(EC.visibility_of_element_located(self._WELCOME)).text

    def get_error_message(self):
        return self._wait.until(EC.visibility_of_element_located(self._ERROR)).text

    def is_form_visible(self):
        return self._driver.find_element(*self._FORM).is_displayed()

    def is_success_visible(self):
        return self._driver.find_element(*self._SUCCESS).is_displayed()

    def is_logout_visible(self):
        return self._driver.find_element(*self._LOGOUT).is_displayed()

    def logout(self):
        self._click(self._LOGOUT)
        self._wait.until(EC.visibility_of_element_located(self._FORM))
        print("ШАГ: выполнен выход", flush=True)

    def get_login_value(self):
        return self._driver.find_element(*self._LOGIN).get_property("value")

    def get_password_value(self):
        return self._driver.find_element(*self._PASSWORD).get_property("value")

    def refresh(self):
        self._driver.refresh()
        self._wait.until(EC.visibility_of_element_located(self._FORM))
        time.sleep(self._pause)
