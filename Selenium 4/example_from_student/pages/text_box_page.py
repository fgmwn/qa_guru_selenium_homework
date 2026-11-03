from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class TextBoxPage(BasePage):
    URL = "https://qa-guru.github.io/one-page-form/text-box.html"

    EMAIL = (By.CSS_SELECTOR, "#userEmail")
    FULL_NAME = (By.CSS_SELECTOR, "#userName")
    OUTPUT_AREA = (By.CSS_SELECTOR, "#output")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "#submit")
    CURRENT_ADDRESS = (By.CSS_SELECTOR, "#currentAddress")
    PERMANENT_ADDRESS = (By.CSS_SELECTOR, "#permanentAddress")

    def open_mine_url(self):
        self.open_url(self.URL)

    def input_full_name(self, full_name: str):
        self.input_text(self.FULL_NAME, full_name)

    def input_email(self, email: str):
        self.input_text(self.EMAIL, email)

    def input_current_address(self, current_address: str):
        self.input_text(self.CURRENT_ADDRESS, current_address)

    def input_permanent_address(self, permanent_address: str):
        self.input_text(self.PERMANENT_ADDRESS, permanent_address)

    def click_submit_button(self):
        self.click_element(self.SUBMIT_BUTTON)

    def scroll_to_data_output(self):
        self.scroll_to_element(self.OUTPUT_AREA)

    def get_actual_data(self):
        return self.get_element_text(self.OUTPUT_AREA)

    def get_email_validation_message(self):
        return self.get_validation_message(self.EMAIL)
