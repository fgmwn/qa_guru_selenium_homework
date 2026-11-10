from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from seleniumpagefactory.Pagefactory import PageFactory


class TextBoxPage:
    URL = 'https://qa-guru.github.io/one-page-form/text-box.html'
    _LOCATORS = {
        'name': (By.ID, 'userName'), 'email': (By.ID, 'userEmail'),
        'cur_addr': (By.CSS_SELECTOR, '#userForm #currentAddress'),
        'perm_addr': (By.CSS_SELECTOR, '#userForm #permanentAddress'),
        'submit_button': (By.ID, 'submit'), 'output': (By.ID, 'output'),
        'result_name': (By.CSS_SELECTOR, '#output #name'),
        'result_email': (By.CSS_SELECTOR, '#output #email'),
        'result_cur_addr': (By.CSS_SELECTOR, '#output #currentAddress'),
        'result_perm_addr': (By.CSS_SELECTOR, '#output #permanentAddress'),
    }

    def __init__(self, driver):
        self.driver = driver

    def _element(self, name):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self._LOCATORS[name]))

    def open(self):
        self.driver.get(self.URL)
        return self

    def fill_form(self, name='', email='', cur_addr='', perm_addr=''):
        for key, value in [('name', name), ('email', email), ('cur_addr', cur_addr), ('perm_addr', perm_addr)]:
            field = self._element(key)
            field.clear()
            field.send_keys(value)
        return self

    def submit(self):
        button = self._element('submit_button')
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", button)
        button.click()
        return self

    def is_output_visible(self):
        return self.driver.find_element(*self._LOCATORS['output']).is_displayed()

    def is_email_invalid(self):
        return not self._element('email').get_property('validity')['valid']

    def get_output_data(self):
        prefixes = {'name': 'Name:', 'email': 'Email:',
                    'cur_addr': 'Current Address :', 'perm_addr': 'Permananet Address :'}
        return {key: self._element('result_' + key).text.removeprefix(prefix).strip()
                for key, prefix in prefixes.items()}


class TextBoxPagePF(TextBoxPage, PageFactory):
    def __init__(self, driver):
        super().__init__(driver)
        types = {By.ID: 'ID', By.CSS_SELECTOR: 'CSS'}
        self.locators = {'pf_' + key: (types[by], value)
                         for key, (by, value) in self._LOCATORS.items()}

    def _element(self, name):
        return getattr(self, 'pf_' + name)
