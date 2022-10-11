import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import ast

def petitenpretty_ingre(product_url):
    def normalize_paragraph(para):
        para = para.replace("Ingredients", "")
        para = para.replace("Ingrédients", "")
        para = para.replace('\r', '').replace('\n', '').replace(".;", ';')\
            .replace(" -- :", ":").replace(";;", ":").replace(" - ", ": ").strip().title().replace(";:", ":")
        para_list = para.split(';')
        ingre=""

        for i in range(0, len(para_list)):
            if ":" in para_list[i] or len(para_list[i].split(',')) > 2:
                ingre += para_list[i] + ";"

        if ingre.count(":;") <= 1:
            ingre = re.sub(r"^.*:;", '', ingre)

        while True:
            flag = False

            if ingre[0] == "/":
                ingre = ingre[1:]
                flag = True

            if ingre[0] == ":":
                ingre = ingre[1:]
                flag = True

            if ingre[0] == ";":
                ingre = ingre[1:]
                flag = True

            if not flag:
                break

        return ingre.strip()

    def extract_model(soup):
        model = soup.find('div', {'class': "modal__content"})
        if model is not None:
            for strong_div in model.find_all('strong'):
                strong_div.replace_with(bs(';' + strong_div.text +":", 'html.parser'))

            full_ingre = ""
            all_paragraphs = model.text.split('\n')

            for p in all_paragraphs:
                if p.strip() != "":
                    if p[0] != ";":
                        p = ";" + p
                    full_ingre += p
            return normalize_paragraph(full_ingre).replace(":;:", ":")
        return ""

    def extract_full_ingre(soup):
        model = extract_model(soup)
        if model != "":
            return model
        try:
            all_collapsable_divs = soup.find_all('div', {'class' : "product-tabs__tab-item-content"})

            for div in all_collapsable_divs:
                if div.parent.has_key("id") and "main-ingredients-content" in div.parent['id']:
                    all_paragraphs = div.find('p', _recursive=False).find_all('p')
                    if len(all_paragraphs) <= 1 and div.find('strong') is None:
                        if len(div.find('p').text) <= 7 or "made of" in div.find('p').text.lower():
                            return 'N/A'
                        return normalize_paragraph(div.find('p').text)
                    else:
                        full_ingre = ""
                        for p in all_paragraphs:
                            full_ingre += ";" + p.text
                        return normalize_paragraph(full_ingre)

            return 'N/A'
        except:
            model = extract_model(soup)
            if model != "":
                return model
            return 'N/A'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36'}  # Defining the User-Agent to fake browser
    response = requests.get(product_url, headers=headers)  # Requesting the product page using product url and headers
    soup = bs(response.content,
              'html.parser')  # Creating the soup using the beautifulsoup library and the response received from the above request


    return [product_url, extract_full_ingre(soup), 'N/A']

print(petitenpretty_ingre("https://www.petitenpretty.com/products/fully-feathered-kajal-eyeliner"))
print(petitenpretty_ingre("https://www.petitenpretty.com/products/my-stellar-micellar-makeup-remover-wipes"))
print(petitenpretty_ingre("https://www.petitenpretty.com/products/10k-shine-lip-gloss"))
print(petitenpretty_ingre("https://www.petitenpretty.com/products/gloss-balm-glossy-lip-balm"))
print(petitenpretty_ingre("https://www.petitenpretty.com/products/clearly-cute-makeup-gift-set"))
print(petitenpretty_ingre("https://www.petitenpretty.com/products/featherlight-clear-brow-gel"))
print(petitenpretty_ingre("https://www.petitenpretty.com/products/fully-feathered-volumizing-mascara"))
print(petitenpretty_ingre("https://www.petitenpretty.com/products/9021-bungalow-eye-cheek-palette"))
print(petitenpretty_ingre("https://www.petitenpretty.com/products/sparkly-ever-after"))
print(petitenpretty_ingre("https://www.petitenpretty.com/products/get-up-and-glow-travel-skincare-set"))
print(petitenpretty_ingre("https://www.petitenpretty.com/products/9021-glow-peel-off-glitter-face-mask"))
print(petitenpretty_ingre("https://www.petitenpretty.com/products/deck-the-palms-gen-glitter-duo"))
print(petitenpretty_ingre("https://www.petitenpretty.com/products/4-0-glow-back-to-school-makeup-set"))
print(petitenpretty_ingre("https://www.petitenpretty.com/products/glo-balm-glossy-lip-balm-gift-set"))
print(petitenpretty_ingre("https://www.petitenpretty.com/products/my-stellar-micellar-makeup-remover-wipes"))
print(petitenpretty_ingre("https://www.petitenpretty.com/products/so-much-yum-makeup-set"))