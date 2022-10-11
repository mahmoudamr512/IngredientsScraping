import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import ast

def kreyolessence_ingre(product_url):
    def extract_ingre(soup):
        try:
            ingredients = ""
            ingre = soup.find('div', {'id': 'tab-3'})
            for p in ingre.find_all('p'):
                if "single hero ingre" not in p.text.lower() and "processed in a facility" not in p.text.lower()\
                        and "warning:" not in p.text.lower() and "certified organic materials" not in p.text.lower() and \
                        "LOVE WHAT" not in p.text.upper()\
                        and "natural ingredients" not in p.text.lower()\
                        and "promises to provide you" not in p.text.lower()\
                        and "INGREDIENTS MARKED WITH AN ASTERISK" not in p.text.upper():
                    if "set includes our" in p.text.lower():
                        ingredients = "N/A"
                        break
                    if p.find('strong') is not None and p.text.strip() != "":
                        ingredients += ";" + p.text.title() + ":"
                    else:
                        ingredients += p.text.title().replace(';', ',')
            if ingredients[0] == ";":
                ingredients = ingredients[1:]

            if len(ingredients) < 3:
                ingredients = "N/A"
            return ingredients.replace('\xa0', '').replace("*Certified Organic Ingredient", "").strip()
        except:
            return 'N/A'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36'}  # Defining the User-Agent to fake browser
    response = requests.get(product_url, headers=headers)  # Requesting the product page using product url and headers
    soup = bs(response.content,
              'html.parser')  # Creating the soup using the beautifulsoup library and the response received from the above request
    return [product_url, extract_ingre(soup), 'N/A']

# print(kreyolessence_ingre("https://kreyolessence.com/products/haitian-black-castor-oil-original-2oz"))
# print(kreyolessence_ingre("https://kreyolessence.com/collections/haitian-black-castor-oil/products/haitian-black-castor-oil-original-3-4oz-super-size"))
# print(kreyolessence_ingre("https://kreyolessence.com/collections/skin-care/products/haitian-moringa-oil-mist-glow-toner-2oz"))
# print(kreyolessence_ingre("https://kreyolessence.com/collections/skin-care/products/new-haitian-moringa-hair-skin-nails-vitamins-4oz-pineapple-rhum-punch"))
# print(kreyolessence_ingre("https://kreyolessence.com/collections/superfood-moringa-styling-products/products/haitian-moringa-oil-mist-me-please-moisture-spritz-8oz"))
# print(kreyolessence_ingre("https://kreyolessence.com/collections/skin-care/products/moringa-skincare-4-piece"))
# print(kreyolessence_ingre("https://kreyolessence.com/collections/superfood-moringa-styling-products/products/curly-girl"))
# print(kreyolessence_ingre("https://kreyolessence.com/collections/superfood-moringa-styling-products/products/straight-laced-hair-kit"))
# print(kreyolessence_ingre("https://kreyolessence.com/collections/vitamins-supplements/products/new-haitian-moringa-hair-skin-nails-vitamins-4oz-original-flavor"))
# print(kreyolessence_ingre("https://kreyolessence.com/products/haitian-mango-br-b-loris-dream-body-set-b-br-br-3-piece-set-br"))
# print(kreyolessence_ingre("https://kreyolessence.com/products/haitian-black-castor-oil-shark-tank-duo-2oz"))
# print(kreyolessence_ingre("https://kreyolessence.com/products/barbaras-lavender-body-trio"))
# print(kreyolessence_ingre("https://kreyolessence.com/collections/haitian-black-castor-oil/products/haitian-black-castor-oil-trio-bundle"))
# print(kreyolessence_ingre("https://kreyolessence.com/collections/haitian-black-castor-oil/products/haitian-black-castor-oil-organic-rosemary-peppermint-2oz"))
print(kreyolessence_ingre("https://kreyolessence.com/collections/skin-care/products/moringa-skincare-4-piece"))