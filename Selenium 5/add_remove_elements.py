import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# 1. Инициализация драйвера (открывается браузер Chrome)
driver = webdriver.Chrome()

try:
    # 2. Переход на целевую страницу
    url = "https://the-internet.herokuapp.com/add_remove_elements/"
    driver.get(url)
    print("Страница успешно открыта.")
    time.sleep(2)  # Пауза для визуального контроля

    # 3. Поиск главной кнопки "Add Element"
    # Используем поиск по тексту кнопки через XPath
    add_button = driver.find_element(By.XPATH, "//button[text()='Add Element']")

    # 4. Демонстрация добавления элементов
    print("Добавляем 3 элемента...")
    for i in range(3):
        add_button.click()
        time.sleep(0.5)  # Короткая пауза, чтобы заметили появление кнопок

    # 5. Подсчет и проверка созданных элементов
    # Ищем все появившиеся кнопки удаления по их классу
    delete_buttons = driver.find_elements(By.CLASS_NAME, "added-manually")
    print(f"Количество созданных кнопок 'Delete': {len(delete_buttons)}")

    # 6. Демонстрация удаления элементов
    print("Удаляем созданные элементы по очереди...")
    for button in delete_buttons:
        button.click()
        print("Элемент удален.")
        time.sleep(0.5)  # Пауза для наглядности удаления

    # Повторная проверка количества элементов после удаления
    remaining_buttons = driver.find_elements(By.CLASS_NAME, "added-manually")
    print(f"Осталось кнопок на странице: {len(remaining_buttons)}")
    time.sleep(2)

finally:
    # 7. Закрытие браузера и завершение сессии
    driver.quit()
    print("Браузер закрыт. Тест завершен.")