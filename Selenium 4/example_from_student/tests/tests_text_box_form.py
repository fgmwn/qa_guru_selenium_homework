def test_positive_data(text_box_page):
    full_name = "Avtomat Avtomatov"

    text_box_page.open_mine_url()
    text_box_page.input_full_name(full_name)
    text_box_page.click_submit_button()
    text_box_page.scroll_to_data_output()

    assert full_name in text_box_page.get_actual_data()


def test_positive_mail(text_box_page):
    email = "Avtomat@mail.com"

    text_box_page.open_mine_url()
    text_box_page.input_email(email)
    text_box_page.click_submit_button()
    text_box_page.scroll_to_data_output()

    assert email in text_box_page.get_actual_data()


def test_positive_current_address(text_box_page):
    current_address = "Eto vremenniy address, dom 1, kv 2, ulica 3"

    text_box_page.open_mine_url()
    text_box_page.input_current_address(current_address)
    text_box_page.click_submit_button()
    text_box_page.scroll_to_data_output()

    assert current_address in text_box_page.get_actual_data()


def test_positive_permanent_address(text_box_page):
    permanent_address = "A eto address propiski, tut tolko gorod dorog"

    text_box_page.open_mine_url()
    text_box_page.input_permanent_address(permanent_address)
    text_box_page.click_submit_button()
    text_box_page.scroll_to_data_output()

    assert permanent_address in text_box_page.get_actual_data()


def test_email_without_username(text_box_page):
    email = "@mail.com"
    validation_message = 'Введите часть адреса до символа "@"'

    text_box_page.open_mine_url()
    text_box_page.input_email(email)
    text_box_page.click_submit_button()
    text_box_page.scroll_to_data_output()

    assert validation_message in text_box_page.get_email_validation_message()


def test_email_without_at(text_box_page):
    email = "Avtomatmail.com"
    validation_message = 'Адрес электронной почты должен содержать символ "@"'

    text_box_page.open_mine_url()
    text_box_page.input_email(email)
    text_box_page.click_submit_button()
    text_box_page.scroll_to_data_output()

    assert validation_message in text_box_page.get_email_validation_message()


def test_email_without_domain(text_box_page):
    email = "Avtomat@"
    validation_message = 'Введите часть адреса после символа "@"'

    text_box_page.open_mine_url()
    text_box_page.input_email(email)
    text_box_page.click_submit_button()
    text_box_page.scroll_to_data_output()

    assert validation_message in text_box_page.get_email_validation_message()


def test_email_with_a_space(text_box_page):
    email = "Avto mat@mail.com"
    validation_message = 'Часть адреса до символа "@" не должна содержать символ " "'

    text_box_page.open_mine_url()
    text_box_page.input_email(email)
    text_box_page.click_submit_button()
    text_box_page.scroll_to_data_output()

    assert validation_message in text_box_page.get_email_validation_message()
