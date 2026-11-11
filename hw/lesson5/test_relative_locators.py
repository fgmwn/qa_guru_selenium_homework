import unittest
from selenium import webdriver
from relative_locators_page import RelativeLocatorsPage

PAUSE = 1


class TestRelativeLocators(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.addCleanup(self.driver.quit)
        # Геометрия влияет на поиск: задаём воспроизводимый размер окна.
        self.driver.set_window_size(1400, 1000)
        self.page = RelativeLocatorsPage(self.driver, pause=PAUSE)

    def test_below(self):
        self.page.open_text_box()
        actual = self.page.fill_email_below_name('ivan@example.com')
        self.assertEqual(actual, ('userEmail', 'ivan@example.com'))
        print('OK: below нашёл поле email', flush=True)

    def test_above(self):
        self.page.open_text_box()
        actual = self.page.fill_name_above_email('Иван Иванов')
        self.assertEqual(actual, ('userName', 'Иван Иванов'))
        print('OK: above нашёл поле имени', flush=True)

    def test_left_of(self):
        self.page.open_registration()
        self.assertEqual(self.page.select_gender_left_of_female(), ('Male', True))
        print('OK: слева от Female выбран Male', flush=True)

    def test_right_of(self):
        self.page.open_registration()
        self.assertEqual(self.page.select_gender_right_of_male(), ('Female', True))
        print('OK: справа от Male выбран Female', flush=True)

    def test_near(self):
        self.page.open_text_box()
        actual = self.page.fill_address_near_label('Минск, ул. Академическая')
        self.assertEqual(actual, ('currentAddress', 'Минск, ул. Академическая'))
        print('OK: near нашёл текущий адрес', flush=True)


if __name__ == '__main__':
    unittest.main(verbosity=2)
