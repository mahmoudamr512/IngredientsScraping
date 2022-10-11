import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import ast

def polaar_ingre(product_url):
    def normalize_paragraph(para):
        para = para.strip()
        para = para.replace("Ingredients :", "")
        para = para.replace("Ingredients: ", "")
        para = para.replace("Ingredients ", "")
        para = para.strip()
        para = ", ".join(para.split("; ")).title()
        para = ", ".join(para.split(" -")).title()
        para = para.lower()\
            .replace("only the list on the product label is authentic.", "")\
            .replace('\r', "").replace('only the list of ingredients on the product is authentic.', '').replace(';;', ';').title()

        while True:
            flag = False
            if para[0] == ';':
                para = para[1:]
                flag = True

            if para[0] == '.':
                para = para[1:]
                flag = True

            if para[0] == '\r':
                para = para[1:]
                flag = True

            if para[0] == '\n':
                para = para[1:]
                flag = True

            if para[0] == ' ':
                para = para[1:]
                flag = True

            if para[0] == ',':
                para = para[1:]
                flag = True

            if para[-1] == ';':
                para = para[:-1]
                flag = True

            if para[-1] == ',':
                para = para[:-1]
                flag = True

            if para[-1] == '.':
                para = para[:-1]
                flag = True

            if not flag:
                break

        return para.strip()

    def extract_keys(soup):
        try:
            key_ingre_div = soup.find('div', attrs={'class', "les-actifs--container"})

            return ", ".join([h3.text.replace('\n', '').strip() for h3 in key_ingre_div.find_all('h3')]).replace('\n','').strip()
        except:
            return 'N/A'

    def extract_ingre(soup):
        ingre_para_list = soup.find("p", {'class': 'content-ingredients'}).text.split('\n')
        ingredients_paragraph = ";".join(ingre_para_list)

        try:
            return normalize_paragraph(ingredients_paragraph)
        except:
            return 'N/A'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36'}  # Defining the User-Agent to fake browser
    response = requests.get(product_url, headers=headers)  # Requesting the product page using product url and headers
    soup = bs(response.content,
              'html.parser')  # Creating the soup using the beautifulsoup library and the response received from the above request
    return [product_url, extract_ingre(soup), extract_keys(soup)]


print(polaar_ingre("https://en.polaar.com/products/gummies-belle-peau"))
print(polaar_ingre("https://en.polaar.com/products/cils-sourcils-icy-magic"))
print(polaar_ingre("https://en.polaar.com/products/solution-anti-imperfections"))
print(polaar_ingre("https://en.polaar.com/products/creme-jeunesse-tube"))
print(polaar_ingre("https://en.polaar.com/products/duo-anti-age-nuit-polaire"))
print(polaar_ingre("https://en.polaar.com/products/duo-anti-age-jour-et-nuit"))
print(polaar_ingre("https://en.polaar.com/products/cils-sourcils-icy-magic"))
print(polaar_ingre("https://en.polaar.com/products/roll-on-defatigant-regard-instantane"))
print(polaar_ingre("https://en.polaar.com/products/eau-micellaire-cristalline"))
print(polaar_ingre("https://en.polaar.com/products/routine-demaquillante"))
print(polaar_ingre("https://en.polaar.com/products/copie-de-rituel-masking"))
print(polaar_ingre("https://en.polaar.com/products/stick-solaire-spf50-sans-parfum"))
print(polaar_ingre("https://en.polaar.com/products/kit-solaire-spf50-format-voyage-edition-limitee"))
print(polaar_ingre("https://en.polaar.com/products/duo-corps-revitalisant"))
print(polaar_ingre("https://en.polaar.com/products/deodorant-mineral"))
print(polaar_ingre("https://en.polaar.com/products/coffret-neige-eternelle"))
print(polaar_ingre("https://en.polaar.com/products/routine-demaquillante"))