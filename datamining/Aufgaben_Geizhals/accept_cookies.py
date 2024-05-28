from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd


def get_products_from_plp(base_url, num_pages):
    # Setup Selenium WebDriver (using Chrome in this example)
    driver = webdriver.Chrome()

    try:
        # Navigate to the PLP page
        driver.get(base_url)

        # Wait for the cookie consent popup to appear and accept cookies
        wait = WebDriverWait(driver, 10)
        accept_cookies_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[contains(text(), "Akzeptieren")]')
            )
        )
        accept_cookies_button.click()

        time.sleep(1)

        # Extract product information from the specified number of pages
        products = []
        for page in range(1, num_pages + 1):
            if page > 1:
                # Navigate to the next page if not the first
                next_page_button = driver.find_element(By.LINK_TEXT, str(page))
                next_page_button.click()

                time.sleep(1)

            # Get page source and parse with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, "html.parser")
            container_div = soup.find(
                "div", class_="listview card listview--filter-results"
            )
            product_list = container_div.find_all(
                "article", class_="listview__item")

            for product in product_list:
                product_name = product.find("h3", class_="listview__name")
                product_price = product.find("div", class_="listview__price")
                product_stars = product.find(
                    "div", class_="listview__content-left")
                product_offers = product.find(
                    "div", class_="listview__offercount")
                product_url_div = product.find("h3", class_="listview__name")
                product_url = product_url_div.find("a")

                title = product_name.find("a").get_text(strip=True)
                price = product_price.find(
                    "span", class_="price").get_text(strip=True)
                offers = product_offers.find("a").get_text(strip=True)
                stars_element = product_stars.find(
                    "span", {"aria-hidden": "true"})
                url = product_url.get("href")

                if stars_element:
                    stars = stars_element.get_text(strip=True)
                else:
                    stars = "No rating"

                products.append([title, price, stars, offers, url])

            time.sleep(1)

        return products

    finally:
        driver.quit()


# Example usage
base_url = "https://geizhals.de/?fs=tv&hloc=at&hloc=de"
num_pages = 3
products = get_products_from_plp(base_url, num_pages)
# for product in products:
#     print(product)

columns = ["title", "price", "stars", "offers", "url"]
dataframe = pd.DataFrame(products, columns=columns)
dataframe.to_csv("datamining/Aufgaben_Geizhals/fernseher.csv", index=False)
