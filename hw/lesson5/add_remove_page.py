import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class AddRemovePage:
    URL = 'https://the-internet.herokuapp.com/add_remove_elements/'
    _ADD = (By.XPATH, "//button[text()='Add Element']")
    _DELETE = (By.CSS_SELECTOR, '#elements button.added-manually')

    def __init__(self, driver, timeout=10, pause=1):
        self._driver = driver
        self._wait = WebDriverWait(driver, timeout)
        self._pause = pause

    def open(self):
        self._driver.get(self.URL)
        self._wait.until(EC.element_to_be_clickable(self._ADD))
        return self

    def get_count(self):
        return len(self._driver.find_elements(*self._DELETE))

    def wait_for_count(self, expected):
        self._wait.until(lambda driver: self.get_count() == expected,
                         message=f'Ожидалось кнопок Delete: {expected}')
        return self

    def add_element(self):
        self._wait.until(EC.element_to_be_clickable(self._ADD)).click()
        print('ШАГ: нажата Add Element', flush=True)
        time.sleep(self._pause)
        return self

    def delete_first(self):
        button = self._wait.until(EC.element_to_be_clickable(self._DELETE))
        button.click()
        self._wait.until(EC.staleness_of(button))
        print('ШАГ: удалена первая кнопка Delete', flush=True)
        time.sleep(self._pause)
        return self
