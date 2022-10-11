import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import ast

def dashingdiva_ingre(product_url):
    def extract_ingredients(soup):
        try:
            paragraphs = soup.find('div', {'data-accordion-block': 'ingredients'}).find_all('p')

            full_ingredients = paragraphs[0].text.title()

            for i in range(1, len(paragraphs)):
                full_ingredients += ";" + paragraphs[i].text.title()

            return full_ingredients
        except:
            return 'N/A'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36'}  # Defining the User-Agent to fake browser
    response = requests.get(product_url, headers=headers)  # Requesting the product page using product url and headers
    soup = bs(response.content,
              'html.parser')  # Creating the soup using the beautifulsoup library and the response received from the above request

    return [product_url, extract_ingredients(soup), 'N/A']

print(dashingdiva_ingre("https://dashingdiva.com/collections/magic-press/products/amber-ale"))
print(dashingdiva_ingre("https://dashingdiva.com/collections/the-pedi-shop/products/twinkle-toes"))
print(dashingdiva_ingre("https://dashingdiva.com/collections/shop-all-manis/products/coconut-milk-short"))
print(dashingdiva_ingre("https://dashingdiva.com/collections/shop-all-manis/products/gloss-gel-strips-glitter-glamour"))
print(dashingdiva_ingre("https://dashingdiva.com/products/gilded-pansy"))
print(dashingdiva_ingre("https://dashingdiva.com/products/solar-sepia"))
print(dashingdiva_ingre("https://dashingdiva.com/collections/red-therapy/products/red-therapy-for-gloss"))
print(dashingdiva_ingre("https://dashingdiva.com/products/spell-book-secrets"))
print(dashingdiva_ingre("https://dashingdiva.com/products/skeleton-dance"))