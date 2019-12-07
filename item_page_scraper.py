from time import sleep
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import pickle
import os
import datetime
import pandas as pd
import random

def pickle_object(file_name, obj):
    with open(file_name, 'wb') as f:
        pickle.dump(obj, f)


def unpickle_object(file_name):
    with open(file_name, 'rb') as f:
        return pickle.load(f)


def get_item_genre():
    global DRIVER
    genre_list = []
    try:
        genre_elem = DRIVER.find_element_by_id("showing-breadcrumbs_div")
        genre_content_elems = genre_elem.find_element_by_tag_name(
            "ul").find_elements_by_tag_name("li")
        for genre_content_elem in genre_content_elems:
            genre_list.append(genre_content_elem.text)
    except NoSuchElementException:
        genre_list.append('Odd item genre page')
    return genre_list


def get_item_info_2():
    global DRIVER
    info_list = []
    try:
        detail_elem = DRIVER.find_element_by_id("prodDetails")
        detail_content_elems = detail_elem.find_elements_by_tag_name('tr')
        for detail_content_elem in detail_content_elems:
            info_list.append(detail_content_elem.text.split())
    except NoSuchElementException:
        info_list.append('Odd item info page')
    return info_list


def get_item_info():
    global DRIVER
    info_list = []
    try:
        detail_elem = DRIVER.find_element_by_id("detail_bullets_id")
        detail_content_elems = detail_elem.find_element_by_class_name(
            "content").find_elements_by_tag_name("li")
        for detail_content_elem in detail_content_elems:
            info_list.append(detail_content_elem.text)
    except NoSuchElementException:
        info_list.append('Odd item info page')
    return info_list


def get_item_brand():
    global DRIVER
    try:
        brand_elem = DRIVER.find_element_by_id("titleBlock")
        brand_text = brand_elem.find_element_by_id(
            "bylineInfo_feature_div").text
        item_text = brand_elem.find_element_by_id("title_feature_div").text
        brand_link = brand_elem.find_element_by_tag_name(
            "a").get_attribute("href")
    except NoSuchElementException:
        return 'Odd item item brand'
    return [brand_text, item_text, brand_link]


def get_item_review():
    global DRIVER
    try:
        review_rate = DRIVER.find_element_by_id(
            "acrPopover").get_attribute("title")
        review_number = DRIVER.find_element_by_id("acrCustomerReviewText").text
    except NoSuchElementException:
        return 'Odd item review'
    return [review_rate, review_number]


def get_item_price():
    try:
        price_info = DRIVER.find_element_by_id("price").text
    except NoSuchElementException:
        price_info = 'Odd price info'
    return price_info


def get_item_text():
    item_text_list = []
    try:
        item_text = DRIVER.find_element_by_id("feature-bullets")
        item_text_elems = item_text.find_element_by_tag_name(
            "ul").find_elements_by_tag_name("li")
        for item_text_elem in item_text_elems:
            item_text_list.append(item_text_elem.text)
    except NoSuchElementException:
        pass
    return item_text_list


def get_images(div_id):
    global DRIVER
    img_list = []
    try:
        img_elem_box = DRIVER.find_element_by_id(div_id)
        img_elems = img_elem_box.find_elements_by_tag_name("li")
        for img_elem in img_elems:
            try:
                img_link = img_elem.find_element_by_tag_name("img").get_attribute("src")
                if 'https://images-na.ssl-images-amazon.com/images/G/09/HomeCustomProduct/360_icon' in img_link:
                    pass
                else:
                    img_list.append(img_elem.find_element_by_tag_name("img").get_attribute("src"))
            except NoSuchElementException:
                pass
    except NoSuchElementException:
        pass
    return img_list

def request_reject_check():
    global DRIVER
    res = 0
    try:
        DRIVER.find_element_by_id('altImages')
    except NoSuchElementException:
        res = 1
        td_elems = DRIVER.find_elements_by_tag_name('td')
        for td_elem in td_elems:
            if '有効なページではありません' in td_elem.text:
                print('有効なページではありません')
                res = 0
            if 'お客様のリクエストの処理中にエラーが発生しました。' in td_elem.text:
                print('お客様のリクエストの処理中にエラーが発生しました。')
                res = 0
    if res == 1:
        print('Rejected')        
    return res

def update_df_main(page_link):
    global DF_MAIN
    global DRIVER
    global STOP_SIG

    print(page_link)
    # create an item page record
    df_tmp = pd.DataFrame([page_link], columns=['page_link'])

    # get images
    DRIVER.get(item_link)
    sleep(random.randint(2,5))
    STOP_SIG = request_reject_check()

    # sleep until passing the reject check
    while STOP_SIG == 1:
        print(DRIVER.page_source)
        file_name = datetime.datetime.now().isoformat()
        os.system('gsutil cp df_main.pickle gs://am-scraped/bk/{file_name}.pickle'.format(file_name=file_name))
        sleep(60*40)
        STOP_SIG = request_reject_check()
        
    alt_image_list = str(get_images("altImages"))
    feature_image_list = str(get_images("twister_feature_div"))
    # get item info
    info_list = str(get_item_info())
    info_list_2 = str(get_item_info_2())
    # get item brand
    item_brand = str(get_item_brand())
    # get item review
    item_review = str(get_item_review())
    # get item price
    item_price = str(get_item_price())
    # get item text
    item_text = str(get_item_text())
    # get item genre
    item_genre = str(get_item_genre())

    df_tmp['alt_images'] = alt_image_list
    df_tmp['feature_images'] = feature_image_list
    df_tmp['item_info'] = info_list
    df_tmp['item_info_2'] = info_list_2
    df_tmp['item_brand'] = item_brand
    df_tmp['item_review'] = item_review
    df_tmp['item_price'] = item_price
    df_tmp['item_text'] = item_text
    df_tmp['item_genre'] = item_genre
    DF_MAIN = DF_MAIN.append(df_tmp)
    pickle_object('df_main.pickle', DF_MAIN)
    

try:
    DF_MAIN = unpickle_object('df_main.pickle')
    EXISTING_LINKS = list(DF_MAIN.page_link)
except FileNotFoundError:
    print('file not found')
    DF_MAIN = pd.DataFrame()
    EXISTING_LINKS = []

pd.set_option('display.max_colwidth', -1)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

STOP_SIG = 0
OPTIONS = Options()
OPTIONS.add_argument('--headless')
DRIVER = webdriver.Chrome(options=OPTIONS, executable_path='./chromedriver')

if __name__ == "__main__":
    global EXISTING_LINKS
    global STOP_SIG
    global DRIVER

    item_links = unpickle_object('item_links.pickle')
    for item_link in item_links:
        if item_link in EXISTING_LINKS:
            pass
        else:
            update_df_main(item_link)
