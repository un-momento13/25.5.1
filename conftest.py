import pytest
from selenium import webdriver

@pytest.fixture(autouse=True)
def driver():
   driver = webdriver.Chrome()
   driver.implicitly_wait(5)
   # Переходим на страницу авторизации
   driver.maximize_window()
   driver.get('https://petfriends.skillfactory.ru/login')

   yield driver

   driver.quit()
   
