import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# TODO: 4) Переписать используя PageFactory (Lesson 5)

# TODO: 2) Добавить работу с таблицей 2
# TODO: 3) Добавить TC в которых идет работа сразу с 2-я таблицами

# 1. Реализация Page Element для таблицы
class TableElement:
    def __init__(self, driver, locator):
        self.driver = driver
        self.locator = locator

    @property
    def element(self):
        return self.driver.find_element(*self.locator)

    def get_headers(self) -> list[str]:
        """Возвращает список заголовков таблицы."""
        header_elements = self.element.find_elements(By.CSS_SELECTOR, "thead th")
        return [header.text for header in header_elements]

    def get_row_data(self, row_index: int) -> list[str]:
        """Возвращает данные конкретной строки по её индексу (начиная с 0)."""
        rows = self.element.find_elements(By.CSS_SELECTOR, "tbody tr")
        cells = rows[row_index].find_elements(By.TAG_NAME, "td")
        return [cell.text for cell in cells]

    def get_cell_value(self, row_index: int, column_index: int) -> str:
        """Возвращает значение конкретной ячейки."""
        rows = self.element.find_elements(By.CSS_SELECTOR, "tbody tr")
        cells = rows[row_index].find_elements(By.TAG_NAME, "td")
        # TODDO: 1) как переписать используя вызов get_row_data ?
        return cells[column_index].text


# 2. Пример использования (Скрипт теста)
if __name__ == "__main__":
    # Инициализация драйвера
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(5)

    try:
        # Открытие страницы
        driver.get("https://the-internet.herokuapp.com/tables")

        # Инициализация таблицы как Page Element через её локатор
        table1_locator = (By.ID, "table1")
        table = TableElement(driver, table1_locator)

        # Сбор данных для демонстрации
        headers = table.get_headers()
        first_row = table.get_row_data(0)
        specific_cell = table.get_cell_value(row_index=2, column_index=3)  # Строка 3, Колонка 4 (Due)

        # Вывод результатов в консоль
        print("Заголовки таблицы:", headers)
        print("Первая строка данных:", first_row)
        print(f"Значение в строке 3, колонке 'Due': {specific_cell}")

        # Простые проверки (Assertions)
        assert "Last Name" in headers, "Заголовок 'Last Name' не найден"
        assert "Smith" in first_row, "Фамилия 'Smith' должна быть в первой строке"
        assert specific_cell == "$100.00", f"Ожидалось $100.00, но получено {specific_cell}"
        
        print("\n✅ Тест успешно пройден!")
        time.sleep(5)

    finally:
        driver.quit()


