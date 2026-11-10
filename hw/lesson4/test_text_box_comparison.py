import unittest
from selenium import webdriver
from text_box_comparison import TextBoxPage, TextBoxPagePF


class TextBoxChecks:
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.addCleanup(self.driver.quit)
        self.driver.maximize_window()
        self.page = self.page_class(self.driver).open()

    def check_data(self, **data):
        self.page.fill_form(**data).submit()
        self.assertTrue(self.page.is_output_visible())
        expected = dict.fromkeys(['name', 'email', 'cur_addr', 'perm_addr'], '')
        expected.update({key: value.strip() for key, value in data.items()})
        self.assertEqual(self.page.get_output_data(), expected)

    def test_all_fields_and_spaces(self):
        self.check_data(name='  Иван  ', email='ivan@example.com', cur_addr=' Адрес 1 ', perm_addr='Адрес 2')

    def test_partial_form(self):
        self.check_data(cur_addr='Только текущий адрес')

    def test_empty_form(self):
        self.check_data()

    def test_invalid_email(self):
        self.page.fill_form(name='Test', email='plainaddress').submit()
        self.assertTrue(self.page.is_email_invalid())
        self.assertFalse(self.page.is_output_visible())

    def test_domain_without_dot(self):
        # type=email принимает адрес без точки в домене: это не проверка DNS.
        self.check_data(email='john@missing-dot')

    def test_long_address(self):
        self.check_data(cur_addr='Current ' * 200)

    def test_sql_as_text(self):
        self.check_data(name="1' OR '1'='1")

    @unittest.expectedFailure
    def test_html_is_shown_as_literal_text(self):
        self.check_data(name='<div>HTML injection</div>')


class TestPlainTextBox(TextBoxChecks, unittest.TestCase):
    page_class = TextBoxPage


class TestFactoryTextBox(TextBoxChecks, unittest.TestCase):
    page_class = TextBoxPagePF


if __name__ == '__main__':
    unittest.main(verbosity=2)
