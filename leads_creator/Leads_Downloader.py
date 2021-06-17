"""Качает лиды с указанной формы или со всех разом в фоновом режиме"""

"""Логика:
- Все в рамках одного словаря, ключ:значение:значение - ID_клиента : название_рабочей_страницы 
                                                                            : список_его_форм: количество_лидов
- Пройтись по всем клиентам из словаря и сделать:
-- Нажать на кнопку выбора страницы
-- Выбрать страницу, название которой совпадает с названием страницы из словаря
-- Пройтись по всем формам, сравнивая текущее количество лидов с сохраненным количеством из словаря
-- Если количество лидов изменилось, записать новое значение в словарь и скачать новые лиды
-- Отправить новые лиды по указанному ID_клиента
"""

import random
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def start_webdriver(initial_url):
    options = webdriver.ChromeOptions()

    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(r'--user-data-dir=C:\Users\asadm\AppData\Local\Google\Chrome\User Data') # Путь к данным гугла
    options.add_argument("--no-startup-window") # Активирует безоконный режим

    driver = webdriver.Chrome(
        r"C:\Programming\Телеграм бот\lead_sender_bot\leads_creator\chromedriver.exe", options=options)
    driver.get(initial_url)
    return driver


def download_from_forms(page_name, leads_of_form, driver):
    """Скачивает все новые лиды с указанной страницы."""

    wait = WebDriverWait(driver, 500)
    # Открывает нужную страницу, где хранятся лиды
    c = wait.until(EC.element_to_be_clickable((By.XPATH, f"//*[contains(@class, 'tn64ylxs')]")))
    time.sleep(random.randint(2, 5))
    c.click()
    time.sleep(random.randint(2, 5))
    wait.until(EC.element_to_be_clickable((
        By.XPATH, f"//*[contains(text(), '{page_name}')and not(contains(text(), '{c.text}'))]"))).click()
    time.sleep(random.randint(2, 5))
    driver.current_window_handle
    time.sleep(random.randint(2, 5))

    # Формирует список элементов с текстом
    elements_with_text = driver.find_elements_by_xpath(
        '//*[contains(@class, "l61y9joe j8otv06s a1itoznt te7ihjl9 kiex77na lgsfgr3h mcogi7i5 ih1xi9zn jrvjs1jy")]')
    # Формирует список элементов с кнопкой "Скачать"
    download_buttons = driver.find_elements_by_xpath("//*[contains(text(), 'Скачать')]")

    # Формирует список количества лидов для каждой формы
    numbers_of_leads = []
    for n in range(len(elements_with_text) - 1, int(len(elements_with_text) / len(download_buttons)) - 2, -4):
        time.sleep(random.randint(1, 2))
        numbers_of_leads.append(int(elements_with_text[n].text))
        numbers_of_leads.reverse()

    number_of_downloads = 0
    # Сравнивает количество лидов каждой формы с количеством лидов для этой формы в базе данных. Если появились новые,
    # скачивает их
    for form_number in range(0, len(leads_of_form), 1):
        if numbers_of_leads[form_number] > int(leads_of_form[form_number]):
            leads_of_form[form_number] = numbers_of_leads[form_number]
            download_buttons[form_number].click()
            time.sleep(random.randint(2, 5))
            wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Скачать новые лиды')]"))).click()
            time.sleep(random.randint(2, 4))
            wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'CSV'))).click()
            time.sleep(random.randint(2, 5))
            wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Закрыть'))).click()
            time.sleep(random.randint(5, 10))
            number_of_downloads += 1

    return number_of_downloads, leads_of_form
