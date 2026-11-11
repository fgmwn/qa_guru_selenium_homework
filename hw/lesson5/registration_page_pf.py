import sys
import time
from datetime import date
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumpagefactory.Pagefactory import PageFactory

HW = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HW))
sys.path.insert(0, str(HW / 'lesson4'))
from automation_practice_form_po import AutomationPracticeFormPO


class CalendarPF(PageFactory):
    locators = {
        'date_input': ('ID', 'dateOfBirthInput'),
        'year_select': ('CLASS_NAME', 'react-datepicker__year-select'),
        'month_select': ('CLASS_NAME', 'react-datepicker__month-select'),
    }

    def __init__(self, driver, pause=1):
        self.driver = driver
        self.timeout = 10
        self.pause = pause
        self.locators = dict(type(self).locators)

    def select_date(self, year, month, day):
        date(year, month, day)
        field = self.date_input
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", field)
        field.click_button()
        self.year_select.select_element_by_value(str(year))
        time.sleep(self.pause)
        self.month_select.select_element_by_index(month - 1)
        time.sleep(self.pause)
        self.locators['target_day'] = ('CSS',
            f'.react-datepicker__day--{day:03d}:not(.react-datepicker__day--outside-month)')
        self.target_day.click_button()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, 'datepickerRoot')))
        print(f'ШАГ: PF выбрал дату {day:02d}.{month:02d}.{year}', flush=True)


class RegistrationPagePF(AutomationPracticeFormPO, PageFactory):
    def __init__(self, driver, timeout=10, pause=1):
        super().__init__(driver, timeout=timeout, pause=pause)
        self.timeout = timeout
        self.locators = {}
        self.calendar = CalendarPF(driver, pause=pause)

    def _pf_element(self, locator):
        types = {By.ID: 'ID', By.CSS_SELECTOR: 'CSS', By.XPATH: 'XPATH'}
        self.locators['active_element'] = (types[locator[0]], locator[1])
        return self.active_element

    def _click(self, locator):
        element = self._pf_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        element.click_button()
        self._pause()

    def _fill(self, locator, value):
        element = self._pf_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        element.clear_text()
        element.set_text(value)
        print(f'ШАГ: PF заполнил {locator[1]}', flush=True)
        self._pause()

    def fill_form(self, **data):
        self.fill_in_form(**data)
        return self

    def get_modal_results(self):
        self.get_result_title()
        rows = self.result_table.get_rows()
        result = {}
        for row in rows:
            if len(row) != 2:
                raise ValueError(f'Неверная структура строки: {row}')
            label, value = row
            if label in result:
                raise ValueError(f'Повторная строка: {label}')
            result[label] = value
        return result
