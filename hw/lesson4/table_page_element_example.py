import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumpagefactory.Pagefactory import PageFactory


class TableElement:
    def __init__(self, driver, locator):
        self.driver = driver
        self.locator = locator

    @property
    def element(self):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.locator))

    def get_headers(self):
        return [cell.text for cell in self.element.find_elements(By.CSS_SELECTOR, 'thead th')]

    def get_rows(self):
        return [[cell.text for cell in row.find_elements(By.TAG_NAME, 'td')]
                for row in self.element.find_elements(By.CSS_SELECTOR, 'tbody tr')]

    def get_row_data(self, row_index):
        return self.get_rows()[row_index]

    def get_cell_value(self, row_index, column_index):
        return self.get_row_data(row_index)[column_index]


class TableElementPF(TableElement, PageFactory):
    def __init__(self, driver, locator):
        super().__init__(driver, locator)
        self.locators = {'table_root': ('ID', locator[1])}

    @property
    def element(self):
        return self.table_root


class TestTables(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.addCleanup(self.driver.quit)
        self.driver.get('https://the-internet.herokuapp.com/tables')
        self.table1 = TableElement(self.driver, (By.ID, 'table1'))
        self.table2 = TableElement(self.driver, (By.ID, 'table2'))

    def test_first_table(self):
        self.assertIn('Last Name', self.table1.get_headers())
        self.assertEqual(self.table1.get_cell_value(0, 0), 'Smith')
        self.assertEqual(self.table1.get_cell_value(2, 3), '$100.00')

    def test_second_table(self):
        self.assertIn('Last Name', self.table2.get_headers())
        self.assertEqual(self.table2.get_cell_value(0, 0), 'Smith')
        self.assertEqual(self.table2.get_cell_value(2, 3), '$100.00')

    def test_both_tables_have_same_data(self):
        self.assertEqual(self.table1.get_headers(), self.table2.get_headers())
        self.assertEqual(len(self.table1.get_rows()), 4)
        self.assertEqual(self.table1.get_rows(), self.table2.get_rows())

    def test_page_factory_reads_both_tables(self):
        pf1 = TableElementPF(self.driver, (By.ID, 'table1'))
        pf2 = TableElementPF(self.driver, (By.ID, 'table2'))
        self.assertEqual(pf1.get_headers(), self.table1.get_headers())
        self.assertEqual(pf1.get_rows(), self.table1.get_rows())
        self.assertEqual(pf2.get_rows(), self.table2.get_rows())


if __name__ == '__main__':
    unittest.main(verbosity=2)
