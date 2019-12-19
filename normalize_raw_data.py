import ast
import pandas as pd
import pickle
import re
import os 
from datetime import date

def string_to_list(string):
    x = ast.literal_eval(string)
    item_list = [n.strip() for n in x]
    return item_list

def extract_cateogry(row, flg):
    # 0: middle category
    # 2: large category
    # 4: small category
    genre_list = string_to_list(row)
    try:
        return genre_list[flg]
    except IndexError:
        return 'N/A'

def extract_item_info(row, flg):
    if 'Odd' not in row:
        info_list = string_to_list(row)
        try:
            return info_list[flg]
        except IndexError:
            return 'N/A'
    else:
        return 'N/A'

def extract_info(row, target_info):
    res = ''
    item_info_list = string_to_list(row)
    for item_info in item_info_list:
        if target_info in item_info:
            res = item_info.replace(target_info, '').strip()
            res = res.replace('：', '').strip()
            res = res.replace(':', '').strip()

        else:
            pass
    return res


def trim_image_param(row):
    res = []
    if ('non valid' in row) or ('processing error' in row):
        return 'N/A'
    else:
        image_list = string_to_list(row)
        for image in image_list:
            file_extension = re.search(r'[a-zA-Z]+$', image).group()
            path = re.sub('\_.*', '', image)
            image_path = path + file_extension
            if image_path not in ['https://images-na.ssl-images-amazon.com/images/G/01/x-locale/common/transparent-pixel.gif','https://m.media-amazon.com/images/G/09/HomeCustomProduct/360png']:
                res.append(image_path)
        return res


def unpickle_object(file_name):
    with open(file_name, 'rb') as f:
        return pickle.load(f)

def download_scraped_data():
    os.system('gsutil -m cp -r gs://am-scraped/bk/am-scraper-1-df_main.pickle ./')
    os.system('gsutil -m cp -r gs://am-scraped/bk/am-scraper-2-df_main.pickle ./')
    os.system('gsutil -m cp -r gs://am-scraped/bk/am-scraper-3-df_main.pickle ./')
    os.system('gsutil -m cp -r gs://am-scraped/bk/am-scraper-4-df_main.pickle ./')
    os.system('gsutil -m cp -r gs://am-scraped/bk/am-scraper-5-df_main.pickle ./')
    os.system('gsutil -m cp -r gs://am-scraped/bk/am-scraper-6-df_main.pickle ./')
    os.system('gsutil -m cp -r gs://am-scraped/bk/am-scraper-7-df_main.pickle ./')

