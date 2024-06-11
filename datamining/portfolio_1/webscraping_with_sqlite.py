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
    if os.path.exists(db_name):
        os.remove(db_name)
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reviews
                 (source TEXT, date TEXT, title TEXT, text TEXT, rating TEXT, product TEXT)''')
    conn.commit()
    conn.close()


def read_database(db_name):
    conn = sqlite3.connect(db_name)
    query = "SELECT * FROM reviews"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def insert_review(db_name, source, date, title, text, rating, product):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("INSERT INTO reviews (source, date, title, text, rating, product) VALUES (?, ?, ?, ?, ?, ?)",
              (source, date, title, text, rating, product))
    conn.commit()
    conn.close()


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
        child for child in reviews_child_child_divs if 'ratings-list svelte' in child.get_attribute('class')]

    # Debugging-Ausgabe der Klassen der untergeordneten divs und ul
    return filtered_elements


def accept_cookies(driver):
    # Wait for the cookie consent popup to appear and accept cookies
    try:
        wait = WebDriverWait(driver, 10)
        accept_cookies_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[contains(text(), "Akzeptieren")]')
            )
        )
        time.sleep(random.randint(18, 65) / 17)
        accept_cookies_button.click()
    except Exception as e:
        print("No cookie consent button found or clickable")


def scrape_reviews(url, max_reviews, db_name):
    # Setup Selenium WebDriver (using Chrome in this example)
    options = webdriver.ChromeOptions()
    # Uncomment the next line to disable headless mode for debugging
    # options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    try:
        # Navigate to the PLP page
        driver.get(url)

        accept_cookies(driver)

        time.sleep(2)  # Increased wait time to ensure page loads

        # Scroll to the bottom of the page
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for content to load

        total_reviews_extracted = 0
        ratings_div_name = get_right_div_names(driver)

        while total_reviews_extracted < max_reviews:

            soup = BeautifulSoup(driver.page_source, "html.parser")

            # Find the div with id="svelte-ratings"
            reviews_div = soup.find("div", id="svelte-ratings")

            # Find all ul elements with the class name stored in ratings_div_name
            ul_elements = reviews_div.find_all(
                "ul", class_=ratings_div_name[0].get_attribute('class'))

            # Check if there are at least two ul elements
            if len(ul_elements) >= 2:
                # Select the second ul element
                second_ul = ul_elements[1]
            else:
                second_ul = ul_elements[0]

            # Find all li elements under this ul
            li_elements = second_ul.find_all('li')
            for i, li in enumerate(li_elements, start=1):
                if total_reviews_extracted >= max_reviews:
                    break

                # Extract required information from each li element
                source = li.find('span').find(
                    'a').text.strip() if li.find('span').find('a') else ''
                date = li.find('time')['datetime'] if li.find(
                    'time') else ''
                title = li.find('div', class_='ratings-title').find(
                    'strong').text.strip() if li.find('div', class_='ratings-title') else ''
                text = li.find('div', class_='ratings-text').text.strip(
                ) if li.find('div', class_='ratings-text') else ''
                rating = li.find('span', class_='stars-rating-label').text.strip(
                ) if li.find('span', class_='stars-rating-label') else ''
                product = li.find('span', class_='rating-for').find(
                    'a').text.strip() if li.find('span', class_='rating-for') else ''

                if source == '':
                    source = 'geizhals.de'

                # Print extracted information
                print(f"Review {total_reviews_extracted + 1}:")
                print(f"Quelle der Bewertung: {source}")
                print(f"Datum der Bewertung: {date}")
                print(f"Bewertungstitel: {title}")
                print(f"Bewertungstext: {text}")
                print(f"Sternebewertung: {rating}")
                print(f"Für welches Produkt: {product}")
                print()

                # Insert data into the database
                insert_review(db_name, source, date,
                              title, text, rating, product)
                total_reviews_extracted += 1

            # Check if there is a next page button and click it
            try:
                next_button = driver.find_element(
                    By.CSS_SELECTOR, 'a.pagination__page--next')
                next_button.click()
                # Increased wait time to ensure the next page loads
                time.sleep(5)
                # Scroll to the bottom of the next page
                driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)  # Wait for content to load
            except:
                print("No more pages or next button not found.")
                break

    finally:
        driver.quit()

# Example usage


if __name__ == "__main__":
    db_name = 'reviews.db'
    current_path = os.path.dirname(os.path.realpath(__file__))
    path_to_db = current_path + '/' + db_name

    create_database(path_to_db)

    # Direct URL to the product page
    url = "https://geizhals.de/lg-oled-g39la-v127135.html"
    max_reviews = 50
    scrape_reviews(url, max_reviews, path_to_db)

    # Optionally, do something with the filtered elements
    print(read_database(path_to_db))
