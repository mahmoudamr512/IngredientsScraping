import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import ast


def bondisands_ingre(product_url):

    def extract_ingredients(soup):
        try:
            ingredients_tab = soup.find('div', {'data-title': 'Ingredients'})
            ingredients_paragraph = str(ingredients_tab.find('p')).split('<br/>')
            text = bs(ingredients_paragraph[0], 'html.parser').text.title()
            if "please refer to" not in text.lower():
                return text
            else:
                return 'N/A'
        except:
            return 'N/A'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36'}  # Defining the User-Agent to fake browser
    response = requests.get(product_url, headers=headers)  # Requesting the product page using product url and headers
    soup = bs(response.content,
              'html.parser')  # Creating the soup using the beautifulsoup library and the response received from the above request
    return [product_url, extract_ingredients(soup), 'N/A']

print(bondisands_ingre("https://bondisands.com/products/get-up-glow-bundle"))
print(bondisands_ingre("https://bondisands.com/products/pure-self-tanning-foaming-water-dark"))
print(bondisands_ingre("https://bondisands.com/products/self-tanning-foam-dark"))
print(bondisands_ingre("https://bondisands.com/products/liquid-gold-self-tanning-foam"))
print(bondisands_ingre("https://bondisands.com/products/coconut-body-wash"))
print(bondisands_ingre("https://bondisands.com/products/summer-fruits-body-scrub"))
print(bondisands_ingre("https://bondisands.com/products/glo-finishing-gloss"))
print(bondisands_ingre("https://bondisands.com/products/tropical-rum-body-moisturiser-200ml"))