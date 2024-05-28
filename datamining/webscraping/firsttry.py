import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
import time
from selenium.webdriver.common.by import By

url = "https://de.wikipedia.org/wiki/Python_(Programmiersprache)"

page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")
print(soup)

driver = webdriver.Chrome()
driver.get(url)
ActionChains(driver).click(driver.find_element(by=By.ID, value="jump-to-nav")).perform()

page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")
