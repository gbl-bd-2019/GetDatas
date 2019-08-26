from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from pprint import pprint
from pymongo import MongoClient
client = MongoClient('mongodb://127.0.0.1:27017')
db = client['mail_letters']
ldb = db.mail_letters

driver = webdriver.Chrome()

driver.get('https://mail.ru/')
assert "Mail.ru: почта" in driver.title

elem = driver.find_element_by_id("mailbox:login")
elem.send_keys('study.ai_172')
elem = driver.find_element_by_id("mailbox:password")
elem.send_keys('Password172')
elem.send_keys(Keys.RETURN)

elem = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.CLASS_NAME, "dataset-letters")))

assert "Входящие - Почта Mail.ru" in driver.title

# elem = driver.find_element_by_class_name('llc')
# attr_value = elem.get_attribute("href")
# print(attr_value)
elems = driver.find_elements_by_class_name('llc')
letters = []
for letr in elems:
    ltr_url = letr.get_attribute("href")
#    letters
    letr_from = letr.find_element_by_class_name('ll-crpt').get_attribute("title")
    letr_tema = letr.find_element_by_class_name('llc__subject').text
    letr_date = letr.find_element_by_class_name('llc__item_date').get_attribute("title")
#    letr_tema = letr_from. #.get_attribute("title")

    letters.append({
        'from': letr_from,
        'tema': letr_tema,
        'date': letr_date,
        'text': ltr_url
    })

pprint(letters)

for letr in letters:
    driver.get(letr['text'])
    elem = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.CLASS_NAME, "letter-body")))
    letr_text = driver.find_element_by_class_name('letter-body').text.strip()
    letr['text'] = letr_text

print('=======================================')
print('=======================================')
print('=======================================')
pprint(letters)

ldb.insert_many(letters)   # загрузка в базу

driver.quit()