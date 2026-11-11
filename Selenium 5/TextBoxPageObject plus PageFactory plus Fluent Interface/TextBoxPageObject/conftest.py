import pytest
from selenium import webdriver
#from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="function")
def driver():
    #options = Options()
    #options.add_argument("--headless")  # Запуск без графического интерфейса
    #options.add_argument("--window-size=1920,1080")
    #driver = webdriver.Chrome(options=options)
    
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

