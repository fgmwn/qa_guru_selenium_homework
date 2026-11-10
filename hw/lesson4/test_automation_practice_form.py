import base64
import tempfile
import unittest
from pathlib import Path
from selenium import webdriver
from automation_practice_form_po import AutomationPracticeFormPO

PAUSE = 1


class TestAutomationPracticeForm(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.addCleanup(self.driver.quit)
        self.driver.maximize_window()
        # Новый браузер И новый PO перед каждым тестом.
        self.page = AutomationPracticeFormPO(self.driver, pause=PAUSE)
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.picture = Path(self.directory.name) / 'student.png'
        self.picture.write_bytes(base64.b64decode(
            'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aKZkAAAAASUVORK5CYII='))
        self.assertEqual(self.page.open_form(), 'Practice Form')

    def check_form(self, data, expected_date):
        self.page.fill_in_form(file_name=self.picture, **data)
        self.assertEqual(self.page.get_result_title(), 'Thanks for submitting the form')
        # Проверяем каждую строку и каждый выбранный предмет/хобби, не только первый.
        expected = {
            'Student Name': f"{data['first_name']} {data['last_name']}",
            'Student Email': data['email'], 'Gender': data['gender'],
            'Mobile': data['user_number'], 'Date of Birth': expected_date,
            'Subjects': ', '.join(data['subjects']), 'Hobbies': ', '.join(data['hobbies']),
            'Picture': self.picture.name, 'Address': data['current_address'],
            'State and City': f"{data['state']} {data['city']}",
        }
        rows = self.page.result_table.get_rows()
        self.assertEqual(len(rows), len(expected))
        actual = {}
        for row in rows:
            self.assertEqual(len(row), 2)
            label, value = row
            self.assertNotIn(label, actual, f'Повторная строка: {label}')
            actual[label] = value
        self.assertEqual(actual, expected)
        print('OK: все данные регистрации проверены', flush=True)
        self.page.close_result()

    def test_first_student(self):
        self.check_form(dict(first_name='Dmitry', last_name='Bugaev', email='bugaev@example.com',
            gender='Male', user_number='1234567890', birth_day=(1988, 5, 22),
            subjects=['Maths', 'English'], hobbies=['Sports', 'Music'],
            current_address='Санкт-Петербург, Невский проспект, 101', state='NCR', city='Noida'),
            '22 May 1988')

    def test_second_student(self):
        self.check_form(dict(first_name='Анна', last_name='Петрова', email='anna@example.com',
            gender='Female', user_number='9991234567', birth_day=(2000, 7, 15),
            subjects=['Physics', 'Chemistry'], hobbies=['Reading'],
            current_address='Москва, ул. Пушкина, 10', state='Haryana', city='Karnal'),
            '15 Jul 2000')

    def test_third_student(self):
        self.check_form(dict(first_name='Alex', last_name='Smith', email='alex@example.com',
            gender='Other', user_number='9876543210', birth_day=(2024, 2, 29),
            subjects=['Computer Science'], hobbies=['Music'],
            current_address='Jaipur, 20', state='Rajasthan', city='Jaipur'),
            '29 Feb 2024')


if __name__ == '__main__':
    unittest.main(verbosity=2)
