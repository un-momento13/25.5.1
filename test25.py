import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test25_3_1__25_5_1(driver):
    driver.find_element(By.ID, 'email').send_keys('un-momento@yandex.ru')  # Вводим email
    driver.find_element(By.ID, 'pass').send_keys('789456')  # Вводим пароль
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()  # Нажимаем на кнопку входа в аккаунт

    element = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.XPATH, '//*[@href="/my_pets"]'))
    )

    element.click()

    # Проверяем, что мы на нужной странице
    WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.ID, 'all_my_pets'))
    )

    # Число питомцев у пользователя
    str1 = driver.find_element(By.XPATH, '//*[@class=".col-sm-4 left"]').get_attribute("innerHTML")
    start = str1.find('Питомцев:') + len('Питомцев: ')
    stop = str1.find('<br>')
    num1 = int(str1[start:stop])

    cells = driver.find_elements(By.XPATH, '//tbody/tr/td')     # Ищем все ячейки таблиц
    empty_cell = 0                                              # признак пустой ячейки
    i = 0                                                       # для подсчета номера ячейки
    names = set()                                               # имена
    pets = set()                                                # набор строк имя+возраст+порода
    pet = str()                                                 # строка имя+возраст+порода

    for cell in cells:
        i += 1

        if i % 4 == 0:                          # Пропускаем ячейки с кнопкой удалить питомца
            pets.add(pet)                       # Добавляем питомца в набор
            pet = ''                            # Чистим строку
            continue                            # Переходим на следующую строку

        pet = pet + cell.text                   # Формируем питомца (имя+возраст+порода)

        if cell.text.replace(' ', '') == "":    # Ячейка имя, возраст или порода пустая
            empty_cell = 1                      # Выставляем флаг - ячейка пустая

        if (i - 1) % 4 == 0:                    # Ячейки с именами
            names.add(cell.text)                # Добавляем имя в набор

    assert num1 == (len(driver.find_elements(By.TAG_NAME, 'tr')) - 1)           # Присутствуют все питомцы
    assert len(driver.find_elements(By.XPATH, '//img[@src=""]')) <= num1 // 2   # Хотя бы у половины питомцев есть фото ((num1 / 2 + 0.5) // 1) - если бы искали не пустые ячейки, а со ссылками

    # Ни один из нижележащих тестов не проходит на том наборе данных, который имеется.
    assert empty_cell == 0                    # У всех питомцев есть имя, возраст и порода.
    assert len(names) == num1                 # Имена уникальны
    assert len(pets) == num1                  # Питомцы уникальны (повторяющиеся питомцы — это питомцы, у которых одинаковое имя, порода и возраст)
