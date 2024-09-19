from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time


executable_path = 'chromedriver.exe'

chrome_service = Service(executable_path)

driver = webdriver.Chrome(service=chrome_service)

driver.get('https://www.saucedemo.com/')

time.sleep(5)


user_name = driver.find_element(By.NAME, 'user-name')
user_name.send_keys('standard_user')

time.sleep(2)

user_pas = driver.find_element(By.ID, 'password').send_keys('secret_sauce')

time.sleep(2)


log_in = driver.find_element(By.CSS_SELECTOR, '#login-button').click()

time.sleep(10)



# Navigate to the webpage (replace with the actual URL of the page)
driver.get("https://www.saucedemo.com/inventory.html")

time.sleep(10)

# Find all items on the page
items = driver.find_elements(By.CLASS_NAME, 'inventory_item')

# List to store the scraped data
data = []

for item in items:
    # Scrape the title, description, price,
    title = item.find_element(By.CLASS_NAME, 'inventory_item_name').text
    description = item.find_element(By.CLASS_NAME, 'inventory_item_desc').text
    price = item.find_element(By.CLASS_NAME, 'inventory_item_price').text
    
    
    # Append the data to the list
    data.append({
        'Title': title,
        'Description': description,
        'Price': price,
        
    })

# Close the browser
driver.quit()

# Convert the data into a DataFrame
df = pd.DataFrame(data)

# Save the data to an Excel file
df.to_excel('inventory_data.xlsx', index=False)

print("Data scraped and saved successfully!")


