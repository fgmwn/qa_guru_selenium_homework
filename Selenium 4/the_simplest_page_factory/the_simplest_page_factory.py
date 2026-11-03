import time
from selenium import webdriver
from seleniumpagefactory.Pagefactory import PageFactory
# pip install selenium-page-factory selenium

# TODO: Это лишь абстрактный пример, переписать хотя бы один тест с хотя бы одним PageObject на PageFactory
# TODO: Постараться использовать в своем проекте расширенные возможности PageFactory (примеры описаны в методе login)

# 1. Описываем класс страницы, наследуясь от PageFactory
class LoginPage(PageFactory):
    def __init__(self, driver):
        self.driver = driver
        # Локаторы задаются в виде словаря. Ключ станет именем переменной-элемента.
        self.locators = {
            "username_input": ('ID', 'username'),
            "password_input": ('XPATH', '//input[@id="password"]'),
            "submit_button": ('CSS', 'button[type="submit"]'),
            "dropdown_role": ('NAME', 'role'),
            "hover_menu": ('ID', 'menu-item')
        }

    # Метод, использующий возможности Page Factory
    def login(self, user, password):
        # Элементы инициализируются «на лету» и имеют расширенные методы
        self.username_input.set_text(user)  # Ввод текста + очистка
        self.password_input.set_text(password)
        
        # Пример работы с выпадающим списком (Select)
        self.dropdown_role.select_element_by_text("Администратор")
        
        # Пример действия hover (наведение) с последующим кликом
        self.hover_menu.hover()
        
        # set_text / click_button включают встроенное ожидание появления элемента
        self.submit_button.click_button() 

# 2. Основной скрипт теста
if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.get("https://example.com")
    
    # Инициализация страницы
    login_page = LoginPage(driver)
    
    # Вызов логики
    login_page.login("admin_user", "SuperSecretPassword123")
    
    time.sleep(5)
    driver.quit()