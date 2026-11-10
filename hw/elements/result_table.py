from selenium.webdriver.common.by import By


class ResultTable:
    def __init__(self, driver):
        self._driver = driver

    _ROWS = (By.CSS_SELECTOR, "#resultBody tr")

    def get_rows(self):
        rows = self._driver.find_elements(*self._ROWS)
        return [
            [cell.text for cell in row.find_elements(By.TAG_NAME, "td")]
            for row in rows
        ]
