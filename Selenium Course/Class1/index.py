from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

executable_path = 'chromedriver.exe'

chrome_service = Service(executable_path)

driver = webdriver.Chrome(service=chrome_service)

driver.get('https://www.google.com/')

time.sleep(5)


search_btn = driver.find_element(By.NAME, "q")

search_query= "facebook"

search_btn.send_keys(search_query)

time.sleep(5)

search_btn.send_keys(Keys.ENTER)

time.sleep(5)



