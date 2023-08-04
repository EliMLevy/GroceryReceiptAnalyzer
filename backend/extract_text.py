from PIL import Image
import pytesseract
import pandas as pd
import numpy as np
import json
import re

pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def run_extraction(store_name, food_img_path, prices_img_path):

    foods_img = np.array(Image.open(food_img_path))
    foods_img_text = pytesseract.image_to_string(foods_img)

    print(foods_img_text)

    pricesImg = np.array(Image.open(prices_img_path))
    prices_img_text = pytesseract.image_to_string(pricesImg, config="--psm 6 digits")

    print(prices_img_text)


    prices_formatted = prices_img_text.split("\n")
    foods_formatted = foods_img_text.split("\n")

    prices_formatted = list(filter(lambda x: len(x) > 0, prices_formatted))
    foods_formatted = list(filter(lambda x: len(x) > 0, foods_formatted))


    print(len(prices_formatted), len(foods_formatted))

    num_prices = len(prices_formatted)
    num_food = len(foods_formatted)

    if num_prices < num_food:
        for i in range(num_food - num_prices):
            prices_formatted.append('0')
    elif num_food < num_prices:
        for i in range(num_prices - num_food):
            foods_formatted.append("-")

    food_mapping_file = open("./mappings.json", "r")
    food_mapping = json.loads(food_mapping_file.read())

    df = pd.DataFrame()
    df["food"] = [food_mapping[mapped_food] if mapped_food in food_mapping else mapped_food for mapped_food in foods_formatted]
    df["price"] = [re.sub(r'\.+', '.', price) for price in prices_formatted]
    df["store"] = [store_name for _ in foods_formatted]

    df.to_csv("output.csv", index=False)
    return df
