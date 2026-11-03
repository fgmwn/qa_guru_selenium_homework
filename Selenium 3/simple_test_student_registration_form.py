import time
import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# python -m unittest simple_test_student_registration_form.py

class TestAutomationForm(unittest.TestCase):

    def setUp(self):
        # Инициализация WebDriver (в данном примере Chrome)
        #options = webdriver.ChromeOptions()
        #options.add_argument("--window-size=1920,1080")
        # Раскомментируйте строку ниже, если хотите запустить в фоновом режиме:
        # options.add_argument("--headless")        
        #self.driver = webdriver.Chrome(options=options)

        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 5)  # Явное ожидание до 5 секунд
        self.url = "https://qa-guru.github.io/one-page-form/automation-practice-form.html"

    def test_fill_entire_form(self):
        driver = self.driver
        wait = self.wait
        driver.get(self.url)

        # 0. Ожидаем загрузки страницы (проверяем видимость главного заголовка формы)
        
        form_title = self.wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/main/section/h1")))
        self.assertEqual(form_title.text, "Practice Form")

        time.sleep(5)

        form_sub_title = self.wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/main/section/div/p")))
        self.assertEqual(form_sub_title.text, "Student Registration Form")

        # 1. Убираем окно "Level up your automation" которое как минимум будет закрывать часть web element-ов и мешать с ними работать!
        # Ожидаем появление заголовка в модальном окне
        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Level up your automation')]")))
        # Находим и кликаем по кнопке закрытия (крестику) модального окна
        close_banner_btn = wait.until(EC.element_to_be_clickable((By.XPATH, """//*[@id="fixedban"]/div/div/button""")))
        close_banner_btn.click()
    
        # Ожидаем, пока баннер полностью исчезнет, чтобы он не перекрывал элементы формы
        wait.until(EC.invisibility_of_element(close_banner_btn))

        # 2. Текстовые поля: Имя и Фамилия
        first_name = self.wait.until(EC.element_to_be_clickable((By.ID, "firstName")))
        first_name.send_keys("Иван")
        
        last_name = driver.find_element(By.ID, "lastName")
        last_name.send_keys("Петров")

        # 3. Текстовое поле: Email
        email = driver.find_element(By.ID, "userEmail")
        email.send_keys("ivan.petrov@example.com")

        # 4. Радиокнопки (Gender): кликаем по связанному тегу <label>, так как сам <input> скрыт
        gender_male_label = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='gender-radio-1']")))
        gender_male_label.click()

        # 5. Текстовое поле: Номер телефона (Mobile)
        mobile_number = driver.find_element(By.ID, "userNumber")
        mobile_number.send_keys("9991234567")

        # 6. Виджет календаря (Date of Birth)
        date_input = driver.find_element(By.ID, "dateOfBirthInput")
        date_input.click()

        # Ожидаем появление всплывающего окна календаря
        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "react-datepicker__month-container")))

        # Выбираем месяц (декабрь) через выпадающий список внутри календаря
        month_select = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "react-datepicker__month-select")))
        month_select.click()
        month_select.find_element(By.XPATH, "//option[@value='11']").click()  # 11 — это Декабрь

        # Выбираем год (1995)
        year_select = driver.find_element(By.CLASS_NAME, "react-datepicker__year-select")
        year_select.click()
        year_select.find_element(By.XPATH, "//option[@value='1995']").click()

        # Выбираем конкретный день месяца (например, 25-е число)
        # Используем специальный класс react-datepicker__day--025, исключая дни соседних месяцев (outside-month)
        day_element = driver.find_element(By.CSS_SELECTOR, ".react-datepicker__day--025:not(.react-datepicker__day--outside-month)")
        day_element.click()

        # 7. Поле автодополнения (Subjects)
        subjects_input = self.wait.until(EC.element_to_be_clickable((By.ID, "subjectsInput")))
        subjects_input.send_keys("Computer Science")
        subjects_input.send_keys(Keys.ENTER)

        # 8. Чекбоксы (Hobbies): кликаем по связанному <label>
        hobby_sports = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='hobbies-checkbox-1']"))
        )
        hobby_sports.click()
        
        hobby_music = driver.find_element(By.CSS_SELECTOR, "label[for='hobbies-checkbox-3']")
        hobby_music.click()

        # 9. Загрузка файла (Picture)
        # Создаем временный файл для теста, чтобы код оставался переносимым
        temp_file_path = os.path.abspath("test_image.jpg")
        with open(temp_file_path, "w") as f:
            f.write("fake image data")

        upload_input = driver.find_element(By.ID, "uploadPicture")
        upload_input.send_keys(temp_file_path)

        # 10. Текстовая область: Текущий адрес (Current Address)
        current_address = driver.find_element(By.ID, "currentAddress")
        current_address.send_keys("123456, г. Москва, ул. Ленина, д. 1")

        # Избавляемся от футеров или рекламы, которые могут перекрывать кастомные дропдауны, делаем скрол (главное, демонстрация execute_script)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.execute_script("document.getElementsByTagName('footer')[0].style.display='none';")
        #driver.execute_script("document.getElementById('fixedban').style.display='none';")

        # 11. Выпадающий список (Dropdown): Выбор Штата (State)
        state_dropdown = self.wait.until(EC.element_to_be_clickable((By.ID, "state")))
        state_dropdown.click()
        # Ждем появления опции во всплывающем меню дропдауна React-Select и кликаем
        state_option = self.wait.until(EC.element_to_be_clickable((By.XPATH, """//*[@id="stateCity-wrapper"]/div[1]""")))
        state_option.click()
        

        # 12. Выпадающий список (Dropdown): Выбор Города (City)
        city_dropdown = self.wait.until(EC.element_to_be_clickable((By.ID, "city")))
        city_dropdown.click()
        city_option = self.wait.until(EC.element_to_be_clickable((By.XPATH, """//*[@id="stateCity-wrapper"]/div[1]""")))
        city_option.click()

        # 13. Отправка формы (Submit)
        submit_button = driver.find_element(By.ID, "submit")
        driver.execute_script("arguments[0].click();", submit_button)  # Надежный клик через JS без перекрытий

        # 14. Проверка результатов (Expected Conditions для модального окна)
        # Проверяем, что появилось финальное окно с подтверждением
        modal_title = self.wait.until(
            EC.visibility_of_element_located((By.ID, "example-modal-sizes-title-lg"))
        )
        self.assertEqual(modal_title.text, "Thanks for submitting the form")

        time.sleep(5)

        # Проверяем наличие валидных данных в таблице результатов
        result_table = driver.find_element(By.CLASS_NAME, "table-responsive")
        self.assertIn("Иван Петров", result_table.text)
        self.assertIn("ivan.petrov@example.com", result_table.text)
        self.assertIn("Male", result_table.text)
        self.assertIn("9991234567", result_table.text)
        self.assertIn("25 Dec 1995", result_table.text) # форма вывода даты может меняться от настроек
        self.assertIn("Computer Science", result_table.text)
        self.assertIn("Sports, Music", result_table.text)
        self.assertIn("test_image.jpg", result_table.text)
        self.assertIn("123456, г. Москва, ул. Ленина, д. 1", result_table.text)
        self.assertIn("NCR Delhi", result_table.text)

    def tearDown(self):
        # Удаляем созданный временный файл, если он существует
        if os.path.exists("test_image.jpg"):
            os.remove("test_image.jpg")
        # Закрываем браузер
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()