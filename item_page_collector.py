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


def collect_item_pages(driver, current_url, container_num):
    prev_url = ''
    item_links = []
    while current_url != prev_url:
        try:
            item_links = unpickle_object(
                '/home/koki_hikichi/am_scraper/item_links.pickle')
            current_url = unpickle_object(
                '/home/koki_hikichi/am_scraper/current_url.pickle')
        except FileNotFoundError:
            print('file not found')
        print('current_url:{}'.format(current_url))
        driver.get(current_url)
        sleep(2)
        try:
            res = driver.find_element_by_id("mainResults")
            item_elems = res.find_elements_by_tag_name("li")
            for item_elem in item_elems:
                item_link = item_elem.find_elements_by_tag_name(
                    "a")[1].get_attribute("href")
                if 'https://www.amazon.co.jp/' in item_link:
                    item_links.append(item_link)
            driver.find_element_by_id("pagnNextString").click()
            print('success 1')
        except NoSuchElementException:
            res = driver.find_element_by_xpath(
                "//div[@class='s-result-list s-search-results sg-row']")
            item_elems = res.find_elements_by_tag_name("h2")
            for item_elem in item_elems:
                item_link = item_elem.find_element_by_xpath(
                    "a[@class='a-link-normal a-text-normal']").get_attribute("href")
                item_links.append(item_link)
            driver.find_element_by_class_name("a-last").click()
            print('success 2')
        tmp_url = current_url
        current_url = driver.current_url
        prev_url = tmp_url
        pickle_object(
            '/home/koki_hikichi/am_scraper/item_links.pickle', item_links)
        pickle_object(
            '/home/koki_hikichi/am_scraper/current_url.pickle', current_url)

        output_item_links = 'am-scraper-{instance_name}-item_links.pickle'.format(
            instance_name=str(args.container_num))
        output_current_url = 'am-scraper-{instance_name}-current_url.pickle'.format(
            instance_name=str(args.container_num))

        os.system(
            'gsutil cp /home/koki_hikichi/am_scraper/{output_item_links} gs://am-scraped/bk/{file_name}'.format(file_name=outputfile_name))
        os.system(
            'gsutil cp /home/koki_hikichi/am_scraper/df_main.pickle gs://am-scraped/bk/{file_name}'.format(file_name=outputfile_name))


if __name__ == "__main__":
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(
        options=options, executable_path='./chromedriver')
    parser = argparse.ArgumentParser()
    parser.add_argument('--url')
    parser.add_argument('container_num')
    args = parser.parse_args()
    if args.url:
        current_url = args.url
    else:
        current_url = unpickle_object('current_url.pickle')
    collect_item_pages(driver, current_url, args.container_num)
