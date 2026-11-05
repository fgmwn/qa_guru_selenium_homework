import base64
import tempfile
import time
import unittest
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


URL = "https://qa-guru.github.io/one-page-form/automation-practice-form.html"
PAUSE = 3  # Для наблюдения за шагами.
TIMEOUT = 10  # Максимальное ожидание готовности элемента.

FIRST_NAME = (By.ID, "firstName")
LAST_NAME = (By.ID, "lastName")
EMAIL = (By.ID, "userEmail")
GENDER_MALE = (By.CSS_SELECTOR, "label[for='gender-radio-1']")
MOBILE = (By.ID, "userNumber")
BIRTH_DATE = (By.ID, "dateOfBirthInput")
MONTH = (By.CLASS_NAME, "react-datepicker__month-select")
YEAR = (By.CLASS_NAME, "react-datepicker__year-select")
DAY_25 = (By.CSS_SELECTOR, ".react-datepicker__day--025:not(.react-datepicker__day--outside-month)")
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
RESULT_ROWS = (By.CSS_SELECTOR, "#resultBody tr")
CLOSE_RESULT = (By.ID, "closeModal")
RESULT_MODAL = (By.ID, "resultModal")


class TestStudentRegistration(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, TIMEOUT)
        self.temp_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_directory.cleanup)
        self.picture_path = Path(self.temp_directory.name) / "student.png"
        self.picture_path.write_bytes(base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aKZkAAAAASUVORK5CYII="
        ))

    def tearDown(self):
        self.driver.quit()

    def pause(self):
        time.sleep(PAUSE)

    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )
        element.click()
        self.pause()

    def fill(self, locator, value):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )
        element.clear()
        element.send_keys(value)
        self.pause()

    def select_birth_date(self):
        self.click(BIRTH_DATE)
        month = self.wait.until(EC.visibility_of_element_located(MONTH))
        Select(month).select_by_value("11") 
        self.pause()
        year = self.wait.until(EC.visibility_of_element_located(YEAR))
        Select(year).select_by_value("1995")
        self.pause()
        self.click(DAY_25)
        self.wait.until(EC.invisibility_of_element_located((By.ID, "datepickerRoot")))
        self.assertEqual(
            self.driver.find_element(*BIRTH_DATE).get_property("value"), "25 Dec 1995"
        )

    def test_fill_entire_form(self):
        self.driver.get(URL)
        title = self.wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1")))
        self.assertEqual(title.text, "Practice Form")
        self.click(BANNER_CLOSE)
        self.wait.until(EC.invisibility_of_element_located((By.ID, "fixedban")))

        self.fill(FIRST_NAME, "Пётр")
        self.fill(LAST_NAME, "Калатушкин")
        self.fill(EMAIL, "petr.kalatushkin@yandex.com")
        self.click(GENDER_MALE)
        self.fill(MOBILE, "+79991234567")
        self.select_birth_date()
        self.fill(SUBJECT, "Computer")
        self.click(SUBJECT_OPTION)
        self.click(SPORTS)
        self.click(MUSIC)
        self.driver.find_element(*PICTURE).send_keys(str(self.picture_path))
        self.pause()
        self.fill(ADDRESS, "Москва, ул. Пушкина, д. 10")
        self.click(STATE)
        self.click(STATE_NCR)
        self.click(CITY)
        self.click(CITY_DELHI)
        self.click(SUBMIT)

        modal_title = self.wait.until(EC.visibility_of_element_located(RESULT_TITLE))
        self.assertEqual(modal_title.text, "Thanks for submitting the form")

        expected = {
            "Student Name": "Пётр Калатушкин",
            "Student Email": "petr.kalatushkin@yandex.com",
            "Gender": "Male",
            "Mobile": "+79991234567",
            "Date of Birth": "25 Dec 1995",
            "Subjects": "Computer Science",
            "Hobbies": "Sports, Music",
            "Picture": "student.png",
            "Address": "Москва, ул. Пушкина, д. 10",
            "State and City": "NCR Delhi",
        }
        rows = self.driver.find_elements(*RESULT_ROWS)
        self.assertEqual(len(rows), len(expected))
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            self.assertEqual(len(cells), 2)
            label, value = cells[0].text, cells[1].text
            self.assertIn(label, expected)
            self.assertEqual(value, expected[label], f"Неверное значение: {label}")

        self.click(CLOSE_RESULT)
        self.wait.until(EC.invisibility_of_element_located(RESULT_MODAL))


if __name__ == "__main__":
    unittest.main(verbosity=2)
