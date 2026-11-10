import time
from datetime import date

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


class Calendar:
    _INPUT = (By.ID, "dateOfBirthInput")
    _POPUP = (By.ID, "datepickerRoot")
    _MONTH = (By.CLASS_NAME, "react-datepicker__month-select")
    _YEAR = (By.CLASS_NAME, "react-datepicker__year-select")

    def __init__(self, driver, timeout=10, pause=1):
        self._driver = driver
        self._wait = WebDriverWait(driver, timeout)
        self._pause_seconds = pause

    def _click(self, locator):
        element = self._wait.until(EC.element_to_be_clickable(locator))
        self._driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )
        element.click()
        time.sleep(self._pause_seconds)

    def select_date(self, year, month, day):
        date(year, month, day) 
        self._click(self._INPUT)
        self._wait.until(EC.visibility_of_element_located(self._POPUP))
        year_select = self._wait.until(EC.element_to_be_clickable(self._YEAR))
        Select(year_select).select_by_value(str(year))
        time.sleep(self._pause_seconds)
        month_select = self._wait.until(EC.element_to_be_clickable(self._MONTH))
        Select(month_select).select_by_value(str(month - 1))
        time.sleep(self._pause_seconds)
        day_locator = (
            By.CSS_SELECTOR,
            f".react-datepicker__day--{day:03d}:not(.react-datepicker__day--outside-month)",
        )
        self._click(day_locator)
        self._wait.until(EC.invisibility_of_element_located(self._POPUP))
        print(f"ШАГ: выбрана дата {day:02d}.{month:02d}.{year}", flush=True)

    def get_value(self):
        return self._driver.find_element(*self._INPUT).get_property("value")
