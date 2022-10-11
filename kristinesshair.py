import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import ast

def kristinesshair_ingre(product_url) -> list:

    def extract_ingredients(soup) -> str:
        for span in soup.find_all('span', {'class': 'product-accordion__title'}):
            if "ingredients" in span.text.lower():
                inner_div = span.parent.parent.find('div', {'class':'product-accordion__content'})

                strings_to_check = ['please note', 'warning', 'important']

                paragraphs = inner_div.find_all('p')

                ingredients = paragraphs[0].text.title().replace('\n', '').replace('\xa0', '')
                for i in range(1, len(paragraphs)):
                    if not any(sub in paragraphs[i].text.lower() for sub in strings_to_check) and not paragraphs[i].text.strip() != '':
                        ingredients += ";" + paragraphs[i].text.title().replace('\n', '').replace('\xa0', '')

                return ingredients

        return 'N/A'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36'}  # Defining the User-Agent to fake browser
    response = requests.get(product_url, headers=headers)  # Requesting the product page using product url and headers
    soup = bs(response.content,
              'html.parser')  # Creating the soup using the beautifulsoup library and the response received from the above request

    return [product_url, extract_ingredients(soup), 'N/A']

print(kristinesshair_ingre("https://www.kristinesshair.com/products/purple-shampoo-2"))
print(kristinesshair_ingre("https://www.kristinesshair.com/products/tone-it-down-set"))
print(kristinesshair_ingre("https://www.kristinesshair.com/products/winter-wheat"))
print(kristinesshair_ingre("https://www.kristinesshair.com/products/purple-shampoo"))
print(kristinesshair_ingre("https://www.kristinesshair.com/products/air-dry-mousse"))
print(kristinesshair_ingre("https://www.kristinesshair.com/products/style-reviving-dry-shampoo"))
print(kristinesshair_ingre("https://www.kristinesshair.com/products/tone-it-down-set"))

