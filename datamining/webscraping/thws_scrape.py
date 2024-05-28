import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
import time
from selenium.webdriver.common.by import By

# URL of the website to scrape
url = "https://www.thws.de"

# Initialize the WebDriver
driver = webdriver.Chrome()

# Open the URL
driver.get(url)

# Locate the element with ID 'nav'
nav_element = driver.find_element(By.ID, "nav")

# Retrieve the list items within the 'nav' element
list_items = nav_element.find_elements(By.TAG_NAME, "li")

# Iterate through each list item
for list_item in list_items:
    # Find the anchor tag within the list item
    try:
        anchor = list_item.find_element(By.TAG_NAME, "a")
        # Retrieve the href attribute value
        href = anchor.get_attribute("href")
        # print(href)
        page = requests.get(href)
        soup = BeautifulSoup(page.content, "html.parser")

        print(soup.title.string)
    except Exception as e:
        None
# Quit the WebDriver
driver.quit()
