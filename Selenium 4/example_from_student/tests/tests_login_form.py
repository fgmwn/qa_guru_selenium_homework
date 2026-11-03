def test_positive_login(login_page):
    login_page.open_mine_url()
    login_page.input_login("Avtomat@mai")
    login_page.input_password("Avtomat1!")
    login_page.click_login_button()


def test_empty_login(login_page):
    login_page.open_mine_url()
    login_page.input_login("")
    login_page.input_password("1qaz@WSX")
    login_page.click_login_button()

    assert login_page.get_error_message("Login is required (minimum 3 characters)")


def test_empty_password(login_page):
    login_page.open_mine_url()
    login_page.input_login("!QAZ2wsx")
    login_page.input_password("")
    login_page.click_login_button()

    assert login_page.get_error_message("Password is required (minimum 6 characters)")


def test_empty_fields(login_page):
    login_page.open_mine_url()
    login_page.input_login("")
    login_page.input_password("")
    login_page.click_login_button()

    assert login_page.get_error_message("Login and password are required (minimum 3 and 6 characters)")


def test_incorrect_data(login_page):
    login_page.open_mine_url()
    login_page.input_login("Avtomat@mai")
    login_page.input_password("123456")
    login_page.click_login_button()

    assert login_page.get_error_message("Wrong login or password")


def test_short_password(login_page):
    login_page.open_mine_url()
    login_page.input_login("Avtomat@mail.ru")
    login_page.input_password("12345")
    login_page.click_login_button()

    assert login_page.get_error_message("Password must be at least 6 characters")


def test_short_login(login_page):
    login_page.open_mine_url()
    login_page.input_login("Av")
    login_page.input_password("123456")
    login_page.click_login_button()

    assert login_page.get_error_message("Login must be at least 3 characters")
