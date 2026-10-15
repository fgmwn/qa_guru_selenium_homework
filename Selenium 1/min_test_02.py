import time
from selenium import webdriver

# 1. Запуск браузера Chrome
driver = webdriver.Chrome()
# 2. Открытие страницы
driver.get("https://qa-guru.github.io/one-page-form/text-box.html")
driver.maximize_window()
time.sleep(5)  # Пауза, чтобы визуально заметить открытие
print("Тест успешно пройден!")
# 3. Закрытие браузера в любом случае
driver.quit()
