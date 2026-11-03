import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec


class PracticeForm:

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 5)
        self.url = "https://qa-guru.github.io/one-page-form/automation-practice-form.html"

    PRACTICE_FORM_TITLE = (By.XPATH, "//main//h1")
    FIRST_NAME_FIELD = (By.ID, "firstName")
    LAST_NAME_FIELD = (By.ID, "lastName")
    EMAIL_FIELD = (By.ID, "userEmail")
    USER_NUMBER_FIELD = (By.ID, "userNumber")
    CALENDAR_INPUT = (By.ID, "dateOfBirthInput")
    YEAR_OF_BIRTH_SELECT = (By.CSS_SELECTOR, ".react-datepicker__year-select")
    MONTH_OF_BIRTH_SELECT = (By.CSS_SELECTOR, ".react-datepicker__month-select")
    SUBJECT_FIELD = (By.ID, "subjectsInput")
    UPLOAD_PICTURE_BUTTON = (By.ID, "uploadPicture")
    CURRENT_ADDRESS_FIELD = (By.ID, "currentAddress")
    STATE_INPUT = (By.ID, "state")
    CITY_INPUT = (By.ID, "city")
    SUBMIT_BUTTON = (By.ID, "submit")
    BANNER_BUTTON = (By.XPATH, "//div[@id='fixedban']//button[@aria-label='Close']")
    RESULT_FORM = (By.ID, "resultModal")

    def setup(self):
        self.driver.set_window_size(1280, 720)
        self.driver.get(self.url)
        self.test_file = self.create_test_file()

    def close_commercial_banner(self):
        banner_button = self.wait.until(ec.element_to_be_clickable(self.BANNER_BUTTON))
        banner_button.click()

    def fill_first_name(self, first_name):
        firstname_field = self.driver.find_element(*self.FIRST_NAME_FIELD)
        firstname_field.send_keys(first_name)

    def fill_last_name(self, last_name):
        lastname_field = self.driver.find_element(*self.LAST_NAME_FIELD)
        lastname_field.send_keys(last_name)

    def fill_email(self, email):
        email_field = self.driver.find_element(*self.EMAIL_FIELD)
        email_field.send_keys(email)

    def fill_user_number(self, user_number):
        user_number_field = self.driver.find_element(*self.USER_NUMBER_FIELD)
        user_number_field.send_keys(user_number)

    def select_gender(self, gender):
        gender_radio_button = self.driver.find_element(By.XPATH,
                                                       f"//div[@id='genterWrapper']//input[@value='{gender}']")
        gender_radio_button.click()

    def select_birth_day(self, year, month, day):
        self.driver.find_element(*self.CALENDAR_INPUT).click()
        Select(self.driver.find_element(*self.YEAR_OF_BIRTH_SELECT)).select_by_value(year)
        Select(self.driver.find_element(*self.MONTH_OF_BIRTH_SELECT)).select_by_value(month)
        self.driver.find_element(By.CSS_SELECTOR, f".react-datepicker__day--0{day}[tabindex='0']").click()

    def create_test_file(self):
        file_path = os.path.abspath('test_file.jpg')
        with open(file_path, 'w') as file:
            file.write("Test")
        return file_path

    def upload_file(self, file_path):
        self.driver.find_element(*self.UPLOAD_PICTURE_BUTTON).send_keys(file_path)

    def fill_subject(self, *subjects):
        subjects_input = self.driver.find_element(*self.SUBJECT_FIELD)
        self.driver.execute_script("arguments[0].scrollIntoView();", subjects_input)
        for subject in subjects:
            subjects_input.send_keys(subject)
            subjects_input.send_keys(Keys.ENTER)

    def select_hobbies(self, *hobbies):
        for hobby in hobbies:
            hobby_check_box = self.driver.find_element(By.XPATH,
                                                       f"//div[@id='hobbiesWrapper']//input[@value='{hobby}']")
            hobby_check_box.click()

    def fill_current_address(self, current_address):
        current_address_field = self.driver.find_element(*self.CURRENT_ADDRESS_FIELD)
        current_address_field.send_keys(current_address)

    def select_state(self, state):
        self.driver.find_element(*self.STATE_INPUT).click()
        state_dropdown = self.wait.until(
            ec.element_to_be_clickable((By.XPATH, f"//div[@class='state-city-option'][text()='{state}']")))
        state_dropdown.click()

    def select_city(self, city):
        self.driver.find_element(*self.CITY_INPUT).click()
        city_dropdown = self.wait.until(
            ec.element_to_be_clickable((By.XPATH, f"//div[@class='state-city-option'][text()='{city}']")))
        city_dropdown.click()

    def click_submit_button(self):
        submit_button = self.driver.find_element(*self.SUBMIT_BUTTON)
        self.driver.execute_script("arguments[0].scrollIntoView();", submit_button)
        submit_button.click()

    def final_result_assertion(self):
        result_form = self.wait.until(ec.visibility_of_element_located(self.RESULT_FORM))
        assert result_form.is_displayed(), "Таблица с данным не отобразилась"

        result_text = result_form.text
        expected_data = {
            "Student Name": "Dmitry Bugaev",
            "Student Email": "bugaev@example.com",
            "Gender": "Male",
            "Mobile": "1234567890",
            "Date of Birth": "1988",
            "Subjects": "Maths",
            "Hobbies": "Sports, Music",
            "Picture": "test_file.jpg",
            "Address": "г. Санкт-Петербург, ул. Невский проспект, д 101",
            "State and City": "NCR Noida"
        }

        for key, value in expected_data.items():
            assert key in result_text and value in result_text, f"Значения {value} из строки {key} не совпадают!"

    def test_fill_entire_form(self):
        practice_form_title = self.driver.find_element(*self.PRACTICE_FORM_TITLE)
        assert practice_form_title.text == "Practice Form", "Заголовок страницы не совпадает"

        self.close_commercial_banner()
        self.fill_first_name("Dmitry")
        self.fill_last_name("Bugaev")
        self.fill_email("bugaev@example.com")
        self.select_gender("Male")
        self.fill_user_number("1234567890")
        self.select_birth_day("1988", "4", "22")
        self.fill_subject("Maths", "English")
        self.select_hobbies("Sports", "Music")
        self.upload_file(self.test_file)
        self.fill_current_address("г. Санкт-Петербург, ул. Невский проспект, д 101")
        self.select_state("NCR")
        self.select_city("Noida")
        self.click_submit_button()
        self.final_result_assertion()

    def tear_down(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.driver.quit()


practice_form = PracticeForm()

try:
    practice_form.setup()
    practice_form.test_fill_entire_form()
finally:
    practice_form.tear_down()