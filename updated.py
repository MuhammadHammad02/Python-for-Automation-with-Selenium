import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the driver
driver = webdriver.Chrome(service=Service('chromedriver.exe'))

# URL of the main page
base_url = 'https://aheart2help.com/org/california/'

# Data containers
results = []

# Iterate through pages
for page_number in range(1, 11):  # Adjust the range to cover more pages if needed
    driver.get(f'{base_url}?page={page_number}')
    
    # Data containers for each page
    map_links = []

    # Get the map links on the current page
    map_elements = driver.find_elements(By.XPATH, '//*[@id="main"]/div/section[2]/div/div[2]/div/div/div/div[1]/div/section[1]/div/div[2]/div/div[2]/div/div/a')
    for map_element in map_elements:
        map_links.append(map_element.get_attribute('href'))
    
    # Get the organization links
    selector = '.elementor-element-aef8c6d .elementor-size-sm'
    organization_name_selector = '.elementor-widget-container h2'

    # Iterate through organization links on the current page
    for i in range(len(map_links)):  # Adjust based on the number of available map links
        try:
            # Fetch the organization links again after each navigation
            links = WebDriverWait(driver, 60).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
            )
            
            if i < len(links):
                link = links[i]
                
                # Scroll to the element to make sure it's in view
                driver.execute_script("arguments[0].scrollIntoView(true);", link)
                
                # Wait until the element is clickable
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
                
                # Use JavaScript to click if standard click fails
                driver.execute_script("arguments[0].click();", link)
                
                # Fetch the organization name
                o_name = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, organization_name_selector))
                )

                # Collect the data into a dictionary
                data_dict = {
                    'organization': o_name.text,
                    'state': driver.find_element(By.XPATH, '//*[@id="main"]/div/section/div/div[1]/div/section[1]/div/div/div/div[2]/div/h2').text,
                    'zip': driver.find_element(By.XPATH, '//*[@id="main"]/div/section/div/div[1]/div/section[1]/div/div/div/div[4]/div/h2').text,
                    'ein': driver.find_element(By.XPATH, '//*[@id="main"]/div/section/div/div[1]/div/section[1]/div/div/div/div[5]/div/h2').text,
                    'ntee_common': driver.find_element(By.XPATH, '//*[@id="main"]/div/section/div/div[1]/div/section[4]/div/div/div/div/div/h2').text,
                    'organization_code': driver.find_element(By.XPATH, '//*[@id="main"]/div/section/div/div[1]/div/section[3]/div/div/div/div/div/h2').text,
                    'deductibility_code': driver.find_element(By.XPATH, '//*[@id="main"]/div/section/div/div[1]/div/section[5]/div/div/div/div/div/h2').text,
                    'ntee_code': driver.find_element(By.XPATH, '//*[@id="main"]/div/section/div/div[1]/div/section[6]/div/div/div/div/div/h2').text,
                    'affiliation_code': driver.find_element(By.XPATH, '//*[@id="main"]/div/section/div/div[1]/div/section[7]/div/div/div/div/div/h2').text,
                    'foundation_code': driver.find_element(By.XPATH, '//*[@id="main"]/div/section/div/div[1]/div/section[8]/div/div/div/div/div/h2').text,
                    'subsection_code': driver.find_element(By.XPATH, '//*[@id="main"]/div/section/div/div[1]/div/section[9]/div/div/div/div/div/h2').text,
                    'exempt_code': driver.find_element(By.XPATH, '//*[@id="main"]/div/section/div/div[1]/div/section[10]/div/div/div/div/div/h2').text,
                    'activity_code': driver.find_element(By.XPATH, '//*[@id="main"]/div/section/div/div[1]/div/section[11]/div/div/div/div/div/h2').text,
                    'tax_period': driver.find_element(By.XPATH, '//*[@id="main"]/div/section/div/div[1]/div/section[12]/div/div/div/div/div/h2').text,
                    'rulling_date': driver.find_element(By.XPATH, '//*[@id="main"]/div/section/div/div[1]/div/section[13]/div/div/div/div/div/h2').text,
                    'accounting_period': driver.find_element(By.XPATH, '//*[@id="main"]/div/section/div/div[1]/div/section[14]/div/div/div/div/div/h2').text,
                    'asset_code': driver.find_element(By.XPATH, '//*[@id="main"]/div/section/div/div[1]/div/section[15]/div/div/div/div/div/h2').text,
                    'income_code': driver.find_element(By.XPATH, '//*[@id="main"]/div/section/div/div[1]/div/section[16]/div/div/div/div/div/h2').text,
                    'asset_amount': driver.find_element(By.XPATH, '//*[@id="main"]/div/section/div/div[1]/div/section[17]/div/div/div/div/div/h2').text,
                    'income_amount': driver.find_element(By.XPATH, '//*[@id="main"]/div/section/div/div[1]/div/section[18]/div/div/div/div/div/h2').text,
                    'filing_req': driver.find_element(By.XPATH, '//*[@id="main"]/div/section/div/div[1]/div/section[19]/div/div/div/div/div/h2').text,
                    'form': driver.find_element(By.XPATH, '//*[@id="main"]/div/section/div/div[1]/div/section[20]/div/div/div/div/div/h2').text,
                    'PF': driver.find_element(By.XPATH, '//*[@id="main"]/div/section/div/div[1]/div/section[21]/div/div/div/div/div/h2').text,
                    'map_link': map_links[i] if i < len(map_links) else ''  # Include map link if available
                }
                results.append(data_dict)
                print(results)
                
                # Go back to the previous page
                driver.back()
                
                # Wait for the page to reload and links to be available again
                WebDriverWait(driver, 60).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
                )
            else:
                print(f"Link index {i} is out of range.")
        
        except Exception as e:
            print(f"An error occurred: {e}")

driver.quit()

# Save the results to a CSV file
with open('organizations_with_maps.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['organization', 'state', 'zip', 'ein', 'ntee_common', 'organization_code', 
                  'deductibility_code', 'ntee_code', 'affiliation_code', 'foundation_code', 
                  'subsection_code', 'exempt_code', 'activity_code', 'tax_period', 'rulling_date', 
                  'accounting_period', 'asset_code', 'income_code', 'asset_amount', 'income_amount', 
                  'filing_req', 'form', 'PF', 'map_link']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for data in results:
        writer.writerow(data)
