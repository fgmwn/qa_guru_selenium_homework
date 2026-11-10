from datetime import date
from selene import Browser, Config, be


class SeleneCalendar:
    def __init__(self, browser):
        self._browser = browser
        self.input_field = browser.element('#dateOfBirthInput')

    def select_date(self, year, month, day):
        date(year, month, day)
        self.input_field.execute_script("element.scrollIntoView({block: 'center'})")
        self.input_field.click()
        self._browser.element('#datepickerRoot').should(be.visible)
        self._browser.element('.react-datepicker__year-select').click()
        self._browser.element(f'.react-datepicker__year-select option[value="{year}"]').click()
        self._browser.element('.react-datepicker__month-select').click()
        self._browser.element(f'.react-datepicker__month-select option[value="{month - 1}"]').click()
        self._browser.element(
            f'.react-datepicker__day--{day:03d}:not(.react-datepicker__day--outside-month)'
        ).click()
        self._browser.element('#datepickerRoot').should(be.not_.visible)

    def get_value(self):
        return self.input_field.locate().get_property('value')


class SeleneRegistrationPage:
    URL = 'https://qa-guru.github.io/one-page-form/automation-practice-form.html'

    def __init__(self, driver):
        self.browser = Browser(Config(driver=driver, timeout=10))
        self.calendar = SeleneCalendar(self.browser)

    def open(self):
        self.browser.open(self.URL)
        self.browser.element('h1').should(be.visible)
        self.browser.element('#fixedban button[aria-label="Close"]').click()
        self.browser.element('#fixedban').should(be.not_.present)
        return self
