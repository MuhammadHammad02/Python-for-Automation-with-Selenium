from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

executable_path = 'chromedriver.exe'

chrome_service = Service(executable_path)

driver = webdriver.Chrome(service=chrome_service)

driver.get('https://opensource-demo.orangehrmlive.com/web/index.php/auth/login')

time.sleep(5)

user_name = driver.find_element(By.NAME, 'username')

user_name.send_keys('Admin')

id_pwd = driver.find_element(By.NAME, 'password').send_keys('admin123')

time.sleep(3)

btn = driver.find_element(By.CSS_SELECTOR, '.orangehrm-login-button').click()

time.sleep(10)
