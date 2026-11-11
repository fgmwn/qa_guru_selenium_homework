import os
import time
import pytest
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
#from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from seleniumpagefactory.Pagefactory import PageFactory

# 1. Создание виртуального окружения
#python -m venv venv

# 1.5 Если не отработал пункт 2 под Windows
# PowerShell: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 2. Активация (Для Windows)
#venv\Scripts\activate
# 2. Активация (Для macOS/Linux)
#source venv/bin/activate

# 3. Установка зависимостей
#pip install -r requirements.txt

#### 1. Специфика реализации PageFactory в экосистеме Python
#В отличие от Java, где локаторы инициализируются через аннотации `@FindBy`, в Python библиотека `selenium-page-factory` реализует динамический дескриптор. 
# Все локаторы описываются в словаре `locators`.
# При обращении к элементу через `self.first_name` библиотека автоматически перехватывает обращение, производит неявный поиск элемента на основе кортежа `('ID', 'firstName')` и возвращает обертку над `WebElement` с расширенными методами (`set_text()`, `click_button()`, `select_element_by_value()`).

#### 2. Работа со сложными кастомными веб-виджетами
#Современные веб-приложения практически не используют стандартные HTML-теги `<select>`. Форма QA Guru построена на базе библиотек экосистемы React (React-Select и React-DatePicker):
#Календарь (DatePicker): Вместо прямой отправки текста в текстовое поле (что часто блокируется или вызывает баги валидации), скрипт имитирует поведение реального пользователя: открывает кликом календарь, взаимодействует с селекторами месяца/года и рассчитывает XPATH для клика по точному дню.
#Кастомные селекты (State / City): Стандартный метод Selenium `.select_by_text()` здесь выбросит исключение. В коде демонстрируется обходной путь: фокус на поле ввода виджета (`state_input`), отправка текста и программная посылка клавиши `Keys.ENTER` для срабатывания триггеров фреймворка React.

#### 3. Безопасное взаимодействие через JavaScript Execution
#При автоматизации реальных интерфейсов элементы часто перекрываются плавающими баннерами, футерами или сторонней рекламой, что вызывает ошибку `ElementClickInterceptedException`. 
#Метод `page.submit_form()` демонстрирует использование инъекции JavaScript: `self.driver.execute_script("arguments[0].click();", self.submit_button)`. Это позволяет инициировать событие отправки формы в обход физических ограничений графического слоя браузера.

#### 4. Парсинг табличных структур (Data Extraction)
#Метод `get_modal_results` обучает конвертировать сырой HTML-код структуры таблицы (`<table> -> <tbody> -> <tr> -> <td>`) в стандартные структуры данных Python (словари `dict`). Это закладывает базу для написания гибких и поддерживаемых ассертов (проверок) без жесткой привязки к индексам элементов.

# ==============================================================================
# 1. КОНФИГУРАЦИЯ ТЕСТОВОЙ СРЕДЫ (pytest fixture)
# ==============================================================================
@pytest.fixture(scope="function")
def driver():
    """Инициализация WebDriver с безопасными флагами для CI/CD и демонстраций."""
    #chrome_options = Options()
    #chrome_options.add_argument("--start-maximized")
    #chrome_options.add_argument("--disable-extensions")
    #chrome_options.add_argument("--headless=new")  # Для фонового запуска студентов
    
    ## Решение проблем с памятью в Docker/стесненных средах обучения
    #chrome_options.add_argument("--no-sandbox")
    #chrome_options.add_argument("--disable-dev-shm-usage")
    
    #driver = webdriver.Chrome(options=chrome_options)

    driver = webdriver.Chrome()
    driver.maximize_window()
    #driver.implicitly_wait = 10
    yield driver
    driver.quit()

# ==============================================================================
# 2. БАЗОВЫЙ КЛАСС СТРАНИЦЫ (Интеграция PageFactory)
# ==============================================================================
class BasePage(PageFactory):
    """Абстрактный класс для расширения возможностей стандартной PageFactory."""
    def __init__(self, driver):
        self.driver = driver
        self.timeout = 10  # Явное ожидание (Explicit Wait) по умолчанию для PageFactory

    def open_url(self, url: str):
        self.driver.get(url)

