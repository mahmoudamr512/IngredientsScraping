import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import ast

def deborahlippmann_ingre(product_url):

    def extract_ingredients(soup):
        try:
            ingredients_divs = soup.find_all('div', class_='ingredients')

            if len(ingredients_divs) <= 1:
                ingredients_divs = soup.find_all('p', class_='ingredients')

            ingredients = ""
            for div in ingredients_divs:
                if "ingredients" in div['class'] and len(div['class']) == 1:
                    try:
                        ingredients = div.find('div').text
                        break
                    except:
                        ingredients = div.text
                        break

            ingredients = ingredients.replace(" .", ",").split(', ')
            for i in range(1, len(ingredients)):
                if ":" in ingredients[i]:
                    ingredients[i] = ";" + ingredients[i]

            if len(ingredients) <= 1:
                return 'N/A'
            else:
                return ", ".join(ingredients).replace(", ;", ";").title().replace("Ingredients/Ingrédients:", "").strip()[:-1]
        except Exception as ex:
            print(ex)
            return 'N/A'



    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36'}  # Defining the User-Agent to fake browser
    response = requests.get(product_url, headers=headers)  # Requesting the product page using product url and headers
    soup = bs(response.content,
              'html.parser')  # Creating the soup using the beautifulsoup library and the response received from the above request

    return [product_url, extract_ingredients(soup), 'N/A']

print(deborahlippmann_ingre("https://deborahlippmann.com/collections/lip-gloss/products/hydra-cushion-balmy-lip-gloss?variant=34750719099018"))
print(deborahlippmann_ingre("https://deborahlippmann.com/collections/lip-gloss/products/lip-nail-duet?variant=34758535774346"))
print(deborahlippmann_ingre("https://deborahlippmann.com/collections/lip-gloss/products/hydra-cushion-balmy-lip-gloss?variant=34750720901258"))
print(deborahlippmann_ingre("https://deborahlippmann.com/collections/skincare-hands/products/its-a-miracle-pen?variant=40723501875338"))
print(deborahlippmann_ingre("https://deborahlippmann.com/collections/sets/products/im-that-girl-nail-polish-trio?variant=42211568746634"))
print(deborahlippmann_ingre("https://deborahlippmann.com/collections/cuticle-care/products/cuticle-pusher-1?variant=34825215869066"))
print(deborahlippmann_ingre("https://deborahlippmann.com/collections/sets/products/fast-girls-base-coat-and-addicted-to-speed-top-coat?variant=41473051066506"))