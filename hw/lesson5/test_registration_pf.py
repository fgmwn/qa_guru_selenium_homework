import base64
import tempfile
from pathlib import Path
import pytest
from selenium import webdriver
from registration_page_pf import RegistrationPagePF

PAUSE = 1


@pytest.mark.parametrize('data, expected_date', [
    (dict(first_name='Ivan', last_name='Ivanov', email='ivanov@university.edu', gender='Male',
          user_number='1234567890', birth_day=(2000, 1, 15), subjects=['Maths', 'Computer Science'],
          hobbies=['Sports', 'Music'], current_address='123 University Avenue, Tomsk, Russia',
          state='NCR', city='Delhi'), '15 Jan 2000'),
    (dict(first_name='Анна', last_name='Петрова', email='anna@example.com', gender='Female',
          user_number='9991234567', birth_day=(1995, 12, 1), subjects=['Physics'],
          hobbies=['Reading'], current_address='Москва, Пушкина, 10',
          state='Haryana', city='Panipat'), '01 Dec 1995'),
    (dict(first_name='Alex', last_name='Smith', email='alex@example.com', gender='Other',
          user_number='9876543210', birth_day=(2024, 2, 29), subjects=['English', 'History'],
          hobbies=['Music'], current_address='Jaipur, 20', state='Rajasthan', city='Jaipur'), '29 Feb 2024'),
], ids=['full_form', 'different_data', 'leap_day'])
def test_full_registration_pf(data, expected_date):
    # Параметризация не требует фикстуры driver: создаём браузер явно.
    driver = webdriver.Chrome()
    try:
        driver.maximize_window()
        with tempfile.TemporaryDirectory() as directory:
            picture = Path(directory) / 'student.png'
            picture.write_bytes(base64.b64decode(
                'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aKZkAAAAASUVORK5CYII='))
            page = RegistrationPagePF(driver, pause=PAUSE)
            assert page.open_form() == 'Practice Form'
            actual = page.fill_form(file_name=picture, **data).get_modal_results()
            expected = {
                'Student Name': f"{data['first_name']} {data['last_name']}",
                'Student Email': data['email'], 'Gender': data['gender'],
                'Mobile': data['user_number'], 'Date of Birth': expected_date,
                'Subjects': ', '.join(data['subjects']), 'Hobbies': ', '.join(data['hobbies']),
                'Picture': picture.name, 'Address': data['current_address'],
                'State and City': f"{data['state']} {data['city']}",
            }
            assert actual == expected
            print('OK: PF — все 10 строк результата совпадают', flush=True)
            page.close_result()
            assert not page.is_result_visible()
    finally:
        driver.quit()
