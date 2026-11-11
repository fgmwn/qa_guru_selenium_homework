"""Относительные локаторы ищут по расположению элементов на экране."""
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.relative_locator import locate_with


class RelativeLocatorsPage:
    def __init__(self, driver, pause=1):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.pause = pause

    def open_text_box(self):
        self.driver.get('https://qa-guru.github.io/one-page-form/text-box.html')
        self.wait.until(EC.visibility_of_element_located((By.ID, 'userName')))
        return self

    def open_registration(self):
        # В Text Box нет радиокнопок: для left/right нужна другая страница.
        self.driver.get('https://qa-guru.github.io/one-page-form/automation-practice-form.html')
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#fixedban button'))).click()
        self.wait.until(EC.invisibility_of_element_located((By.ID, 'fixedban')))
        return self

    def fill_email_below_name(self, email):
        name = self.driver.find_element(By.ID, 'userName')
        field = self.driver.find_element(locate_with(By.CSS_SELECTOR, '#userForm input').below(name))
        field.send_keys(email)
        time.sleep(self.pause)
        return field.get_attribute('id'), field.get_property('value')

    def fill_name_above_email(self, name):
        email = self.driver.find_element(By.ID, 'userEmail')
        field = self.driver.find_element(locate_with(By.CSS_SELECTOR, '#userForm input').above(email))
        field.send_keys(name)
        time.sleep(self.pause)
        return field.get_attribute('id'), field.get_property('value')

    def _select_relative_gender(self, relative_locator):
        # Кликаем видимую подпись, связанную с radio, а не скрытый input.
        label = self.driver.find_element(relative_locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", label)
        label.click()
        time.sleep(self.pause)
        radio = label.find_element(By.TAG_NAME, 'input')
        return radio.get_property('value'), radio.is_selected()

    def select_gender_left_of_female(self):
        female = self.driver.find_element(By.CSS_SELECTOR, '#genterWrapper label:has(input[value="Female"])')
        locator = locate_with(By.CSS_SELECTOR, '#genterWrapper label').to_left_of(female)
        return self._select_relative_gender(locator)

    def select_gender_right_of_male(self):
        male = self.driver.find_element(By.CSS_SELECTOR, '#genterWrapper label:has(input[value="Male"])')
        locator = locate_with(By.CSS_SELECTOR, '#genterWrapper label').to_right_of(male)
        return self._select_relative_gender(locator)

    def fill_address_near_label(self, address):
        label = self.driver.find_element(By.CSS_SELECTOR, 'label[for="currentAddress"]')
        # Стандартного радиуса near (50 px) мало для подписи слева от широкого поля.
        locator = locate_with(By.CSS_SELECTOR, '#userForm textarea').near(label, 300)
        field = self.driver.find_element(locator)
        field.send_keys(address)
        time.sleep(self.pause)
        return field.get_attribute('id'), field.get_property('value')
