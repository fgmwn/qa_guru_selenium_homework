from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class RegistrationPage(BasePage):
    URL = "https://qa-guru.github.io/one-page-form/automation-practice-form.html"

    LAST_NAME = (By.CSS_SELECTOR, "#lastName")
    FIRST_NAME = (By.CSS_SELECTOR, "#firstName")
    CITY_INPUT = (By.CSS_SELECTOR, "#city")
    USER_EMAIL = (By.CSS_SELECTOR, "#userEmail")
    STATE_INPUT = (By.CSS_SELECTOR, "#state")
    MODAL_DIALOG = (By.CSS_SELECTOR, "#example-modal-sizes-title-lg")
    MOBILE_NUMBER = (By.CSS_SELECTOR, "#userNumber")
    BUTTON_SUBMIT = (By.CSS_SELECTOR, "#submit")
    PICTURE_INPUT = (By.CSS_SELECTOR, "#uploadPicture")
    SUBJECTS_INPUT = (By.CSS_SELECTOR, "#subjectsInput")
    CITY_DROP_DOWN = (By.CSS_SELECTOR, "#stateCity-wrapper")
    STATE_DROP_DOWN = (By.CSS_SELECTOR, "#stateCity-wrapper")
    CURRENT_ADDRESS = (By.CSS_SELECTOR, "#currentAddress")
    ERROR_MESSAGE_AREA = (By.CSS_SELECTOR, "#formError")
    MODAL_DIALOG_RESULT = (By.CSS_SELECTOR, "#resultBody")
    SUBJECTS_MENU_OPTION = (By.CSS_SELECTOR, "div[class='subjects-auto-complete__option']")
    # Локаторы гендер, gender_value = gender-radio-1 (2,3)
    GENDER_RADIO_LOCATOR = (By.CSS_SELECTOR, "label:has(input[value='{gender_value}'])")
    # Локаторы хобби
    HOBBIES_MUSIC_INPUT = (By.ID, "hobbies-checkbox-3")
    HOBBIES_SPORTS_INPUT = (By.ID, "hobbies-checkbox-1")
    HOBBIES_READING_INPUT = (By.ID, "hobbies-checkbox-2")
    HOBBY_LABEL_LOCATOR = (By.XPATH, "//label[contains(text(), '{hobby_name}')]")
    HOBBIES_MUSIC_LABEL = (By.CSS_SELECTOR, "label[for='hobbies-checkbox-3']")
    HOBBIES_SPORTS_LABEL = (By.CSS_SELECTOR, "label[for='hobbies-checkbox-1']")
    HOBBIES_READING_LABEL = (By.CSS_SELECTOR, "label[for='hobbies-checkbox-2']")
    # Локаторы полей календаря
    DATE_INPUT = (By.CSS_SELECTOR, "#dateOfBirthInput")
    DAY_OPTION = (By.CSS_SELECTOR,
                  "div.react-datepicker__day--0{padded_day}:not(.react-datepicker__day--outside-month)")
    YEAR_SELECT = (By.CSS_SELECTOR, "select[class='react-datepicker__year-select']")
    MONS_SELECT = (By.CSS_SELECTOR, "select[class='react-datepicker__month-select']")
    CALENDAR_AREA = (By.CSS_SELECTOR, "div[class='react-datepicker__month-container']")

    def open_mine_url(self):
        self.open_url(self.URL)

    def close_banner(self):
        """Закрыть баннер"""
        self.click_element((By.CSS_SELECTOR, "button[aria-label='Close']"))

    def input_first_name(self, first_name: str):
        """Ввести имя"""
        self.input_text(self.FIRST_NAME, first_name)

    def input_last_name(self, last_name: str):
        """Ввести фамилию"""
        self.input_text(self.LAST_NAME, last_name)

    def select_gender(self, gender: str):
        """Выбрать гендер"""
        if gender is None:
            return

        gender_value = gender.strip().capitalize()
        # если значение гендера отлично от [], то ошибка в тестовых данных
        if gender_value not in ["Male", "Female", "Other"]:
            raise ValueError(f"Неверный гендер: '{gender}'. Допустимые варианты: Male, Female, Other")

        # разделение локатора класса на: поиск элемента (by=By.CSS_SEL..) и текст элемента (locator_string="label[for='{gende..)
        by, locator_string = self.GENDER_RADIO_LOCATOR
        # подставление переданного gender_value в текст элемента и сборка кортежа
        dynamic_locator = (by, locator_string.format(gender_value=gender_value))
        self.click_element(dynamic_locator)

    def input_mobile_number(self, mobile_number: str):
        """Ввести номер телефона"""
        self.input_text(self.MOBILE_NUMBER, mobile_number)

    def input_email(self, email: str):
        """Ввести email"""
        self.input_text(self.USER_EMAIL, email)

    def select_date_of_birth(self, day: int, month: int, year: int):
        """Указать дату рождения"""
        self.click_element(self.DATE_INPUT)
        self.wait_for_element_visible(self.CALENDAR_AREA)
        self.calendar.select_date(day, month, year)

    def get_expected_birth_date_text(self, day: int, month: int, year: int) -> str:
        """Получить форматированную строку даты"""
        return self.calendar.format_to_site_date(day, month, year)

    def input_subjects(self, subjects: list | str) -> str:
        """Выбрать предметы"""
        subjects_list = subjects if isinstance(subjects, list) else [subjects]
        input_subject = self.wait_for_element_clickable(self.SUBJECTS_INPUT)

        for subject in subjects:
            input_subject.send_keys(subject)
            specific_option = (By.XPATH,
                               f"//div[contains(@class, 'subjects-auto-complete__option') and text()='{subject}']")
            self.scroll_to_element(specific_option)
            self.click_element(specific_option)

        self.driver.execute_script("arguments[0].blur();", input_subject)
        return ", ".join(subjects_list)

    def select_hobbies(self, hobbies: list | str) -> str:
        """Выбрать хобби"""
        hobbies_list = hobbies if isinstance(hobbies, list) else [hobbies]
        by, locator_string = self.HOBBY_LABEL_LOCATOR

        for hobby_name in hobbies_list:
            dynamic_locator = (by, locator_string.format(hobby_name=hobby_name))
            self.click_element(dynamic_locator)
        return ", ".join(hobbies_list)

    def upload_picture(self, file_path: str):
        """Загрузить файл"""
        self.upload_file(self.PICTURE_INPUT, file_path)

    def input_current_address(self, current_address: str):
        """Ввести адресс"""
        self.input_text(self.CURRENT_ADDRESS, current_address)

    def select_state(self, state_name: str):
        """Выбрать штат"""
        state_option = (By.XPATH, f"//div[@class='state-city-option' and text()='{state_name}']")

        self.click_element(self.STATE_INPUT)
        self.wait_for_element_visible(self.STATE_DROP_DOWN)
        self.scroll_to_element(state_option)
        element = self.driver.find_element(*state_option)
        self.driver.execute_script("arguments[0].click();", element)

    def select_city(self, city_name: str):
        """Выбрать город"""
        city_option = (By.XPATH, f"//div[@class='state-city-option' and text()='{city_name}']")

        self.click_element(self.CITY_INPUT)
        self.wait_for_element_visible(self.CITY_DROP_DOWN)
        self.scroll_to_element(city_option)
        element = self.driver.find_element(*city_option)
        self.driver.execute_script("arguments[0].click();", element)

    def click_submit_button(self):
        """Нажать кнопку отправки"""
        self.click_element(self.BUTTON_SUBMIT)

    def get_result_form(self) -> str:
        """Получить форму с результатами"""
        self.wait_for_element_visible(self.MODAL_DIALOG_RESULT)
        return self.get_element_text(self.MODAL_DIALOG_RESULT)

    def get_error_message(self):
        """Получить текст ошибки"""
        return self.get_element_text(self.ERROR_MESSAGE_AREA)
