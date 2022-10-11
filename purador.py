import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import ast

def puradoor_ingre(product_url):
    def extract_ingre(soup):
        try:
            divs = soup.find_all('div', {"class": 'ec-description-container'})
            for div in divs:
                if div.find('h3', text="Ingredients") is not None:

                    all_ingre = ""
                    ingredients_heading = div.find('h3', text="Ingredients")
                    ingredients = ingredients_heading.find_next('p')

                    while ingredients is not None:
                        if ingredients.find('strong') is not None:
                            all_ingre += ';' + ingredients.get_text(strip=True).strip()
                        else:
                            try:
                                ingredients.find('br').replace_with(bs(", ", 'html.parser'))
                            except:
                                pass
                            all_ingre += ingredients.get_text(strip=True).title()\
                        .replace("*Certified Organic Ingredients", "").replace("(Packaging May Vary)", "")\
                        .replace("*Certified Organic", "")\
                        .replace('**Non-GMO', "") \
                        .replace('**Non-Gmo', "") \
                        .replace("Ingredient", "")\
                        .strip()


                        ingredients = ingredients.find_next('p')
                        if ingredients.find_next('p') is not None and ingredients.find_next(
                            'p').parent == ingredients_heading.parent:
                            continue
                        else:
                            break

                    if all_ingre[0] == ';':
                        all_ingre = all_ingre[1:]

                    return ' '.join(all_ingre.split())
            return 'N/A'
        except:
            return 'N/A'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36'}  # Defining the User-Agent to fake browser
    response = requests.get(product_url, headers=headers)  # Requesting the product page using product url and headers
    soup = bs(response.content,
              'html.parser')  # Creating the soup using the beautifulsoup library and the response received from the above request
    return [product_url, extract_ingre(soup), 'N/A']

# print(puradoor_ingre("https://purador.com/products/foase-under-eye-patches-with-24k-gold-20pk"))
# print(puradoor_ingre("https://purador.com/collections/haircare/products/advanced-therapy-conditioner"))
# print(puradoor_ingre("https://purador.com/products/advanced-therapy-conditioner"))
# print(puradoor_ingre("https://purador.com/collections/skincare/products/1-7oz-golden-glow-face-cream"))
# print(puradoor_ingre("https://purador.com/collections/skincare/products/30ml-face-serum-collagen-whitening-moisturizer"))
# print(puradoor_ingre("https://purador.com/collections/skincare/products/25-vitamin-c-serum-with-derma-roller"))
# print(puradoor_ingre("https://purador.com/collections/aromatherapy/products/10ml-essential-oil-set-usda-organic-100-pure-natural-therapeutic-grade"))
# print(puradoor_ingre("https://purador.com/collections/haircare/products/16oz-apple-cider-vinegar-thin2thick-shampoo-and-conditioner-set"))
# print(puradoor_ingre("https://purador.com/collections/aromatherapy/products/16oz-organic-sweet-almond-oil"))
# print(puradoor_ingre("https://purador.com/collections/aromatherapy/products/organic-sunflower-seed-oil-16-fl-oz"))
print(puradoor_ingre("https://purador.com/collections/all-products/products/hair-thinning-therapy-system-original-scent"))
print(puradoor_ingre("https://purador.com/collections/all-products/products/hair-thinning-therapy-energizing-scalp-serum"))
