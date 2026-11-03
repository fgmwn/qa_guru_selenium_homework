from typing import Tuple
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from pages.elements.calendar import Calendar


class BasePage:

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.default_timeout = 10
        self.wait = WebDriverWait(self.driver, self.default_timeout)
        self.calendar = Calendar(self)

    def open_url(self, url: str):
        """Открыть урл и развернуть окно на весь экран"""
        self.driver.get(url)
        self.driver.maximize_window()

    def wait_for_element_visible(self, locator: Tuple[str, str]):
        """Ожидание появления элемента на странице"""
        return self.wait.until(ec.visibility_of_element_located(locator))

    def wait_for_element_clickable(self, locator: Tuple[str, str]):
        """Ожидание пока элемента станет кликабельным"""
        return self.wait.until(ec.element_to_be_clickable(locator))

    def wait_for_element_text(self, locator: Tuple[str, str], text: str) -> bool:
        """Возвращает текст элемента"""
        return self.wait.until(ec.text_to_be_present_in_element(locator, text))

    def click_element(self, locator: Tuple[str, str]):
        """Ожидание кликабельности элемента и клик по нему"""
        element = self.wait_for_element_clickable(locator)
        element.click()

    def input_text(self, locator: Tuple[str, str], text: str):
        """Ожидание доступности поля, очистка поля и ввод значения в поле"""
        element = self.wait_for_element_clickable(locator)
        element.clear()
        element.send_keys(text)

    def get_element_text(self, locator: Tuple[str, str]) -> str:
        """Ожидание видимости элемента и возврщение его текста"""
        element = self.wait_for_element_visible(locator)
        return element.text

    def get_element_attribute(self, locator: Tuple[str, str], attribute_name: str = "value"):
        """Ожидание видимости элемента и возвращение его атрибута"""
        element = self.wait_for_element_visible(locator)
        return element.get_attribute(attribute_name)

    def get_validation_message(self, locator: Tuple[str, str]):
        """Получить текст валидации браузера для поля"""
        element = self.wait_for_element_visible(locator)
        return self.driver.execute_script("return arguments[0].validationMessage;",element)

    def scroll_to_footer(self):
        """Прокрутить страницу вниз до футера и скрыть его"""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.driver.execute_script("document.getElementsByTagName('footer')[0].style.display='none';")

    def scroll_to_element(self, locator: Tuple[str, str]):
        """Найти элемент в DOM дереве и отцентровать"""
        element = self.wait.until(ec.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        return element

    def wait_for_element_present(self, locator: Tuple[str, str]):
        """Ожидание появления элемента в DOM, даже если он скрыт"""
        return self.wait.until(ec.presence_of_element_located(locator))

    def upload_file(self, locator: Tuple[str, str], file_path: str):
        """Найти инпут загрузки файла в HTML (DOM) и передать туда путь к файлу"""
        element = self.wait_for_element_present(locator)
        element.send_keys(file_path)
