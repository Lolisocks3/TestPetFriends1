import re
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="function")
def driver():
    service = Service(executable_path='C:/chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    # Переходим на страницу авторизации
    driver.get('https://petfriends.skillfactory.ru/login')

    yield driver

    driver.quit()


def login(driver):
    login_button = '/html/body/div/div/form/div[3]/button'
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('223test23@mail.ru')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('23test23@mail.ru12')
    driver.find_element(By.XPATH, login_button).click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.XPATH, '/html/body/div/div/div[2]')
    driver.find_element(By.CLASS_NAME, 'nav-link').click()


def test_login(driver):
    login(driver)
    driver.implicitly_wait(10)


def test_pet_board(driver):
    login(driver)
    assert WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='.col-sm-8 right fill']"))
    )


def test_pets_cards(driver):
    login(driver)
    driver.implicitly_wait(10)
    # Поиск всех строк в таблице
    tr_elements = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')

    # Поиск элемента с классом '.col-sm-4 left' и извлечение текста
    pet_number_raw = driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]')
    pet_number_text = pet_number_raw.text

    # Поиск всех ячеек с возрастом питомцев
    pet_age_raw = driver.find_elements(By.XPATH, '/html/body/div[1]/div/div[2]/div/div/table/tbody/tr/td[1]')

    # Извлечение текста из каждой ячейки
    pet_ages = [element.text for element in pet_age_raw]

    # Используем регулярное выражение для извлечения числа питомцев из строки
    match = re.search(r'Питомцев:\s*(\d+)', pet_number_text)
    if match:
        pet_number = int(match.group(1))
        print("Всего питомцев:", pet_number)
    else:
        print("ERROR")
        pet_number = 0  # Устанавливаем значение 0, если не удалось извлечь число

    image_pets = driver.find_elements(By.CSS_SELECTOR, 'img[src*="data:image"]')
    if len(image_pets) > 0:
        print(f"Найдено {len(image_pets)} питомцев с фото")

    if len(tr_elements) > 0:
        print(f"Найдено {len(tr_elements)} питомцев")

    # Проверка соответствия найденного количества питомцев фактическому
    assert len(tr_elements) == pet_number

    # Вывод результатов
    print("Возраст питомцев:", pet_ages)
