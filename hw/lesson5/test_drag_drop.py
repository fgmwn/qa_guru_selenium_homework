import unittest
from selenium import webdriver
from drag_drop_page import DragDropPage

PAUSE = 1


class TestDragDrop(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.addCleanup(self.driver.quit)
        self.driver.maximize_window()
        self.page = DragDropPage(self.driver, pause=PAUSE).open()

    def check_labels(self, left, right):
        self.page.wait_for_labels(left, right)
        self.assertEqual(self.page.get_labels(), (left, right))
        print(f'OK: слева {left}, справа {right}', flush=True)

    def test_initial_order(self):
        self.check_labels('A', 'B')

    def test_drag_left_to_right(self):
        self.check_labels('A', 'B')
        self.page.drag_left_to_right()
        self.check_labels('B', 'A')

    def test_drag_right_to_left(self):
        self.check_labels('A', 'B')
        self.page.drag_right_to_left()
        self.check_labels('B', 'A')

    def test_swap_and_return(self):
        self.page.drag_left_to_right()
        self.check_labels('B', 'A')
        self.page.drag_right_to_left()
        self.check_labels('A', 'B')


if __name__ == '__main__':
    unittest.main(verbosity=2)
