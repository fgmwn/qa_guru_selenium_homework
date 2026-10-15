import time
from selenium import webdriver
from selenium.webdriver.common.by import By

class TestSuite:
    # Метод-конструктор: вызывается при создании нового объекта
    def __init__(self, url, driver):
        # Note: pytest не работает с TestSuit-ами в которых есть конструктор!
        self.__url = url
        self.__driver = driver

    # Метод для получения URL - значения скрытого атрибута (геттер)
    def get_url(self):
        return self.__url

    # Метод для получения Driver - значения скрытого атрибута (геттер) 
    def get_driver(self):
        return self.__driver

    # Обычный метод класса - тестовый метод
    def test_case01(self):
        try:
            # 2. Открытие страницы
            self.get_driver().get(self.get_url())
            self.get_driver().maximize_window()
            time.sleep(5)  # Пауза, чтобы визуально заметить открытие

            # 3. Поиск элементов и заполнение полей
            # Находим поле Full Name по его ID и вводим текст
            full_name_field = self.get_driver().find_element(By.ID, "userName")
            full_name_field.send_keys("Иван Иванов")

            # Находим поле Email по его ID и вводим текст
            email_field = self.get_driver().find_element(By.ID, "userEmail")
            email_field.send_keys("ivan@example.com")

            # Находим кнопку Submit по ее ID и кликаем
            submit_button = self.get_driver().find_element(By.ID, "submit")
            submit_button.click()

            # 4. Проверка результата
            time.sleep(5)  # Пауза, чтобы увидеть результат отправки
            
            # Находим блок с отправленными данными
            result_box = self.get_driver().find_element(By.ID, "output")
            
            # Проверяем, что в блоке результата появился введенный текст
            assert "Иван Иванов" in result_box.text
            print("Тест 01 успешно пройден!")

        finally:
            # 5. Закрытие браузера в любом случае
            print("Очищаем driver между тестами для чистоты эксперимента.")
            #self.get_driver().close()
            #self.get_driver().quit()
            

    # Обычный метод класса - тестовый метод
    def test_case02(self):
        try:
            # 2. Открытие страницы
            self.get_driver().get(self.get_url())
            self.get_driver().maximize_window()
            time.sleep(5)  # Пауза, чтобы визуально заметить открытие

            # 3. Поиск элементов и заполнение полей
            # Находим поле Full Name по его ID и вводим текст
            full_name_field = self.get_driver().find_element(By.ID, "userName")
            full_name_field.send_keys("Иван Иванов")

            # Находим поле Email по его ID и вводим текст
            email_field = self.get_driver().find_element(By.ID, "userEmail")
            email_field.send_keys("ivan@example.com")

            # Находим поле Permanent Adress по его ID и вводим текст
            permanent_address_field = self.get_driver().find_element(By.ID, "permanentAddress")
            permanent_address_field.send_keys("Ленинград, 3-я улица Строителей, 25")

            # Находим кнопку Submit по ее ID и кликаем
            submit_button = self.get_driver().find_element(By.ID, "submit")
            submit_button.click()

            # 4. Проверка результата
            time.sleep(5)  # Пауза, чтобы увидеть результат отправки
            
            # Находим блок с отправленными данными
            result_box = self.get_driver().find_element(By.ID, "output")
            
            # Проверяем, что в блоке результата появился введенный текст
            assert "Иван Иванов" in result_box.text
            print("Тест 02 успешно пройден!")

            #self.get_driver().navigate().to("https://example.com") # нет в новых версиях

            #self.get_driver().back()      # вернуться на предыдущую страницу
            #self.get_driver().forward()   # пойти вперед по истории
            #self.get_driver().refresh()   # перезагрузить текущую страницу
            #self.get_driver().navigate().to("https://www.google.com/") # нет в новых версиях

        finally:
            # 5. Закрытие браузера в любом случае
            print("Очищаем driver между тестами для чистоты эксперимента.")
            #self.get_driver().close()
            #self.get_driver().quit()

    
# 1. Запуск браузера Chrome
url = "https://qa-guru.github.io/one-page-form/text-box.html"
driver = webdriver.Chrome()

test_suite = TestSuite(url, driver)
test_suite.test_case01()
test_suite.test_case02()

