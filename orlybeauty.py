import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import ast

def orlybeauty_ingre(product_url):

    def extract_ingredients(soup):
        try:
            full_ingre =  key_ingre = ""
            ingredients_span = None
            all_ingredients_spans = soup.find_all('span', {'class': 'ingredients'})
            for span in all_ingredients_spans:
                if "ingredients:" in span.text.lower():
                    ingredients_span = span

            paragraphs = ingredients_span.find_all('p')
            full = False
            i = 0
            while i < len(paragraphs):
                if "key ingredients" in paragraphs[i].text.lower():
                    try:
                        paragraphs[i].find('strong').extract()
                    except:
                        pass
                    key_ingre += paragraphs[i].text.strip()[:-1]

                    for j in range(1, len(paragraphs)):
                        if "ingredients:" not in paragraphs[j].text.lower():
                            key_ingre += ", " + paragraphs[j].text.strip().replace('.', '').replace('Key Ingredient: ', "")
                        else:
                            i = j
                            break
                else:
                    try:
                        paragraphs[i].find('strong').extract()
                    except:
                        pass
                    full_ingre += paragraphs[i].text.strip().replace('\n', '').replace('.', '') + ','
                    i += 1

            return full_ingre[:-1], key_ingre
        except:
            return 'N/A', 'N/A'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36'}  # Defining the User-Agent to fake browser
    response = requests.get(product_url, headers=headers)  # Requesting the product page using product url and headers
    soup = bs(response.content,
              'html.parser')  # Creating the soup using the beautifulsoup library and the response received from the above request

    full_ingre, key_ingre = extract_ingredients(soup)
    return [product_url, full_ingre, key_ingre]

print(orlybeauty_ingre("https://orlybeauty.com/products/metamorphosis"))
print(orlybeauty_ingre("https://orlybeauty.com/collections/tools/products/gel-fx-dry-brush"))
print(orlybeauty_ingre("https://orlybeauty.com/products/stop-the-clock"))
print(orlybeauty_ingre("https://orlybeauty.com/collections/nail-treatments/products/tough-cookie"))
print(orlybeauty_ingre("https://orlybeauty.com/collections/nail-treatments/products/cutique-cuticle-stain-remover"))
print(orlybeauty_ingre("https://orlybeauty.com/products/breathable-calcium-boost"))
print(orlybeauty_ingre("https://orlybeauty.com/products/crash-the-party"))