"""Page Object формы Text Box: локаторы и взаимодействие со страницей."""
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class TextBoxPage:
    URL = "https://qa-guru.github.io/one-page-form/text-box.html"
    _NAME = (By.ID, "userName")
    _EMAIL = (By.ID, "userEmail")
    _CURRENT_ADDRESS = (By.CSS_SELECTOR, "#userForm #currentAddress")
    _PERMANENT_ADDRESS = (By.CSS_SELECTOR, "#userForm #permanentAddress")
    _SUBMIT = (By.ID, "submit")
    _OUTPUT = (By.ID, "output")
    _RESULT_NAME = (By.CSS_SELECTOR, "#output #name")

    def __init__(self, driver, timeout=10, pause=5):
        self._driver = driver
        self._wait = WebDriverWait(driver, timeout)
        self._pause = pause

    def open(self):
        self._driver.get(self.URL)
        self._wait.until(EC.visibility_of_element_located(self._NAME))
        time.sleep(self._pause)

    def _fill(self, locator, value):
        field = self._wait.until(EC.element_to_be_clickable(locator))
        field.clear()
        field.send_keys(value)
        print(f"ШАГ: заполнено поле {locator[1]} ({len(value)} символов)", flush=True)
        time.sleep(self._pause)

    def fill_name(self, value):
        self._fill(self._NAME, value)

    def fill_email(self, value):
        self._fill(self._EMAIL, value)

    def fill_current_address(self, value):
        self._fill(self._CURRENT_ADDRESS, value)

    def fill_permanent_address(self, value):
        self._fill(self._PERMANENT_ADDRESS, value)

    def submit(self):
        button = self._wait.until(EC.element_to_be_clickable(self._SUBMIT))
        self._driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
        button.click()
        time.sleep(self._pause)

    def is_email_format_invalid(self):
        return self._driver.find_element(*self._EMAIL).get_property("validity")["typeMismatch"]

    def is_output_visible(self):
        return self._driver.find_element(*self._OUTPUT).is_displayed()

    def get_name_value(self):
        return self._driver.find_element(*self._NAME).get_property("value")

    def get_name_result(self):
        return self._wait.until(EC.visibility_of_element_located(self._RESULT_NAME)).text

    def get_name_result_child_count(self):
        result = self._wait.until(EC.visibility_of_element_located(self._RESULT_NAME))
        return len(result.find_elements(By.XPATH, "./*"))

    def get_results(self):
        self._wait.until(EC.visibility_of_element_located(self._OUTPUT))
        # Поиск ограничен output: на странице повторяются ID адресов.
        return {
            name: self._driver.find_element(By.CSS_SELECTOR, f"#output #{element_id}").text
            for name, element_id in [
                ("name", "name"), ("email", "email"),
                ("current_address", "currentAddress"),
                ("permanent_address", "permanentAddress"),
            ]
        }
