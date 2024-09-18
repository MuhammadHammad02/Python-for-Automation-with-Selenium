from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

# Set up the webdriver (use the appropriate driver for your browser, e.g., ChromeDriver)
driver = webdriver.Chrome(executable_path='chromedriver.exe')

# Open the Playboard search page
url = "https://playboard.co/en/search?subscribers=100000%3A200000&country=PK&sortTypeId=1"
driver.get(url)

# Wait for the page to load fully
time.sleep(5)

# Function to scroll down and scrape new data
def scroll_and_scrape(driver, scroll_pause_time=15):
    last_height = driver.execute_script("return document.body.scrollHeight")
    scraped_channels = set()  # To track already scraped channels

    with open('playboard_data.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Channel Name', 'Link', 'Subscribers'])

        while True:
            # Find all channel elements by their XPath
            channels = driver.find_elements(By.XPATH, "//div[@class='channel-cell list__item']")
            new_data_found = False

            # Loop through each channel and extract data
            for channel in channels:
                try:
                    # Extract the channel name and link from the h2 a tag
                    name_element = channel.find_element(By.XPATH, ".//h2[@class='name']/a")
                    channel_name = name_element.text.strip()
                    channel_link = name_element.get_attribute("href")

                    # Extract the subscribers count from the ul li tag
                    subscribers_element = channel.find_element(By.XPATH, ".//ul[@class='simple-scores']/li[1]")
                    subscribers = subscribers_element.text.strip()

                    # Avoid scraping the same channel twice
                    if channel_name not in scraped_channels:
                        # Write the data to CSV
                        writer.writerow([channel_name, channel_link, subscribers])
                        scraped_channels.add(channel_name)
                        new_data_found = True  # Mark that new data was found
                        print(f"Scraped channel: {channel_name} with {subscribers}")

                except Exception as e:
                    print(f"Error occurred while scraping: {e}")
                    continue

            # Scroll down to the bottom of the page
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # Wait for the page to load new content
            time.sleep(scroll_pause_time)

            # Calculate new scroll height and compare with the last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                # Break the loop if no new content is loaded or no new data is found
                if not new_data_found:
                    print("All data scraped, no more new content to load.")
                    break

            last_height = new_height
            print("Scrolled to the bottom, checking for new content...")

# Scroll and scrape data
scroll_and_scrape(driver)

# Close the driver
driver.quit()
