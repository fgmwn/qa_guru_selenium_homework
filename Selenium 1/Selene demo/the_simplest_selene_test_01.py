from selene import browser, have

# python -m venv venv
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# venv\Scripts\activate

# pip install -r requirements.txt
# pip show selene selenium

# python script.py

# There is the place where screenshots placed C:\Users\user\.selene\screenshots\1783075108353

# https://github.com/yashaka/selene

# "selene ImportError: cannot import name 'AnyDevice' from 'selenium.webdriver.common.action_chains'"
# selene 2.0.0rc9 была выпущена в марте 2024 года. В тот период Selenium еще не использовал внутренний тип AnyDevice в своем модуле action_chains.
# selenium 4.44.0 была выпущена в мае 2026 года. В этой современной версии разработчики Selenium обновили аннотации типов и добавили AnyDevice, сломав обратную совместимость со старыми релиз-кандидатами Selene.
# Решение: понизить версию Selenium под вашу текущую Selene (на виртуальном env)
# pip install "selenium>=4.12.0,<4.17.0"

# 1. Создание виртуального окружения
# python -m venv venv

# 1.5 Если не отработал пункт 2 под Windows
# PowerShell: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 2. Активация (Для Windows)
# venv\Scripts\activate
# 2. Активация (Для macOS/Linux)
#source venv/bin/activate

# В случае возникновения проблем может пригодиться
# pip install --force-reinstall selene==2.0.0rc9 --pre

def test_google_search():
    # 1. Открываем главную страницу Google
    browser.open('https://google.com')

    # 2. Находим поле поиска, вводим текст и нажимаем Enter
    browser.element('[name="q"]').type('selene python').press_enter()

    # 3. Проверяем, что на странице результатов есть ссылка на GitHub
    browser.element('#search').should(have.text('yashaka/selene'))

test_google_search()

