import ast
import pandas as pd
import pickle
import re


def string_to_list(string):
    x = ast.literal_eval(string)
    item_list = [n.strip() for n in x]
    return item_list


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
    image_list = string_to_list(row)
    for image in image_list:
        file_extension = re.search(r'[a-zA-Z]+$', image).group()
        path = re.sub('\_.*', '', image)
        image_path = path + file_extension
        res.append(image_path)
    return ','.join(res)


def unpickle_object(file_name):
    with open(file_name, 'rb') as f:
        return pickle.load(f)


if __name__ == "__main__":
    df = unpickle_object('./df_main.pickle')
    df_item_master = pd.DataFrame()

    pd.set_option('display.max_colwidth', -1)
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    df_item_master['page_link'] = df.page_link
    df_item_master['asin'] = df.item_info.apply(
        lambda x: extract_info(x, 'ASIN'))
    df_item_master['alt_images'] = df.alt_images.apply(
        lambda x: trim_image_param(x))
    df_item_master['feature_images'] = df.feature_images.apply(
        lambda x: trim_image_param(x))
    df_item_master['genre'] = df.item_genre.apply(lambda x: string_to_list(x))
    df_item_master['item_price_text'] = df.item_price
    df_item_master.to_csv('./item_master.csv', index=None)
