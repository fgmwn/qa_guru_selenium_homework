import unittest
from selenium import webdriver
from add_remove_page import AddRemovePage

PAUSE = 1  # Для наблюдения.


class TestAddRemove(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.addCleanup(self.driver.quit)
        self.driver.maximize_window()
        self.page = AddRemovePage(self.driver, pause=PAUSE).open()

    def check_count(self, expected):
        self.page.wait_for_count(expected)
        self.assertEqual(self.page.get_count(), expected)
        print(f'OK: количество Delete = {expected}', flush=True)

    def test_initial_page_is_empty(self):
        self.check_count(0)

    def test_add_three_and_delete_all(self):
        self.check_count(0)
        for expected in (1, 2, 3):
            self.page.add_element()
            self.check_count(expected)
        for expected in (2, 1, 0):
            self.page.delete_first()
            self.check_count(expected)

    def test_delete_only_one(self):
        self.page.add_element().add_element().add_element()
        self.check_count(3)
        self.page.delete_first()
        self.check_count(2)

    def test_add_again_after_deletion(self):
        self.page.add_element().wait_for_count(1).delete_first()
        self.check_count(0)
        self.page.add_element()
        self.check_count(1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