# ==============================================================================
# 3. КЛАСС СТРАНИЦЫ ФОРМЫ (Реализация паттерна PageFactory)
# ==============================================================================
class AutomationPracticeFormPage(BasePage):
    """
    Класс страницы формы. Демонстрирует декларативное описание локаторов
    и инкапсуляцию сложного взаимодействия с веб-элементами.
    """
    def __init__(self, driver):
        super().__init__(driver)

        # Декларативная мапа локаторов (Специфика паттерна PageFactory в Python)
        # Формат: 'название_элемента': (тип_локатора, 'значение_локатора')
        # NOTE: обратите внимание - инициализация вне конструктора, реальная работа по первому обращению (lazy initizalization)
    locators = {
        'first_name': ('ID', 'firstName'),
        'last_name': ('ID', 'lastName'),
        'user_email': ('ID', 'userEmail'),

        'banner_button' : ('XPATH',  "//div[@id='fixedban']//button[@aria-label='Close']"),
        
        # Радиокнопки выбора пола (локаторы на кликабельные label)
        'gender_male': ('XPATH', "//label[@for='gender-radio-1']"),
        'gender_female': ('XPATH', "//label[@for='gender-radio-2']"),
        'gender_other': ('XPATH', "//label[@for='gender-radio-3']"),
        
        'user_number': ('ID', 'userNumber'),
        
        # Компоненты виджета календаря (DatePicker)
        'date_of_birth_input': ('ID', 'dateOfBirthInput'),
        'calendar_month_select': ('CLASS_NAME', 'react-datepicker__month-select'),
        'calendar_year_select': ('CLASS_NAME', 'react-datepicker__year-select'),
        # Динамический локатор для выбора конкретного дня (использует параметризацию через XPATH)
        'calendar_target_day': ('XPATH', "//div[contains(@class, 'react-datepicker__day') and not(contains(@class, 'outside-month')) and text()='{day}']"),
        
        # Поле автодополнения (кастомный выпадающий список)
        'subjects_input': ('ID', 'subjectsInput'),
        'subjects_auto_complete_option': ('XPATH', "//div[contains(@class, 'subjects-auto-complete__option')]"),
        
        # Чекбоксы хобби (локаторы на кликабельные label)
        'hobby_sports': ('XPATH', "//label[@for='hobbies-checkbox-1']"),
        'hobby_reading': ('XPATH', "//label[@for='hobbies-checkbox-2']"),
        'hobby_music': ('XPATH', "//label[@for='hobbies-checkbox-3']"),
        
        # Загрузка файлов и адресный блок
        'upload_picture_btn': ('ID', 'uploadPicture'),
        'current_address': ('ID', 'currentAddress'),
        
        # Кастомные выпадающие списки (React-Select) штата и города
        'state_dropdown': ('ID', 'state'),
        'state_input': ('XPATH', "//div[@id='state']//input"),
        'city_dropdown': ('ID', 'city'),
        'city_input': ('XPATH', "//div[@id='city']//input"),
        
        'submit_button': ('ID', 'submit'),
        
        # Модальное окно подтверждения результатов отправки
        'modal_title': ('ID', 'example-modal-sizes-title-lg'),
        'modal_table_rows': ('XPATH', "//div[@class='modal-body']//tbody/tr")
    }

    def _close_commercial_banner(self):
        self.banner_button.click()

    # --------------------------------------------------------------------------
    # Бизнес-методы (Действия на странице)
    # --------------------------------------------------------------------------
    def fill_personal_info(self, first_name: str, last_name: str, email: str, gender: str, mobile: str):
        """Заполнение основных персональных данных и выбор радиокнопок."""

        self._close_commercial_banner()

        self.first_name.set_text(first_name)
        self.last_name.set_text(last_name)
        self.user_email.set_text(email)
        
        # Выбор радиокнопки на основе переданного текста
        if gender.lower() == 'male':
            self.gender_male.click_button()
        elif gender.lower() == 'female':
            self.gender_female.click_button()
        else:
            self.gender_other.click_button()
            
        self.user_number.set_text(mobile)

    def select_date_of_birth(self, year: str, month: str, day: str):
        """Работа со сложным виджетом календаря (React DatePicker)."""
        self.date_of_birth_input.click_button()
        
        # Выбор из стандартных HTML-селектов внутри виджета
        self.calendar_year_select.select_element_by_value(year)
        self.calendar_month_select.select_element_by_text(month)
        
        # Динамическая замена плейсхолдера в XPATH для выбора дня
        xpath_tuple = self.locators['calendar_target_day']
        dynamic_xpath = xpath_tuple[1].format(day=day)
        
        # Поиск и клик по динамически сформированному локатору дня
        day_element = self.driver.find_element(xpath_tuple[0], dynamic_xpath)
        day_element.click()

    def enter_subjects(self, subjects: list):
        """Работа с полем ввода, поддерживающим автодополнение (React-Select)."""
        for subject in subjects:
            self.subjects_input.set_text(subject)
            # Ожидание появления подсказки и нажатие Enter/клик для фиксации элемента
            self.subjects_input.send_keys(Keys.ENTER)

    def select_hobbies(self, hobbies: list):
        """Выбор нескольких чекбоксов."""
        hobbies_map = {
            'sports': self.hobby_sports,
            'reading': self.hobby_reading,
            'music': self.hobby_music
        }
        for hobby in hobbies:
            hobby_lower = hobby.lower()
            if hobby_lower in hobbies_map:
                print(hobbies_map[hobby_lower])
                hobbies_map[hobby_lower].click_button()

    def upload_file(self, file_path: str):
        """Загрузка файла через прямую передачу абсолютного пути в input[type='file']."""
        # По правилам Selenium, для загрузки файлов используется отправка текста (пути к файлу)
        self.upload_picture_btn.send_keys(file_path)

    def fill_address_and_location(self, address: str, state: str, city: str):
        """Заполнение адреса и работа со сложными кастомными выпадающими списками."""
        self.current_address.set_text(address)
        
        # Для кастомных выпадающих списков React-Select: скроллим, вводим текст и нажимаем ENTER
        self.driver.execute_script("arguments[0].scrollIntoView(true);", self.state_dropdown)
        self.state_input.send_keys(state)
        self.state_input.send_keys(Keys.ENTER)
        
        self.city_input.send_keys(city)
        self.city_input.send_keys(Keys.ENTER)

    def submit_form(self):
        """Финальная отправка формы кликом по кнопке Submit через JavaScript (защита от перекрытия футером)."""
        self.driver.execute_script("arguments[0].click();", self.submit_button)

    def get_modal_results(self) -> dict:
        """Парсинг результирующей таблицы внутри модального окна в Python-словарь."""
        # Ожидаем появление заголовка модального окна для синхронизации
        self.modal_title.visibility_of_element_located()
        
        result_data = {}
        # Получаем список всех строк tr из таблицы результатов
        rows = self.driver.find_elements(*self.locators['modal_table_rows'])
        
        for row in rows:
            cells = row.find_elements_by_tag_name("td")
            if len(cells) == 2:
                label = cells[0].text.strip()
                value = cells[1].text.strip()
                result_data[label] = value
                
        return result_data

