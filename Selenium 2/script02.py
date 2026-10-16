import time
from selenium import webdriver
#from selenium.webdriver.window_types import WindowTypes # Selenium 3
from selenium.webdriver.common.window import WindowTypes # Selenium 4

# Для Selenium нет разницы между новой вкладкой и новым окном — 
# они оба управляются через уникальные идентификаторы (дескрипторы) window_handles.

driver = webdriver.Chrome()
driver.maximize_window()

try:
    # 1. Открываем исходную страницу
    driver.get("https://qa-guru.github.io/one-page-form/automation-practice-form.html")
    
    # Сохраняем дескриптор ПЕРВОГО (оригинального) окна
    original_window = driver.current_window_handle
    print(f"Идентификатор главной вкладки: {original_window}")
    time.sleep(3)

    # 2. Открываем НОВУЮ ВКЛАДКУ
    print("Открываем новую пустую вкладку...")
    driver.switch_to.new_window(WindowTypes.TAB)
    time.sleep(3)

    # 3. Загружаем сайт на новой вкладке
    print("Открываем Google на новой вкладке...")
    driver.get("https://google.com")
    time.sleep(3)

    # Получаем список всех открытых вкладок
    all_windows = driver.window_handles
    print(f"Все открытые вкладки: {all_windows}")

    # 4. ПЕРЕКЛЮЧЕНИЕ обратно на главную страницу формы
    print("Переключаемся обратно на вкладку с формой...")
    driver.switch_to.window(original_window)
    time.sleep(3)

    # Докажем, что мы вернулись: выведем заголовок страницы
    print(f"Текущий заголовок страницы: {driver.title}")

    # 5. Закрытие конкретной вкладки
    # Переключаемся на вторую вкладку и закрываем её
    for window in all_windows:
        if window != original_window:
            driver.switch_to.window(window)
            print("Закрываем вторую вкладку...")
            time.sleep(3)
            driver.close() # close() закрывает текущую вкладку, но оставляет сессию

    # Возвращаем фокус драйвера на оставшуюся вкладку
    driver.switch_to.window(original_window) # Selenium 4
    time.sleep(3)

finally:
    # Полностью закрываем браузер
    print("Завершаем работу драйвера.")
    driver.quit()


