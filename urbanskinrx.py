import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import ast

def urbanskinrx_ingre(product_url):

    def extract_ingredients(box) -> str:
        if (len(box) == 1):
            box = box[0]

        try:
            box.find('strong').extract()

            try:
                box.find('br').extract()
            except:
                pass

            products = box.find_all_next('strong')
            for i in range(1, len(products)):
                products[i].replace_with(";" + products[i].text)
            return box.text.replace(' - ', ': ').strip()
        except Exception as ex:
            pass

        try:
            text = box[0].text.replace(";Full Ingredient List:;", '')
            for i in range(1, len(box)):
                text += box[i].replace_with(";" + box[i].text).text
            return text.replace(' - ', ': ')
        except:
            pass


    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36'}  # Defining the User-Agent to fake browser
    response = requests.get(product_url, headers=headers)  # Requesting the product page using product url and headers
    soup = bs(response.content,
              'html.parser')  # Creating the soup using the beautifulsoup library and the response received from the above request

    ingredient_box = soup.find('div', {'class': 'ingredient-chart-desktop'}).find_all('p') # Get both ingredient boxes for Full and Key ingredients.

    key_ingredients = full_ingredients = 'N/A'

    key_ingredients = extract_ingredients(ingredient_box[0])

    full_ingredients = extract_ingredients(ingredient_box[1:])

    return [product_url, full_ingredients, key_ingredients]

print(urbanskinrx_ingre("https://urbanskinrx.com/collections/skincare-kits-value-sets/products/even-tone-value-kit"))
# print(urbanskinrx_ingre("https://urbanskinrx.com/collections/shop-all/products/clarify-value-kit"))