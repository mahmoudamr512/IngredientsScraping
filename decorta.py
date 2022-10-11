import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import ast
import json

def decorte_ingre(product_url):
    def normalize(text):
        para = text.lower().strip().replace("ingredients:", ":")
        if para[-1] == ';':
            para = para[:-1]
        while True:
            if para[0] == ":":
                para = para[1:]
            else:
                break

        return ", ".join(para.title().split("･ ")).strip().replace(": :", ":")

    def return_description(soup):

        for script in soup.find_all('script', type="application/ld+json"):
            if "description" in json.loads(script.text):
                return json.loads(script.text)["description"]

    def extract_ingre(text, soup) -> list:
        key_ingre = full_ingre = "N/A"

        paragraphs = text.split('\n')
        i = 0

        while i < len(paragraphs):
            if "key ingredients" in paragraphs[i].strip().lower():
                key_ingre = ""
                j = i + 1
                while j < len(paragraphs):
                    if "direction" not in paragraphs[j].lower().strip():
                        if paragraphs[j].lower().strip() != "":
                            key_ingre += paragraphs[j] + ", "
                            if len(paragraphs[j+1].strip().split(" ")) > 5 or "." in paragraphs[j+1].lower():
                                j += 2
                            else:
                                j += 1
                        else:
                            j += 1
                    else:
                        break
                i = j
                key_ingre = key_ingre.strip()[:-1]
            i += 1

        for button in soup.find_all("button", attrs={'data-action': 'toggle-collapsible'}):
            if button.text.lower().strip() == "ingredients":
                full_ingre = ""
                para_div = button.find_next('div', attrs={'class': 'dct-ingredients'})
                paragraphs = para_div.find_all('p')

                for p in paragraphs:
                    if "facial pure cotton" not in p.text.lower():
                        full_ingre += p.text + ";"
                full_ingre = normalize(full_ingre)
        return [full_ingre, key_ingre]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36'}  # Defining the User-Agent to fake browser
    response = requests.get(product_url, headers=headers)  # Requesting the product page using product url and headers
    soup = bs(response.content,
              'html.parser')  # Creating the soup using the beautifulsoup library and the response received from the above request

    description = return_description(soup)

    full_ingre, key_ingre = extract_ingre(description, soup)

    return [product_url, full_ingre, key_ingre]

print(decorte_ingre("https://decortecosmetics.com/collections/hydra-clarity-collection/products/hydra-clarity-micro-essence-cleansing-emulsion"))
print(decorte_ingre("https://decortecosmetics.com/collections/hydra-clarity-collection/products/hydra-clarity-restorative-concentrate-cream"))
print(decorte_ingre("https://decortecosmetics.com/collections/ipshot-collection/products/advanced-ip-shot"))
print(decorte_ingre("https://decortecosmetics.com/collections/ipshot-collection/products/advanced-ip-shot-wrinkle-treatment-mask"))
print(decorte_ingre("https://decortecosmetics.com/collections/vi-fusion/products/slim-firm-concentrate"))
print(decorte_ingre("https://decortecosmetics.com/collections/vi-fusion/products/vi-fusion-essentials"))
print(decorte_ingre("https://decortecosmetics.com/collections/vi-fusion/products/overnight-performance-cream"))
print(decorte_ingre("https://decortecosmetics.com/collections/gift-sets/products/aq-meliority-luxurious-coffret-perfect-collection-iii"))
print(decorte_ingre("https://decortecosmetics.com/collections/gifts/products/decorte-perfect-botanical-kit"))

