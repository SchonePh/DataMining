import requests

# from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
import time
from selenium.webdriver.common.by import By

url = "https://www.google.com/search?q=python"
driver = webdriver.Chrome()
driver.get(url)

ActionChains(driver).click(driver.find_element(by=By.ID, value="L2AGLb")).perform()
time.sleep(2)

# Locate all <h3> elements
h3_elements = driver.find_elements(By.TAG_NAME, "h3")

# Collect the text from each <h3> element
h3_texts = [h3.text for h3 in h3_elements]

# Print the collected <h3> texts
for text in h3_texts:
    print(text)


driver.quit()
