"""Решение TODO: Page Object использует готовые Calendar и ResultTable."""
import sys
from pathlib import Path
from selenium.webdriver.common.by import By

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from pages.registration_page import RegistrationPage


class AutomationPracticeFormPO(RegistrationPage):
    def fill_in_form(self, *, file_name, first_name, last_name, email, gender,
                     user_number, birth_day, subjects, hobbies, current_address, state, city):
        # Именованные аргументы защищают от путаницы в длинном списке данных.
        # Подготовка браузера, открытие страницы и проверки остаются у теста.
        self.fill_first_name(first_name)
        self.fill_last_name(last_name)
        self.fill_email(email)
        self._click((By.CSS_SELECTOR, f"label:has(input[name='gender'][value='{gender}'])"))
        self.fill_mobile(user_number)
        self.calendar.select_date(*birth_day)
        for subject in subjects:
            self._fill((By.ID, 'subjectsInput'), subject)
            self._click((By.XPATH, f"//*[@id='subjectsDropdown']/*[normalize-space()='{subject}']"))
        for hobby in hobbies:
            # Ошибки поиска не перехватываем: иначе тест может продолжить без выбора.
            self._click((By.CSS_SELECTOR, f"#hobbiesWrapper label:has(input[value='{hobby}'])"))
        self.upload_picture(file_name)
        self.fill_address(current_address)
        self._click((By.ID, 'state'))
        self._click((By.XPATH, f"//*[@id='stateCity-wrapper']/*[normalize-space()='{state}']"))
        self._click((By.ID, 'city'))
        self._click((By.XPATH, f"//*[@id='stateCity-wrapper']/*[normalize-space()='{city}']"))
        self.submit()