if __name__ == "__main__":
    pd.set_option('display.max_colwidth', -1)
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)
    today = str(date.today())
    download_scraped_data()
    df_1 = unpickle_object('./am-scraper-1-df_main.pickle')
    df_2 = unpickle_object('./am-scraper-2-df_main.pickle')
    df_3 = unpickle_object('./am-scraper-3-df_main.pickle')
    df_4 = unpickle_object('./am-scraper-4-df_main.pickle')
    df_5 = unpickle_object('./am-scraper-5-df_main.pickle')
    df_6 = unpickle_object('./am-scraper-6-df_main.pickle')
    df_7 = unpickle_object('./am-scraper-7-df_main.pickle')
    df = df_1.append([df_2, df_3, df_4, df_5, df_6, df_7])
    df.to_csv('./df_{today}.csv'.format(today=today), index=None)
    df = pd.read_csv('./df_{today}.csv'.format(today=today))
    df_item_master = pd.DataFrame()
    df_item_master['page_link'] = df.page_link
    df_item_master['asin'] = df.item_info.apply(
        lambda x: extract_info(x, 'ASIN'))
    df_item_master['alt_images'] = df.alt_images.apply(
        lambda x: trim_image_param(x))
    df_item_master['feature_images'] = df.feature_images.apply(
        lambda x: trim_image_param(x))
    df_item_master['genre'] = df.item_genre.apply(lambda x: string_to_list(x))
    df_item_master['item_price_text'] = df.item_price
    df_item_master['genre_small'] = df.item_genre.apply(lambda x: extract_cateogry(x, 4))
    df_item_master['item_brand'] = df.item_brand.apply(lambda x: extract_item_info(x, 0))
    df_item_master['item_name'] = df.item_brand.apply(lambda x: extract_item_info(x, 1))
    df_item_master = df_item_master[df_item_master.alt_images.apply(len) != 0]
    df_item_master.to_csv('./df_{today}_item_master.csv'.format(today=today), index=None)
    
    df_tops = df_item_master[df_item_master.genre_small == 'トップス']
    df_one_piece_dress = df_item_master[df_item_master.genre_small == 'ワンピース・ドレス']
    df_skirts = df_item_master[df_item_master.genre_small == 'スカート']
    df_coats_jackets = df_item_master[df_item_master.genre_small == 'コート・ジャケット']
    df_pants = df_item_master[df_item_master.genre_small == 'パンツ']
    
    df_image_tops = df_tops[['alt_images', 'asin', 'page_link']].explode('alt_images')
    df_image_one_piece_dress = df_one_piece_dress[['alt_images', 'asin', 'page_link']].explode('alt_images')
    df_image_skirts = df_skirts[['alt_images', 'asin', 'page_link']].explode('alt_images')
    df_image_coats_jackets = df_coats_jackets[['alt_images', 'asin', 'page_link']].explode('alt_images')
    df_image_pants = df_pants[['alt_images', 'asin', 'page_link']].explode('alt_images')

    df_tops.to_csv('./df_{today}_tops.csv'.format(today=today), index=None)
    df_one_piece_dress.to_csv('./df_{today}_one_piece_dress.csv'.format(today=today), index=None)
    df_skirts.to_csv('./df_{today}_skirts.csv'.format(today=today), index=None)
    df_coats_jackets.to_csv('./df_{today}_coats_jackets.csv'.format(today=today), index=None)
    df_pants.to_csv('./df_{today}_pants.csv'.format(today=today), index=None)    
    df_image_tops.to_csv('./df_{today}_image_tops.csv'.format(today=today), index=None)
    df_image_one_piece_dress.to_csv('./df_{today}_image_one_piece_dress.csv'.format(today=today), index=None)
    df_image_skirts.to_csv('./df_{today}_image_skirts.csv'.format(today=today), index=None)
    df_image_coats_jackets.to_csv('./df_{today}_image_coats_jackets.csv'.format(today=today), index=None)
    df_image_pants.to_csv('./df_{today}_image_pants.csv'.format(today=today), index=None)

    os.system('gsutil mv ./df_{today}_tops.csv gs://am-scraped/data/item/'.format(today=today))
    os.system('gsutil mv ./df_{today}_one_piece_dress.csv gs://am-scraped/data/item/'.format(today=today))
    os.system('gsutil mv ./df_{today}_skirts.csv gs://am-scraped/data/item/'.format(today=today))
    os.system('gsutil mv ./df_{today}_coats_jackets.csv gs://am-scraped/data/item/'.format(today=today))
    os.system('gsutil mv ./df_{today}_pants.csv gs://am-scraped/data/item/'.format(today=today))
    os.system('gsutil mv ./df_{today}_image_tops.csv gs://am-scraped/data/image/'.format(today=today))
    os.system('gsutil mv ./df_{today}_image_one_piece_dress.csv gs://am-scraped/data/image/'.format(today=today))
    os.system('gsutil mv ./df_{today}_image_skirts.csv gs://am-scraped/data/image/'.format(today=today))
    os.system('gsutil mv ./df_{today}_image_coats_jackets.csv gs://am-scraped/data/image/'.format(today=today))
    os.system('gsutil mv ./df_{today}_image_pants.csv gs://am-scraped/data/image/'.format(today=today))
