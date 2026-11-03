from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class LoginPage(BasePage):
    URL = "https://qa-guru.github.io/one-page-form/login.html"

    LOGIN = (By.CSS_SELECTOR, "#login-input")
    PASSWORD = (By.CSS_SELECTOR, "#password-input")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "#submit-button")

    ERROR_MESSAGE = (By.CSS_SELECTOR, "#error-message")

    def open_mine_url(self):
        self.open_url(self.URL)

    def input_login(self, login: str):
        self.input_text(self.LOGIN, login)

    def input_password(self, password: str):
        self.input_text(self.PASSWORD, password)

    def click_login_button(self):
        self.click_element(self.LOGIN_BUTTON)

    def get_error_message(self, error_text: str) -> bool:
        return self.wait_for_element_text(self.ERROR_MESSAGE, error_text)
