from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
import random

# Set up WebDriver (make sure ChromeDriver path is correct)
service = Service(executable_path='chromedriver.exe')  # Update the path to chromedriver
driver = webdriver.Chrome(service=service)

# Wait for elements to appear
wait = WebDriverWait(driver, 15)

# Define the base URL for car listings
base_url = "https://www.cars.com/shopping/results/?makes[]=tesla&maximum_distance=all&models[]=&page={}&stock_type=all&zip="

# Function to simulate human-like pauses
def random_sleep(min_seconds, max_seconds):
    time.sleep(random.uniform(min_seconds, max_seconds))

# Function to scrape seller contact information from the car detail page
def scrape_contact_info(car_link):
    driver.get(car_link)
    random_sleep(2, 5)  # Simulate human behavior
    
    try:
        # Wait for contact information elements to load
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.sidebar-lead-form-container')))
        
        # Get the contact seller section
        contact_seller = driver.find_element(By.CSS_SELECTOR, 'div.sidebar-lead-form-container .dealer-phone')
        return contact_seller.text.strip()  # Get the phone number

    except Exception as e:
        print(f"Error scraping contact info: {e}")
    
    return 'N/A'  # Return 'N/A' if no contact information is found

# Function to scrape car details including links
def scrape_data():
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.vehicle-card')))
    cars = driver.find_elements(By.CSS_SELECTOR, 'div.vehicle-card')  # Fetch all car listings
    data = []

    for index in range(len(cars)):
        try:
            # Simulate human pause before interacting with each car
            random_sleep(2, 5)

            # Re-fetch the cars list to avoid stale element reference
            cars = driver.find_elements(By.CSS_SELECTOR, 'div.vehicle-card')  # Refresh car list
            car = cars[index]  # Get the current car element

            # Extract car details
            make_model = car.find_element(By.CSS_SELECTOR, 'h2.title').text.strip()
            price = car.find_element(By.CSS_SELECTOR, 'span.primary-price').text.strip()

            # Split make_model to get year, make, and model
            year = make_model.split(' ')[0]
            make = make_model.split(' ')[1]
            model = ' '.join(make_model.split(' ')[2:])

            # Get the link to the car details page
            car_link = car.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')

            # Scrape seller contact information from the car link
            seller_contact = scrape_contact_info(car_link)

            # Append the extracted data to the list
            data.append([year, make, model, price, seller_contact])

            # Go back to the previous page with the listings
            driver.back()
            random_sleep(2, 5)  # Wait for the page to load again
            
        except Exception as e:
            print(f"Error scraping car data on page, car index {index}: {e}")

    return data

# Function to navigate through pages and scrape data
def navigate_and_scrape(total_pages=5):
    all_data = []

    for page in range(1, total_pages + 1):
        print(f"Scraping page {page}")
        driver.get(base_url.format(page))  # Navigate to the current page
        
        # Scrape the current page
        page_data = scrape_data()
        all_data.extend(page_data)

        # Save to CSV after scraping each page to avoid data loss
        with open('cars_data.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if page == 1:  # Write the header only once
                writer.writerow(['Year', 'Make', 'Model', 'Price', 'Seller Contact'])
            writer.writerows(page_data)

        print(f"Data for page {page} saved to CSV")

        random_sleep(2, 5)  # Delay to avoid being flagged as a bot

    return all_data

# Start scraping
try:
    car_data = navigate_and_scrape(total_pages=5)  # Set the number of pages you want to scrape
finally:
    driver.quit()

print("Scraping completed and data saved.")
