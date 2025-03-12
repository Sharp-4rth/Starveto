from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.tokenize import sent_tokenize


def setup_driver(postcode):
    postcode = 'L1 4TW'
    url = f'https://deliveroo.co.uk/restaurants/london/westminster?postcode={postcode}&collection=all-restaurants'
    chrome_driver_path = Service(r'/Users/leonidas/chromedriver-mac-arm64/chromedriver')
    initial_load_time = 0.1
    scroll_pause_time = 0.0001

    driver = webdriver.Chrome(service=chrome_driver_path)
    driver.get(url)
    time.sleep(initial_load_time)
    screen_height = driver.execute_script('return window.screen.height;')

    return driver, screen_height, scroll_pause_time


def create_soup(driver, screen_height, scroll_pause_time):
    cookie_button = WebDriverWait(driver, 1).until(
        EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
    )
    cookie_button.click()

    time.sleep(1)
    ok_button = WebDriverWait(driver, 1).until(
        EC.element_to_be_clickable((By.XPATH, "//button[span[text()='OK']]"))
    )
    ok_button.click()

    scroll_count = 2  # Set to 1 for a single scroll, or 2 for twice
    for i in range(scroll_count):
        driver.execute_script(f"window.scrollTo(0, {screen_height} * {i});")
        time.sleep(scroll_pause_time)  # Allow time for content to load

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    return soup


def extract_class(soup):
    a_tag_class = 'HomeFeedUICard-3e299003014c14f9'

    # soup = create_soup()
    restaurants_html_obj = soup.find_all(class_ = a_tag_class)

    return restaurants_html_obj


def clean_data(restaurants_html_obj):
    names_times = []
    for restaurant in restaurants_html_obj:
        if len(names_times) == 10:
            break
        else:
            details = restaurant.get("aria-label")  # Extracts name & details
            name = details.split(".")[0].strip()  # Extracts name
            time_range = details.split(".")[3].strip()
            t = re.findall(r'\d+', time_range)
            t = list(map(int, t))
            average_time = float(np.mean(t))
            row = {name: average_time}
            names_times.append(row)

    sorted_nts = sorted(names_times, key=lambda d: list(d.values())[0])
    print(sorted_nts)

    return sorted_nts


def gather_data(postcode):
    driver, screen_height, scroll_pause_time = setup_driver(postcode)
    soup = create_soup(driver, screen_height, scroll_pause_time)
    restaurants_html_obj = extract_class(soup)
    restaurant_times = clean_data(restaurants_html_obj)

    return restaurant_times

if __name__ == "__main__":
    gather_data()