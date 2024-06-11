from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd
import random
import sqlite3
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')


def create_database(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reviews
                 (source TEXT, date TEXT, title TEXT, text TEXT, rating INTEGER, product TEXT)''')
    conn.commit()
    conn.close()


def read_database(db_name):
    conn = sqlite3.connect(db_name)
    query = "SELECT * FROM reviews"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def flatten_list(nested_list):
    flat_list = []
    for item in nested_list:
        if isinstance(item, list):
            flat_list.extend(item)
        else:
            flat_list.append(item)
    return flat_list


def get_right_div_names(driver):
    # Find the div with id="svelte-ratings"
    reviews_div = driver.find_element(By.ID, "svelte-ratings")

    # Find all direct child divs under the div with id="svelte-ratings"
    reviews_child_div = reviews_div.find_elements(By.XPATH, './div')

    if len(reviews_child_div) == 1:
        reviews_child_child_divs = reviews_child_div[0].find_elements(
            By.XPATH, './div')
        reviews_child_child_divs.append(
            reviews_child_div[0].find_elements(By.XPATH, './ul'))

    # Flatten the list to handle nested lists
    reviews_child_child_divs = flatten_list(reviews_child_child_divs)

    filtered_elements = [
        child for child in reviews_child_child_divs if 'ratings-list' in child.get_attribute('class')]

    # Debugging-Ausgabe der Klassen der untergeordneten divs und ul
    return filtered_elements


def accept_cookies(driver):
    # Wait for the cookie consent popup to appear and accept cookies
    wait = WebDriverWait(driver, 10)
    accept_cookies_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//button[contains(text(), "Akzeptieren")]')
        )
    )
    time.sleep(random.randint(18, 65) / 17)
    accept_cookies_button.click()


def scrape_reviews(html_file, max_reviews):
    # Setup Selenium WebDriver (using Chrome in this example)
    driver = webdriver.Chrome()

    try:
        # Navigate to the PLP page
        driver.get(f"file:///{os.path.abspath(html_file)}")

        accept_cookies(driver)

        time.sleep(1)

        div_names = get_right_div_names(driver)

        for div in div_names:
            if not 'list-gh-only-wrapper' in div.get_attribute('class'):
                ratings_div_name = div.get_attribute('class')

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Find the div with id="svelte-ratings"
        reviews_div = soup.find("div", id="svelte-ratings")

        ratings_div = reviews_div.find(
            "div", class_=ratings_div_name)
        if (ratings_div == None):
            ratings_div = reviews_div.find(
                "ul", class_=ratings_div_name)

        print(ratings_div)

        # Rückgabe der gefundenen untergeordneten divs und ul
        # return reviews_child_child_divs

    finally:
        driver.quit()

# Example usage


if __name__ == "__main__":
    db_name = 'reviews.db'
    current_path = os.path.dirname(os.path.realpath(__file__))
    path_to_db = current_path + '/' + db_name

    create_database(path_to_db)

    print(read_database(path_to_db))

    html_file = "datamining/portfolio_1/test_data.html"
    max_reviews = 50
    product_name = 'Produktname'  # Ersetze durch den tatsächlichen Produktnamen
    child_divs = scrape_reviews(html_file, max_reviews)

    # Optionally, do something with the child_divs
    # if child_divs:
    #     for i, div in enumerate(child_divs, start=1):
    #         print(f"Child div {i}: {div.get_attribute('outerHTML')}")
