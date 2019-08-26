from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
driver = webdriver.Chrome()

driver.get('https://travelata.ru/cuba/resorts/varadero/hotels/grand-memories-varadero-ex-riu-varadero-5.html#?fromCity=2&dateFrom=22.10.2019&dateTo=22.10.2019&nightFrom=11&nightTo=11&priceFrom=10000&priceTo=500000&adults=2&meal=all&activeTab=tours&sid=0&hsid=0k2k66r3yi')
assert "Туры в отель Grand Memories" in driver.title

elem = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.CLASS_NAME, 'popupClose')))

elems = driver.find_element_by_class_name('lotteryDg__title')
print(elems.text)

alert = driver.switch_to_alert()
alert.dismiss()

# button = driver.find_element_by_class_name('popupClose')
# button = button.find_element_by_class_name('icon-i16_x')
# button.click()


# elem = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.CLASS_NAME, "hotelToursList__show-more-hotels")))
#
# button = driver.find_element_by_class_name('hotelToursList__show-more-hotels')
# button.click()

#driver.quit()