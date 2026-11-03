from random import randint
from tests.conftest import temp_test_file


def test_positive_required_fields(registration_page):
    first_name = "Avtomat"
    last_name = "Avtomatov"
    number = str(randint(9000000000, 9999999999))
    gender = "Male"

    registration_page.open_mine_url()
    registration_page.close_banner()
    registration_page.input_first_name(first_name)
    registration_page.input_last_name(last_name)
    registration_page.input_mobile_number(number)
    registration_page.select_gender(gender)
    registration_page.scroll_to_footer()
    registration_page.click_submit_button()
    registration_page.get_result_form()

    result_text = registration_page.get_result_form()

    assert first_name in result_text, f"Имя '{first_name}' не найдено!"
    assert last_name in result_text, f"Фамилия '{last_name}' не найдена!"
    assert str(number) in result_text, f"Номер '{number}' не найден!"
    assert gender in result_text, f"Пол '{gender}' не найден!"


def test_positive_all_fields(registration_page, temp_test_file):
    file_path, file_name = temp_test_file

    first_name = "Avtomat"
    last_name = "Avtomatov"
    email = "avtomat@guru.com"
    number = str(randint(9000000000, 9999999999))
    gender = "Female"
    day, month, year = 1, 2, 1990
    subjects_list = ["Maths", "Physics", "Chemistry"]
    hobbies_list = ["Sports", "Reading"]
    current_address = "Vremenniy address"
    state_name = "Uttar Pradesh"
    city_name = "Lucknow"

    registration_page.open_mine_url()
    registration_page.close_banner()
    registration_page.input_first_name(first_name)
    registration_page.input_last_name(last_name)
    registration_page.input_email(email)
    registration_page.input_mobile_number(number)
    registration_page.select_gender(gender)
    registration_page.scroll_to_footer()
    registration_page.select_date_of_birth(day, month, year)
    expected_subjects = registration_page.input_subjects(subjects_list)
    expected_hobbies = registration_page.select_hobbies(hobbies_list)
    registration_page.upload_picture(file_path)
    registration_page.input_current_address(current_address)
    registration_page.select_state(state_name)
    registration_page.select_city(city_name)
    registration_page.click_submit_button()
    registration_page.get_result_form()

    result_text = registration_page.get_result_form()
    expected_date = registration_page.get_expected_birth_date_text(day, month, year)

    assert first_name in result_text, f"Имя '{first_name}' не найдено!"
    assert last_name in result_text, f"Фимилия '{last_name}' не найдена!"
    assert email in result_text, f"Почта '{email}' не найдена!"
    assert number in result_text, f"Номер '{number}' не найден!"
    assert gender in result_text, f"Пол '{gender}' не найден!"
    assert expected_date in result_text, f"Дата рождения '{expected_date}' не найдена!"
    assert expected_subjects in result_text, f"Предметы '{expected_subjects}' не найдены!"
    assert expected_hobbies in result_text, f"Хобби '{expected_hobbies}' не найдены!"
    assert file_name in result_text, f"Файл '{file_name}' не найден!"
    assert current_address in result_text, f"Адрес '{current_address}' не найден!"
    assert state_name in result_text, f"Штат '{state_name}' не найден!"
    assert city_name in result_text, f"Город '{city_name}' не найден!"


def test_negative_empty_first_name(registration_page):
    first_name = ""
    last_name = "Avtomatov"
    number = randint(9000000000, 9999999999)
    gender = "Male"
    error_message = "Please fill required fields and enter a valid 10-digit mobile number."

    registration_page.open_mine_url()
    registration_page.close_banner()
    registration_page.input_first_name(first_name)
    registration_page.input_last_name(last_name)
    registration_page.input_mobile_number(number)
    registration_page.select_gender(gender)
    registration_page.scroll_to_footer()
    registration_page.click_submit_button()
    actual_error = registration_page.get_error_message()

    assert error_message in actual_error


def test_negative_empty_last_name(registration_page):
    first_name = "Ю"
    last_name = ""
    number = str(randint(9000000000, 9999999999))
    gender = "Male"
    error_message = "Please fill required fields and enter a valid 10-digit mobile number."

    registration_page.open_mine_url()
    registration_page.close_banner()
    registration_page.input_first_name(first_name)
    registration_page.input_last_name(last_name)
    registration_page.input_mobile_number(number)
    registration_page.select_gender(gender)
    registration_page.scroll_to_footer()
    registration_page.click_submit_button()
    actual_error = registration_page.get_error_message()

    assert error_message in actual_error


def test_negative_empty_gender(registration_page):
    first_name = "Ю"
    last_name = "Буква"
    number = str(randint(9000000000, 9999999999))
    error_message = "Please fill required fields and enter a valid 10-digit mobile number."

    registration_page.open_mine_url()
    registration_page.close_banner()
    registration_page.input_first_name(first_name)
    registration_page.input_last_name(last_name)
    registration_page.input_mobile_number(number)
    registration_page.scroll_to_footer()
    registration_page.click_submit_button()
    actual_error = registration_page.get_error_message()

    assert error_message in actual_error


def test_negative_empty_number(registration_page):
    first_name = "Ю"
    last_name = "Я"
    gender = "Male"
    error_message = "Please fill required fields and enter a valid 10-digit mobile number."

    registration_page.open_mine_url()
    registration_page.close_banner()
    registration_page.input_first_name(first_name)
    registration_page.input_last_name(last_name)
    registration_page.select_gender(gender)
    registration_page.scroll_to_footer()
    registration_page.click_submit_button()
    actual_error = registration_page.get_error_message()

    assert error_message in actual_error
