import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import pickle
from time import sleep
import argparse

def pickle_object(file_name, obj):
    with open(file_name, 'wb') as f:
        pickle.dump(obj, f)
        
def unpickle_object(file_name):
    with open(file_name, 'rb') as f:
        return pickle.load(f)

def collect_item_pages(driver, current_url):
    prev_url = ''
    item_links = []
    while current_url != prev_url:
        try:
            item_links = unpickle_object('item_links.pickle')
            current_url = unpickle_object('current_url.pickle')
        except FileNotFoundError:
            print('file not found')
        print('current_url:{}'.format(current_url))
        driver.get(current_url)
        sleep(2)        
        try:
            res = driver.find_element_by_id("mainResults")
            item_elems = res.find_elements_by_tag_name("li")
            for item_elem in item_elems:
                item_link = item_elem.find_elements_by_tag_name("a")[1].get_attribute("href")
                if 'https://www.amazon.co.jp/' in item_link:
                    item_links.append(item_link)
            driver.find_element_by_id("pagnNextString").click()
            print('success 1')
        except NoSuchElementException:
            res = driver.find_element_by_xpath("//div[@class='s-result-list s-search-results sg-row']")
            item_elems = res.find_elements_by_tag_name("h2")
            for item_elem in item_elems:
                item_link = item_elem.find_element_by_xpath("a[@class='a-link-normal a-text-normal']").get_attribute("href")
                item_links.append(item_link)
            driver.find_element_by_class_name("a-last").click()
            print('success 2')
        tmp_url = current_url
        current_url = driver.current_url
        prev_url = tmp_url
        pickle_object('item_links.pickle', item_links)
        pickle_object('current_url.pickle', current_url)

if __name__ == "__main__":
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options, executable_path='./chromedriver')
    parser = argparse.ArgumentParser()
    parser.add_argument('--url')
    args = parser.parse_args()
    if args.url:
        current_url = args.url
    else:
        current_url = unpickle_object('current_url.pickle')
    collect_item_pages(driver, current_url)
