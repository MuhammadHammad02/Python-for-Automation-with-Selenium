from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time

# Path to your ChromeDriver executable
#chromedriver_path = "C:\Drivers\chromedriver.exe"
chrome_service = Service(executable_path="C:\Drivers\chromedriver.exe")

# Initialize the Chrome WebDriver
driver = webdriver.Chrome(service=chrome_service)

#browser = webdriver.Chrome(chromedriver_path)

# Open Google

driver.get("https://www.google.com/")

time.sleep(2) # Let the user actually see something!

# Find the search input field
search_box = driver.find_element(By.NAME, 'q')

# Enter a search query
search_query = "Selenium WebDriver"
search_box.send_keys(search_query)

time.sleep(2)

search_btn = driver.find_elements(By.CSS_SELECTOR, "input[type='submit']")[0]
search_btn.click()
# Submit the search form
#search_box.send_keys(Keys.RETURN)

# Wait for a few seconds to see the results
time.sleep(2)

# Close the browser
driver.quit()

'''
<textarea class="gLFyf" aria-controls="Alh6id" aria-owns="Alh6id" autofocus="" title="Search" value="" jsaction="paste:puy29d;" aria-label="Search" aria-autocomplete="both" aria-expanded="true" aria-haspopup="false" autocapitalize="off" autocomplete="off" autocorrect="off" id="APjFqb" maxlength="2048" name="q" role="combobox" rows="1" spellcheck="false" data-ved="0ahUKEwjLj6LJgP-GAxUUQ_EDHdrAD2IQ39UDCA0" aria-activedescendant="" style="" data-listener-added_9462a190="true"></textarea>
'''


'''
<input class="gNO89b" value="Google Search" aria-label="Google Search" name="btnK" role="button" tabindex="0" type="submit" data-ved="0ahUKEwjLj6LJgP-GAxUUQ_EDHdrAD2IQ4dUDCBY">
'''