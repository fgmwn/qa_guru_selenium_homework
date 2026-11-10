import base64
import tempfile
import unittest
from pathlib import Path

from selenium import webdriver
# При прямом запуске файла Python ищет пакет pages рядом с этим файлом.
from pages.registration_page import RegistrationPage

PAUSE = 1
TIMEOUT = 10
REQUIRED_FIELDS_ERROR = "Please fill required fields and enter a valid 10-digit mobile number."


class TestStudentRegistration(unittest.TestCase):
    def setUp(self):
        print(f"\nСТАРТ: {self._testMethodName}", flush=True)
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        # Page Object получает тот же браузер, который создаёт и закрывает тест.
        self.page = RegistrationPage(self.driver, timeout=TIMEOUT, pause=PAUSE)
        self.temp_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_directory.cleanup)
        self.picture_path = Path(self.temp_directory.name) / "student.png"
        self.picture_path.write_bytes(base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aKZkAAAAASUVORK5CYII="
        ))

    def tearDown(self):
        self.driver.quit()

    def test_fill_entire_form(self):
        self.assertEqual(self.page.open_form(), "Practice Form")
        self.page.fill_first_name("Пётр")
        self.page.fill_last_name("Калатушкин")
        self.page.fill_email("petr.kalatushkin@yandex.com")
        self.page.select_male()
        self.page.fill_mobile("9991234567")
        self.page.select_birth_date()
        self.assertEqual(self.page.get_birth_date(), "25 Dec 1995")
        self.page.select_computer_science()
        self.page.select_sports()
        self.page.select_music()
        self.page.upload_picture(self.picture_path)
        self.page.fill_address("Москва, ул. Пушкина, д. Калатушкина")
        self.page.select_ncr_delhi()
        self.page.submit()

        self.assertEqual(self.page.get_result_title(), "Thanks for submitting the form")

        expected = {
            "Student Name": "Пётр Калатушкин",
            "Student Email": "petr.kalatushkin@yandex.com",
            "Gender": "Male",
            "Mobile": "9991234567",
            "Date of Birth": "25 Dec 1995",
            "Subjects": "Computer Science",
            "Hobbies": "Sports, Music",
            "Picture": "student.png",
            "Address": "Москва, ул. Пушкина, д. Калатушкина",
            "State and City": "NCR Delhi",
        }
        rows = self.page.get_result_rows()
        self.assertEqual(len(rows), len(expected))
        for row in rows:
            cells = row
            self.assertEqual(len(cells), 2)
            label, value = cells[0], cells[1]
            self.assertIn(label, expected)
            self.assertEqual(value, expected[label], f"Неверное значение: {label}")
            print(f"OK: {label} = {value!r}", flush=True)

        self.page.close_result()
        print("OK: полная регистрация и закрытие результата проверены", flush=True)

    def fill_required_fields(self):
        self.page.fill_first_name("Пётр")
        self.page.fill_last_name("Калатушкин")
        self.page.select_male()
        self.page.fill_mobile("9991234567")

    def check_submission_rejected(self, scenario):
        self.page.submit()
        self.assertEqual(self.page.get_error_message(), REQUIRED_FIELDS_ERROR)
        self.assertFalse(
            self.page.is_result_visible(),
            "Форма с некорректными данными показала окно успеха",
        )
        self.assertEqual(self.page.get_result_rows(), [])
        print(f"OK: {scenario} : ошибка показана, результата регистрации нет", flush=True)

    def test_empty_form(self):
        self.assertEqual(self.page.open_form(), "Practice Form")
        self.check_submission_rejected("все обязательные поля пустые")

    def test_missing_first_name(self):
        self.assertEqual(self.page.open_form(), "Practice Form")
        self.fill_required_fields()
        self.page.fill_first_name("")
        self.check_submission_rejected("не указано имя")

    def test_missing_last_name(self):
        self.assertEqual(self.page.open_form(), "Practice Form")
        self.fill_required_fields()
        self.page.fill_last_name("")
        self.check_submission_rejected("не указана фамилия")

    def test_missing_gender(self):
        self.assertEqual(self.page.open_form(), "Practice Form")
        self.page.fill_first_name("Пётр")
        self.page.fill_last_name("Калатушкин")
        self.page.fill_mobile("9991234567")
        self.check_submission_rejected("не выбран пол")

    def test_missing_mobile(self):
        self.assertEqual(self.page.open_form(), "Practice Form")
        self.fill_required_fields()
        self.page.fill_mobile("")
        self.check_submission_rejected("не указан телефон")

    def test_short_mobile(self):
        self.assertEqual(self.page.open_form(), "Practice Form")
        self.fill_required_fields()
        self.page.fill_mobile("123456789")
        self.check_submission_rejected("телефон содержит 9 цифр вместо 10")

    def test_mobile_with_letters(self):
        self.assertEqual(self.page.open_form(), "Practice Form")
        self.fill_required_fields()
        self.page.fill_mobile("999abc4567")
        self.check_submission_rejected("телефон содержит буквы")

    def test_whitespace_first_name(self):
        self.assertEqual(self.page.open_form(), "Practice Form")
        self.fill_required_fields()
        self.page.fill_first_name("   ")
        self.check_submission_rejected("имя состоит только из пробелов")


if __name__ == "__main__":
    unittest.main(verbosity=2)
