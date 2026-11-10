import unittest
from selenium import webdriver
from pages.login_page import LoginPage

VALID_LOGIN = "user1"
VALID_PASSWORD = "password1"
WRONG_CREDENTIALS = "Wrong login or password"
PAUSE = 0

class TestLogin(unittest.TestCase):

    def setUp(self):
        print(f"\nСТАРТ: {self._testMethodName}", flush=True)
        self.driver = webdriver.Chrome()
        # Cleanup закроет браузер даже при ошибке в дальнейшей подготовке.
        self.addCleanup(self.driver.quit)
        self.driver.maximize_window()
        self.page = LoginPage(self.driver, pause=PAUSE)

    def check_successful_login(self):
        self.assertEqual(self.page.get_welcome_message(), f"Welcome, {VALID_LOGIN}!")
        self.assertFalse(self.page.is_form_visible())
        self.assertTrue(self.page.is_logout_visible())

    def check_invalid_login(self, login, password, expected_error, scenario):
        self.page.open()
        self.page.login(login, password)
        self.assertEqual(self.page.get_error_message(), expected_error, scenario)
        self.assertTrue(self.page.is_form_visible())
        self.assertFalse(self.page.is_success_visible())
        print(f"OK: {scenario}", flush=True)

    def test_valid_login(self):
        self.page.open()
        self.page.login(VALID_LOGIN, VALID_PASSWORD)
        self.check_successful_login()
        print("OK: успешный вход", flush=True)

    def test_wrong_login(self):
        self.check_invalid_login("user2", VALID_PASSWORD,
                            WRONG_CREDENTIALS, "неверный логин")

    def test_wrong_password(self):
        self.check_invalid_login(VALID_LOGIN, "password2",
                            WRONG_CREDENTIALS, "неверный пароль")

    def test_empty_fields(self):
        self.check_invalid_login(
            "", "",
            "Login and password are required (minimum 3 and 6 characters)",
            "пустые поля",
        )

    def test_empty_login(self):
        self.check_invalid_login("", VALID_PASSWORD,
                            "Login is required (minimum 3 characters)", "пустой логин")

    def test_empty_password(self):
        self.check_invalid_login(VALID_LOGIN, "",
                            "Password is required (minimum 6 characters)", "пустой пароль")

    def test_short_login(self):
        self.check_invalid_login("ab", VALID_PASSWORD,
                            "Login must be at least 3 characters", "короткий логин")

    def test_short_password(self):
        self.check_invalid_login(VALID_LOGIN, "12345",
                            "Password must be at least 6 characters", "короткий пароль")

    def test_logout(self):
        self.page.open()
        self.page.login(VALID_LOGIN, VALID_PASSWORD)
        self.check_successful_login()
        self.page.logout()
        self.assertFalse(self.page.is_success_visible())
        self.assertEqual(self.page.get_login_value(), "")
        self.assertEqual(self.page.get_password_value(), "")
        self.page.refresh()
        self.assertTrue(self.page.is_form_visible())
        self.assertFalse(self.page.is_success_visible())
        print("OK: выход и сохранение выхода после обновления", flush=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
