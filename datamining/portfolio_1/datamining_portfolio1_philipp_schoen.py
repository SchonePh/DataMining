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
    """
    Creates a SQLite database.
    If the database already exists, it will be deleted and recreated.

    Parameters:
    db_name (str): Name of the database file.
    """
    if os.path.exists(db_name):
        os.remove(db_name)
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reviews
                 (source TEXT, date TEXT, title TEXT, text TEXT, rating TEXT, product TEXT)''')
    conn.commit()
    conn.close()


def read_database(db_name):
    """
    Prints contents of DataBase and returns it as pandas DataFrame.

    Parameters:
    db_name (str): Name of the database file.

    Returns:
    pandas.DataFrame: DataFrame containing the reviews.
    """
    conn = sqlite3.connect(db_name)
    query = "SELECT * FROM reviews"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def insert_review(db_name, source, date, title, text, rating, product):
    """
    Inserts review into SQLite DataBase.

    Parameters:
    db_name (str): Name of the database file.
    source (str): source of the review.
    date (str): date of the review.
    title (str): title of the review.
    text (str): text of the review.
    rating (str): rating of the review.
    product (str): reviewed product.
    """
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("INSERT INTO reviews (source, date, title, text, rating, product) VALUES (?, ?, ?, ?, ?, ?)",
              (source, date, title, text, rating, product))
    conn.commit()
    conn.close()


def flatten_list(nested_list):
    """
    Flattens a nested list.

    Parameters:
    nested_list (list): nested list.

    Returns:
    list: returns the flattened list.
    """
    flat_list = []
    for item in nested_list:
        if isinstance(item, list):
            flat_list.extend(item)
        else:
            flat_list.append(item)
    return flat_list


def get_ratings_div_name(driver):
    """
    Searches for the name of the div containing the reviews.

    Parameters:
    driver (webdriver): Selenium WebDriver instance.

    Returns:
    list: list of filtered elements that contain the ratings.
    """
    reviews_div = driver.find_element(By.ID, "svelte-ratings")
    reviews_child_div = reviews_div.find_elements(By.XPATH, './div')

    if len(reviews_child_div) == 1:
        reviews_child_child_divs = reviews_child_div[0].find_elements(
            By.XPATH, './div')
        reviews_child_child_divs.append(
            reviews_child_div[0].find_elements(By.XPATH, './ul'))

    reviews_child_child_divs = flatten_list(reviews_child_child_divs)
    filtered_elements = [
        child for child in reviews_child_child_divs if 'ratings-list svelte' in child.get_attribute('class')]

    return filtered_elements


def accept_cookies(driver):
    """
    Accepts cookies on the website by clicking the appropriate button with a random delay.

    Parameters:
    driver (webdriver): Selenium WebDriver instance.
    """
    try:
        wait = WebDriverWait(driver, 10)
        accept_cookies_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[contains(text(), "Akzeptieren")]'))
        )
        time.sleep(random.uniform(1.5, 4.8))
        accept_cookies_button.click()
    except Exception:
        print("No cookie consent button found or clickable")


def setup_driver():
    """
    Sets up the Selenium WebDriver with the necessary options.

    Returns:
    webdriver: The configured Selenium WebDriver instance.
    """
    options = webdriver.ChromeOptions()
    # Uncomment the next line to disable headless mode for debugging
    # options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    return driver


def load_page(driver, url):
    """
    Loads the webpage, accepts cookies, and scrolls to the bottom of the page.
    Scrolling is important, because otherwise the javascript of the reviews isn't getting loaded

    Parameters:
    driver (webdriver): Selenium WebDriver instance.
    url (str): URL of the webpage to load.
    """
    driver.get(url)
    accept_cookies(driver)
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)


def extract_reviews(soup, ratings_div_name):
    """
    Extracts reviews from BeautifulSoup object.

    Parameters:
    soup (BeautifulSoup): BeautifulSoup object containing the page source.
    ratings_div_name (str): Class name of the div containing the ratings.

    Returns:
    list: list of tuples, each containing the extracted review information.
    """
    reviews_div = soup.find("div", id="svelte-ratings")
    ul_elements = reviews_div.find_all("ul", class_=ratings_div_name)

    second_ul = ul_elements[1] if len(ul_elements) >= 2 else ul_elements[0]
    li_elements = second_ul.find_all('li')

    reviews = []
    for li in li_elements:
        source = li.find('span').find('a').text.strip() if li.find(
            'span').find('a') else 'geizhals.de'
        date = li.find('time')['datetime'] if li.find('time') else ''
        title = li.find('div', class_='ratings-title').find(
            'strong').text.strip() if li.find('div', class_='ratings-title') else ''
        text = li.find('div', class_='ratings-text').text.strip(
        ) if li.find('div', class_='ratings-text') else ''
        rating = li.find('span', class_='stars-rating-label').text.strip(
        ) if li.find('span', class_='stars-rating-label') else ''
        product = li.find('span', class_='rating-for').find(
            'a').text.strip() if li.find('span', class_='rating-for') else ''

        reviews.append((source, date, title, text, rating, product))

    return reviews


def scrape_reviews(url, max_reviews, db_name):
    """
    Scrapes reviews from the given URL and inserts them into a SQLite database.

    Parameters:
    url (str): URL of the product page to scrape.
    max_reviews (int): maximum number of reviews to scrape.
    db_name (str): name of the database file.
    """
    driver = setup_driver()

    try:
        load_page(driver, url)
        total_reviews_extracted = 0
        ratings_div_name = get_ratings_div_name(
            driver)[0].get_attribute('class')

        while total_reviews_extracted < max_reviews:
            soup = BeautifulSoup(driver.page_source, "html.parser")
            reviews = extract_reviews(soup, ratings_div_name)

            for review in reviews:
                if total_reviews_extracted >= max_reviews:
                    break
                insert_review(db_name, *review)
                total_reviews_extracted += 1

            try:
                next_button = driver.find_element(
                    By.CSS_SELECTOR, 'a.pagination__page--next')
                next_button.click()
                time.sleep(random.uniform(1, 3.5))
                driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.uniform(1, 3.5))
            except:
                print("No more pages or next button not found.")
                break

    finally:
        driver.quit()


if __name__ == "__main__":
    db_name = 'reviews.db'
    current_path = os.path.dirname(os.path.realpath(__file__))
    path_to_db = os.path.join(current_path, db_name)

    create_database(path_to_db)

    # https://geizhals.de/lg-oled-g39la-v127135.html
    url = "https://geizhals.de/lg-oled-g39la-v127135.html"
    max_reviews = 50
    scrape_reviews(url, max_reviews, path_to_db)

    # Ensure full DataFrame display without truncation
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_colwidth', 20)
    pd.set_option('display.width', None)

    print(read_database(path_to_db))
