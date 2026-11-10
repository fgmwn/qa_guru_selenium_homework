import sys
import unittest
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from calendar_selene import SeleneRegistrationPage

# Элемент Selenium уже реализован в основном решении домашки.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from elements.calendar import Calendar


class CalendarChecks:
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.addCleanup(self.driver.quit)
        self.driver.maximize_window()
        self.prepare_calendar()

    def test_lesson_date(self):
        self.calendar.select_date(2000, 7, 15)
        self.assertEqual(self.calendar.get_value(), '15 Jul 2000')

    def test_single_digit_day(self):
        self.calendar.select_date(1995, 12, 1)
        self.assertEqual(self.calendar.get_value(), '01 Dec 1995')

    def test_leap_day(self):
        self.calendar.select_date(2024, 2, 29)
        self.assertEqual(self.calendar.get_value(), '29 Feb 2024')


class TestSeleneCalendar(CalendarChecks, unittest.TestCase):
    def prepare_calendar(self):
        self.page = SeleneRegistrationPage(self.driver).open()
        self.calendar = self.page.calendar


class TestSeleniumCalendar(CalendarChecks, unittest.TestCase):
    def prepare_calendar(self):
        self.driver.get(SeleneRegistrationPage.URL)
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#fixedban button'))).click()
        wait.until(EC.invisibility_of_element_located((By.ID, 'fixedban')))
        self.calendar = Calendar(self.driver, pause=0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
