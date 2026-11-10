import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from elements.calendar import Calendar
from elements.result_table import ResultTable

URL = "https://qa-guru.github.io/one-page-form/automation-practice-form.html"

FIRST_NAME = (By.ID, "firstName")
LAST_NAME = (By.ID, "lastName")
EMAIL = (By.ID, "userEmail")
GENDER_MALE = (By.CSS_SELECTOR, "label[for='gender-radio-1']")
MOBILE = (By.ID, "userNumber")
SUBJECT = (By.ID, "subjectsInput")
SUBJECT_OPTION = (By.XPATH, "//*[@id='subjectsDropdown']/*[normalize-space()='Computer Science']")
SPORTS = (By.CSS_SELECTOR, "label[for='hobbies-checkbox-1']")
MUSIC = (By.CSS_SELECTOR, "label[for='hobbies-checkbox-3']")
PICTURE = (By.ID, "uploadPicture")
ADDRESS = (By.ID, "currentAddress")
STATE = (By.ID, "state")
STATE_NCR = (By.XPATH, "//*[@id='stateCity-wrapper']/*[normalize-space()='NCR']")
CITY = (By.ID, "city")
CITY_DELHI = (By.XPATH, "//*[@id='stateCity-wrapper']/*[normalize-space()='Delhi']")
SUBMIT = (By.ID, "submit")
BANNER_CLOSE = (By.CSS_SELECTOR, "#fixedban button[aria-label='Close']")
RESULT_TITLE = (By.ID, "example-modal-sizes-title-lg")
CLOSE_RESULT = (By.ID, "closeModal")
RESULT_MODAL = (By.ID, "resultModal")
FORM_ERROR = (By.ID, "formError")


class RegistrationPage:
    def __init__(self, driver, timeout=10, pause=1):
        # Получаем уже открытый тестом браузер: страница не управляет его жизнью.
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.pause_seconds = pause
        # Страница содержит Page Element, который отвечает только за календарь.
        self.calendar = Calendar(driver, timeout=timeout, pause=pause)
        # Таблица сама знает, как устроены строки и ячейки HTML.
        self.result_table = ResultTable(driver)

    def _pause(self):
        time.sleep(self.pause_seconds)

    def _click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )
        element.click()
        print(f"ШАГ: нажат элемент {locator[1]}", flush=True)
        self._pause()

    def _fill(self, locator, value):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )
        element.clear()
        element.send_keys(value)
        print(f"ШАГ: поле {locator[1]} заполнено: {value!r}", flush=True)
        self._pause()

    def open_form(self):
        self.driver.get(URL)
        title = self.wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1")))
        self._click(BANNER_CLOSE)
        self.wait.until(EC.invisibility_of_element_located((By.ID, "fixedban")))

        print("ШАГ: форма открыта, баннер закрыт", flush=True)
        return title.text

    def fill_first_name(self, value):
        self._fill(FIRST_NAME, value)

    def fill_last_name(self, value):
        self._fill(LAST_NAME, value)

    def fill_email(self, value):
        self._fill(EMAIL, value)

    def fill_mobile(self, value):
        self._fill(MOBILE, value)

    def fill_address(self, value):
        self._fill(ADDRESS, value)

    def select_male(self):
        self._click(GENDER_MALE)

    def select_sports(self):
        self._click(SPORTS)

    def select_music(self):
        self._click(MUSIC)

    def submit(self):
        self._click(SUBMIT)

    def select_computer_science(self):
        self._fill(SUBJECT, "Computer")
        self._click(SUBJECT_OPTION)

    def upload_picture(self, path):
        self.driver.find_element(*PICTURE).send_keys(str(path))
        print("ШАГ: картинка загружена", flush=True)
        self._pause()

    def select_ncr_delhi(self):
        self._click(STATE)
        self._click(STATE_NCR)
        self._click(CITY)
        self._click(CITY_DELHI)

    def get_result_title(self):
        return self.wait.until(EC.visibility_of_element_located(RESULT_TITLE)).text

    def get_error_message(self):
        return self.wait.until(EC.visibility_of_element_located(FORM_ERROR)).text

    def is_result_visible(self):
        return self.driver.find_element(*RESULT_MODAL).is_displayed()

    def close_result(self):
        self._click(CLOSE_RESULT)
        self.wait.until(EC.invisibility_of_element_located(RESULT_MODAL))
