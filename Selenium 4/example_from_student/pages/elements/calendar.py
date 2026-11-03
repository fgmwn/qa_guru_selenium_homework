from selenium.webdriver.common.by import By
import datetime

class Calendar:
    def __init__(self, page):
        self.page = page

        self.CALENDAR_AREA = (By.CSS_SELECTOR, "div[class='react-datepicker__month-container']")
        self.DAY_OPTION = (By.CSS_SELECTOR, "div.react-datepicker__day--0{padded_day}:not(.react-datepicker__day--outside-month)")
        self.YEAR_SELECT = (By.CSS_SELECTOR, "select[class='react-datepicker__year-select']")
        self.MONTH_SELECT = (By.CSS_SELECTOR, "select[class='react-datepicker__month-select']")

    def select_date(self, day: int, month: int, year: int):
        self.page.click_element(self.YEAR_SELECT)
        self.page.click_element((By.CSS_SELECTOR, f"option[value='{year}']"))

        self.page.click_element(self.MONTH_SELECT)
        self.page.click_element((By.CSS_SELECTOR, f"option[value='{month - 1}']"))

        self.page.click_element((By.CSS_SELECTOR, f"span[data-day='{day}']"))

    @staticmethod
    def format_to_site_date(day: int, month: int, year: int) -> str:
        """Конвертирует числовую дату в формат отображения в форме результатов (например: '11 Jul 2008')"""
        date_object = datetime.date(year, month, day)
        month_name = date_object.strftime("%b")
        return f"{day} {month_name} {year}"

