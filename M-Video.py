from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

driver.get('https://www.mvideo.ru/')
assert "М.Видео - интернет-магазин" in driver.title

elem = driver.find_element_by_class_name('sel-hits-block')
#elems = elem.find_elements_by_class_name('c-product-tile__description-wrapper')

#button = elem.find_element_by_class_name('sel-hits-button-next')
button = WebDriverWait(elem,15).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'sel-hits-button-next'))
        )
button.click()

button = WebDriverWait(elem,15).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'sel-hits-button-next'))
        )
#button.click()

elems = elem.find_elements_by_class_name('c-product-tile__description-wrapper')

for prod in elems:
    print(prod.find_element_by_class_name('e-h4').get_attribute("title"))


#driver.quit()