# ==============================================================================
# 4. ТЕСТОВЫЙ СЦЕНАРИЙ (Бизнес-логика проверки)
# ==============================================================================
def test_student_registration_form_max_capabilities(driver):
    """
    Комплексный тест, валидирующий сквозной сценарий заполнения формы
    и корректность отображения данных в результирующем модальном окне.
    """
    # Подготовка тестового файла для демонстрации Upload функционала
    test_filename = "demo_upload.txt"
    with open(test_filename, "w") as f:
        f.write("QA Guru PageFactory Demo File Content")
    abs_file_path = os.path.abspath(test_filename)

    try:
        # Инициализация POM-класса страницы
        page = AutomationPracticeFormPage(driver)
        page.open_url("https://qa-guru.github.io/one-page-form/automation-practice-form.html")

        # Выполнение цепочки бизнес-действий
        page.fill_personal_info(
            first_name="Ivan",
            last_name="Ivanov",
            email="ivanov@university.edu",
            gender="Male",
            mobile="1234567890"
        )

        # TODO: Дописать этот тест;
        # развить проект, возможно, добавив business action самого высокого порядка, вроде fill_form();
        # постараться использовать как можно больше возможностей библиотеки selenium-page-factory, максимум методов из расширения \ wrapper-а класса WebElement;
        # добавить параметризацию используя материалы занятий по pytest
        # https://pypi.org/project/selenium-page-factory/
        # https://selenium-page-factory.readthedocs.io/en/latest/

        #page.select_date_of_birth(year="2000", month="January", day="15")
        #page.enter_subjects(subjects=["Maths", "Computer Science"])
        #page.select_hobbies(hobbies=["Sports", "Music"])
        #page.upload_file(file_path=abs_file_path)
        #page.fill_address_and_location(address="123 University Avenue, Tomsk, Russia ;)",state="NCR",city="Delhi")
        page.submit_form()

        time.sleep(3)
        
        # Стадия верификации (Assertions) полученных результатов
        actual_results = page.get_modal_results()
        # Точечные жесткие проверки ключевых полей формы согласно ТЗ
        assert actual_results.get("Student Name") == "Ivan Ivanov", f"Ожидалось имя 'Ivan Ivanov', получено: {actual_results.get('Student Name')}"
        assert actual_results.get("Student Email") == "ivanov@university.edu"
        assert actual_results.get("Gender") == "Male"
        assert actual_results.get("Mobile") == "1234567890"
        assert actual_results.get("Date of Birth") == "15 January,2000"
        assert actual_results.get("Subjects") == "Maths, Computer Science"
        assert actual_results.get("Hobbies") == "Sports, Music"
        assert actual_results.get("Picture") == test_filename
        assert actual_results.get("Address") == "123 University Avenue, Tomsk, Russia"
        assert actual_results.get("State and City") == "NCR Delhi"
    finally:
        if os.path.exists(abs_file_path):
            os.remove(abs_file_path)
        pass


