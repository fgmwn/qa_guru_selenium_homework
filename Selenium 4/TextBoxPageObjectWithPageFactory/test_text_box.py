import pytest
import time
from text_box_page_pf import TextBoxPage

# TODO: Запустить все тесты без использования PageFactory и с использованием, сравнить количество пройденных и падений, сравнить ошибки при падениях
# TODO: Если количество падений разное - найти ответ почему? ну или задать вопрос сперва Алексу, а потом и лектору :)

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

# 4. Запуск всех тестов
#pytest -v test_text_box.py

# 4. Запуск конкретного параметризованного метода (TestSuite)
#pytest -v test_text_box.py::test_empty_form_submission

# 4. Запуск конкретного тест-кейса из параметризованного набора
#pytest test_text_box.py::test_positive_form_submission[John Doe-john@example.com-123 Elm St-456 Oak St] -v

# TODO: как улучшить проверки в существующих тестах с предлагаемыми данными?
# --- 1. Позитивные сценарии (Валидные данные) ---
@pytest.mark.parametrize("name, email, cur_addr, perm_addr", [
    ("John Doe", "john@example.com", "123 Elm St", "456 Oak St"),                      # Стандартный кейс
    ("Иван Иванов", "ivan@mail.ru", "ул. Ленина, д. 1", "ул. Пушкина, д. 2"),          # Кириллица
    ("A", "a@b.cc", "B", "C"),                                                         # Минимальная длина строк
    ("Name-With Dash", "dash@email.co.uk", "Addr 1/2", "Addr 3 & 4"),                  # Спецсимволы в полях
    ("   John   ", "spaces@test.com", "  Street 1  ", "  Street 2  "),                 # Строки с пробелами
])
def test_positive_form_submission(driver, name, email, cur_addr, perm_addr):
    #page = TextBoxPage(driver).open() # TODO: Мы еще поговорим о таком варианте реализации
    
    page = TextBoxPage(driver)
    page.open()
    page.fill_form(name, email, cur_addr, perm_addr)
    page.submit()    
    output = page.get_output_data()

    # TODO: Мы еще поговорим о таком варианте реализации
    # Fluent Interface Impl:
    #output = page.fill_form(name, email, cur_addr, perm_addr).submit().get_output_data()

    # Fluent Interface Impl (Java, C#, C++ style):
    #output = page.fill_form(name, email, cur_addr, perm_addr)
    #                .submit()
    #                .get_output_data()

    time.sleep(3) # tmp solution

    assert output is not None, "Блок с результатами не отобразился"
    assert output["name"] == name.strip()
    assert output["email"] == email.strip()
    assert output["cur_addr"] == cur_addr.strip()
    assert output["perm_addr"] == perm_addr.strip()


# --- 2. Частичное заполнение обязательных/необязательных полей ---
@pytest.mark.parametrize("name, email, cur_addr, perm_addr", [
    ("Only Name", "", "", ""),
    ("", "only@email.com", "", ""),
    ("", "", "Only Current Address", ""),
    ("", "", "", "Only Permanent Address"),
    ("Name & Email", "name_email@test.com", "", ""),
])
def test_partial_form_submission(driver, name, email, cur_addr, perm_addr):
    page = TextBoxPage(driver)
    page.open()
    page.fill_form(name, email, cur_addr, perm_addr)
    page.submit()    
    output = page.get_output_data()

    time.sleep(3) # tmp solution

    assert output is not None, "Форма должна отправляться при частичном заполнении"
    if name: assert output["name"] == name
    if email: assert output["email"] == email
    if cur_addr: assert output["cur_addr"] == cur_addr
    if perm_addr: assert output["perm_addr"] == perm_addr


# --- 3. Негативные сценарии (Невалидный Email) ---
@pytest.mark.parametrize("invalid_email", [
    "plainaddress",          # Нет собаки и домена
    "@no-local-part.com",    # Нет имени пользователя
    "john.doe@com",          # Нет доменной зоны верхнего уровня - TODO: обратите особое внимание
    "john@missing-dot",      # Нет точки в домене - TODO: обратите особое внимание
    "john@@example.com",     # Две собаки
    "john@example..com",     # Две точки подряд
])
def test_invalid_email_validation(driver, invalid_email):
    page = TextBoxPage(driver)
    page.open()
    page.fill_form(name="Test", email=invalid_email)
    page.submit()
    
    # Ожидаем, что блок вывода не появился ИЛИ поле подсвечено ошибкой
    output = page.get_output_data()

    time.sleep(3) # tmp solution

    assert output is None or page.is_email_error_present(), f"Email '{invalid_email}' не должен быть принят системой"


# --- 4. Граничные значения и нагрузка на длину полей (Длинные строки) ---
@pytest.mark.parametrize("field_type, long_string", [
    ("name", "A" * 1000),                             # Экстремально длинное имя
    ("email", f"{'b' * 64}@example.com"),             # Максимальная длина локальной части email
    ("cur_addr", "Current " * 200),                   # Длинный адрес (проверка на переполнение)
    ("perm_addr", "Permanent " * 200)                 # Длинный адрес
])
def test_long_input_fields(driver, field_type, long_string):
    page = TextBoxPage(driver).open()
    
    # TODO: условные операторы в тесте, как можно от них избавиться и станет ли от этого понятнее решение?
    if field_type == "name": page.fill_form(name=long_string)
    elif field_type == "email": page.fill_form(email=long_string)
    elif field_type == "cur_addr": page.fill_form(cur_addr=long_string)
    elif field_type == "perm_addr": page.fill_form(perm_addr=long_string)
        
    page.submit()
    output = page.get_output_data()

    time.sleep(3) # tmp solution

    assert output is not None, f"Форма не справилась с длинной строкой в поле {field_type}"


# --- 5. Безопасность и спец-инъекции (XSS, SQLi, Эмодзи) ---
@pytest.mark.parametrize("security_payload", [
    "<script>alert('xss')</script>",                 # Базовый XSS скрипт - TODO: нашли и исправили ошибку?
    "1' OR '1'='1",                                  # Базовая SQL-инъекция
    ":):):):))))::;)",                               # Суррогатные пары (Эмодзи)
    "<div>HTML injection</div>"                      # Теги верстки - нашли ошибку? - TODO: нашли и исправили ошибку?
])
def test_security_and_special_inputs(driver, security_payload):
    page = TextBoxPage(driver).open()
    # Заполняем все поля потенциально опасным контентом
    page.fill_form(name=security_payload, cur_addr=security_payload, perm_addr=security_payload)
    page.submit()    
    output = page.get_output_data()

    time.sleep(3) # tmp solution

    assert output is not None, "Форма упала при вводе спецсимволов/инъекций"
    # Текст должен отобразиться строго как строка, а не выполниться кодом
    assert output["name"] == security_payload


# --- 6. Пустая форма ---
def test_empty_form_submission(driver):
    page = TextBoxPage(driver).open()
    page.submit()    
    output = page.get_output_data()

    time.sleep(3) # tmp solution

    # Зависит от требований: либо форма не отправляется (None), либо пустые строки
    if output is not None:
        assert output["name"] == ""
        assert output["email"] == ""
