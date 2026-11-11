import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class DragDropPage:
    URL = 'https://the-internet.herokuapp.com/drag_and_drop'
    _LEFT = (By.ID, 'column-a')
    _RIGHT = (By.ID, 'column-b')

    def __init__(self, driver, timeout=10, pause=1):
        self._driver = driver
        self._wait = WebDriverWait(driver, timeout)
        self._pause = pause

    def open(self):
        self._driver.get(self.URL)
        self._wait.until(EC.visibility_of_element_located(self._LEFT))
        self._wait.until(EC.visibility_of_element_located(self._RIGHT))
        time.sleep(self._pause)
        return self

    def get_labels(self):
        return (
            self._driver.find_element(*self._LEFT).find_element(By.TAG_NAME, 'header').text,
            self._driver.find_element(*self._RIGHT).find_element(By.TAG_NAME, 'header').text,
        )

    def wait_for_labels(self, left, right):
        self._wait.until(lambda driver: self.get_labels() == (left, right),
                         message=f'Ожидались надписи {(left, right)}')
        return self

    def _drag(self, source_locator, target_locator):
        source = self._wait.until(EC.element_to_be_clickable(source_locator))
        target = self._wait.until(EC.element_to_be_clickable(target_locator))
        ActionChains(self._driver).drag_and_drop(source, target).perform()
        print('ШАГ: выполнен перенос блока мышью', flush=True)
        time.sleep(self._pause)
        return self

    def drag_left_to_right(self):
        return self._drag(self._LEFT, self._RIGHT)

    def drag_right_to_left(self):
        return self._drag(self._RIGHT, self._LEFT)
