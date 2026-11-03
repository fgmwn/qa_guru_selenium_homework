from selenium.webdriver.common.by import By

class TextBoxPage:
    URL = "https://qa-guru.github.io/one-page-form/text-box.html" # Частный случай
    
    # Локаторы элементов формы
    FULL_NAME           = (By.ID, "userName")
    EMAIL               = (By.ID, "userEmail")
    CURRENT_ADDRESS     = (By.ID, "currentAddress")
    PERMANENT_ADDRESS   = (By.ID, "permanentAddress")
    SUBMIT_BUTTON       = (By.ID, "submit")
    
    # Локаторы результирующего блока (вывода данных)
    OUTPUT_BOX          = (By.ID, "output")
    OUTPUT_NAME         = (By.ID, "name")
    OUTPUT_EMAIL        = (By.ID, "email")
    OUTPUT_CUR_ADDR     = (By.CSS_SELECTOR, "#output #currentAddress")
    OUTPUT_PERM_ADDR    = (By.CSS_SELECTOR, "#output #permanentAddress")

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)
        return self # NOTE: for Fluent Interface Implementation (just an example)

    def fill_form(self, name=None, email=None, cur_addr=None, perm_addr=None):
        if name is not None:
            full_name_field = self.driver.find_element(*self.FULL_NAME)            
            full_name_field.clear()
            full_name_field.send_keys(name)

            # NOTE: Вариант реализации в одну строчку
            #self.driver.find_element(*self.FULL_NAME).send_keys(name)

            # NOTE: Вариант реализации при котором создали low level action fill_in_full_name пусть и в одну строчку
            #self.fill_in_full_name(name)
        if email is not None:
            self.driver.find_element(*self.EMAIL).send_keys(email)
        if cur_addr is not None:
            self.driver.find_element(*self.CURRENT_ADDRESS).send_keys(cur_addr)
        if perm_addr is not None:
            self.driver.find_element(*self.PERMANENT_ADDRESS).send_keys(perm_addr)
        return self # NOTE: for Fluent Interface Implementation
    
    # В Python выделять low level action-ы в отдельные методы не принято
    def fill_in_full_name(self, name):
        self.driver.find_element(*self.FULL_NAME).send_keys(name)

    def submit(self):
        # Прокрутка до кнопки и клик через JS, если перекрыта футером
        button = self.driver.find_element(*self.SUBMIT_BUTTON)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
        button.click()
        return self # NOTE: for Fluent Interface Implementation

    def get_output_data(self):
        # Возвращает текст из блока вывода, если он появился
        if not self.driver.find_element(*self.OUTPUT_BOX).is_displayed():
            return None
        
        # Парсинг строк (удаляем префиксы вроде 'Name:')
        name = self.driver.find_element(*self.OUTPUT_NAME).text.replace("Name:", "").strip()
        email = self.driver.find_element(*self.OUTPUT_EMAIL).text.replace("Email:", "").strip()
        cur_addr = self.driver.find_element(*self.OUTPUT_CUR_ADDR).text.replace("Current Address :", "").strip()
        perm_addr = self.driver.find_element(*self.OUTPUT_PERM_ADDR).text.replace("Permananet Address :", "").strip()
        
        return {"name": name, "email": email, "cur_addr": cur_addr, "perm_addr": perm_addr}

    def is_email_error_present(self):
        # Проверяем наличие класса ошибки у поля Email
        email_field = self.driver.find_element(*self.EMAIL)
        field_class = email_field.get_attribute("class")
        # TypeError: argument of type 'NoneType' is not a container or iterable
        # TODO: как нужно обновить - исправить проверку?
        return "field-error" in field_class or "error" in field_class or False

