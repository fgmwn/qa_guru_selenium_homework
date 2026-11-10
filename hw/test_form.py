import unittest
from selenium import webdriver
from pages.text_box_page import TextBoxPage

PAUSE = 0
FULL_NAME = "Петя Иванов"
EMAIL = "petya@yandex.com"
CURRENT_ADDRESS = "ул. Пушкина, д. Калатушкино"
PERMANENT_ADDRESS = "ул. Лермонтова, д. 20"


class TestTextBox(unittest.TestCase):
    def setUp(self):
        print(f"\nСТАРТ: {self._testMethodName}", flush=True)
        self.driver = webdriver.Chrome()
        self.addCleanup(self.driver.quit)
        self.driver.maximize_window()
        self.page = TextBoxPage(self.driver, pause=PAUSE)
        self.page.open()

    def test_all_fields(self):
        self.page.fill_name(FULL_NAME)
        self.page.fill_email(EMAIL)
        self.page.fill_current_address(CURRENT_ADDRESS)
        self.page.fill_permanent_address(PERMANENT_ADDRESS)
        self.page.submit()
        expected = {
            "name": f"Name:{FULL_NAME}",
            "email": f"Email:{EMAIL}",
            "current_address": f"Current Address :{CURRENT_ADDRESS}",
            "permanent_address": f"Permananet Address :{PERMANENT_ADDRESS}",
        }
        self.assertEqual(self.page.get_results(), expected)
        print("OK: все четыре поля проверены", flush=True)

    def test_invalid_email(self):
        self.page.fill_name(FULL_NAME)
        self.page.fill_email("ivan.example.com")
        self.page.submit()
        self.assertTrue(self.page.is_email_format_invalid())
        self.assertFalse(self.page.is_output_visible())
        print("OK: email без @ отклонён", flush=True)

    def check_unusual_name(self, name, scenario):
        self.page.fill_name(name)
        self.assertEqual(self.page.get_name_value(), name)
        self.page.fill_email(EMAIL)
        self.page.submit()
        self.assertEqual(self.page.get_name_result(), f"Name:{name}")
        self.assertEqual(self.page.get_name_result_child_count(), 0)
        print(f"OK: {scenario}", flush=True)

    def test_long_name(self):
        self.check_unusual_name("A" * 5000, "имя длиной 5000 символов")

    def test_special_characters(self):
        self.check_unusual_name('!@#$%^&*()_+{}|:"<>?~`', "спецсимволы")

    def test_sql_string(self):
        self.check_unusual_name("' OR '1'='1'; DROP TABLE users;--", "SQL-строка")


if __name__ == "__main__":
    unittest.main(verbosity=2)
