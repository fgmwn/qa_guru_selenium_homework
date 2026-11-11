from seleniumpagefactory.Pagefactory import PageFactory

# pip install selenium-page-factory

class TextBoxPage(PageFactory):
    URL = "https://qa-guru.github.io/one-page-form/text-box.html" # Частный случай
    
    def __init__(self, driver):
        self.driver = driver
        self.locators = {
            "full_name_input": ('ID', "userName"),
            "email_input": ('ID', "userEmail"),
            "current_address_input": ('ID', "currentAddress"),
            "permanent_address_input": ('ID', "permanentAddress"),
            "submit_button": ('ID', "submit"),
            "output_box": ('ID', "output"),
            "output_name": ('ID', "name"),
            "output_email": ('ID', "email"),
            "output_current_address": ('CSS', "#output #currentAddress"),
            "output_permnent_address": ('CSS', "#output #permanentAddress")
        }

    def open(self):
        self.driver.get(self.URL)

    def fill_form(self, name=None, email=None, cur_addr=None, perm_addr=None):
        if name is not None:
            self.full_name_input.send_keys(name)
        if email is not None:
            self.email_input.send_keys(email)
        if cur_addr is not None:
            self.current_address_input.send_keys(cur_addr)
        if perm_addr is not None:
            self.permanent_address_input.send_keys(perm_addr)
        
    def submit(self):
        # Прокрутка до кнопки и клик через JS, если перекрыта футером
        self.driver.execute_script("arguments[0].scrollIntoView(true);", self.submit_button)
        self.submit_button.click()

    def get_output_data(self):
        # Возвращает текст из блока вывода, если он появился
        if not self.output_box.is_displayed():
            return None
        
        # Парсинг строк (удаляем префиксы вроде 'Name:')
        name        = self.output_name.text.replace("Name:", "").strip()
        email       = self.output_email.text.replace("Email:", "").strip()
        cur_addr    = self.output_current_address.text.replace("Current Address :", "").strip()
        perm_addr   = self.output_permnent_address.text.replace("Permananet Address :", "").strip()
        
        return {"name": name, "email": email, "cur_addr": cur_addr, "perm_addr": perm_addr}

    def is_email_error_present(self):
        # Проверяем наличие класса ошибки у поля Email
        field_class = self.email_input.get_attribute("class")
        # TypeError: argument of type 'NoneType' is not a container or iterable
        # TODO: как нужно обновить - исправить проверку?
        return "field-error" in field_class or "error" in field_class or False

