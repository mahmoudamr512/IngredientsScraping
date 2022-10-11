import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import ast


def heritage_stone(product_url):
    def normalize_para(text):

        full_ingre = ""

        for p in text.split('\n'):
            p = p.strip()

            if re.match('[^A-Za-z0-9\.\s,()\-:]+.*', p) is None:
                full_ingre += re.sub(r'[^A-Za-z0-9\.\s,()\-:&]+', '', p) + ";"

        while True:
            if full_ingre[-1] == ";" or full_ingre[-1] == '.':
                full_ingre = full_ingre[:-1]
            else:
                break

        return full_ingre.replace('.;', ';').replace('Certified Organic', '').replace('Ingredients:', '').strip()

    def extract_key(soup):
        try:
            return normalize_para(soup.find('h3', attrs={'class': 'product-ingredients__title'}).find_next('p').text)
        except:
            return 'N/A'

    def extract_ingre(soup):
        try:
            headings = soup.find_all('div', attrs={'class': "product-accordion__toggler"})
            if len(headings) > 0:
                ingre_para = None

                for heading in headings:
                    if heading.text.lower().strip() == "ingredients":
                        ingre_para = heading.find_next("div", attrs={"class", "product-accordion__content"})

                for br in ingre_para.find_all('br'):
                    br.replace_with(bs('\n', 'html.parser'))

                ingre_para = bs(str(ingre_para).replace('</p>', '\n'), 'html.parser')
                return normalize_para(ingre_para.text)

            product_desc = soup.find('div', attrs={'class': 'product-section__description'})
            for p in product_desc.find_all('p'):
                if "Ingredients:" in p.text:
                    return normalize_para(p.text)

            return 'N/A'
        except:
            return 'N/A'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36'}  # Defining the User-Agent to fake browser
    response = requests.get(product_url, headers=headers)  # Requesting the product page using product url and headers
    soup = bs(response.content,
              'html.parser')  # Creating the soup using the beautifulsoup library and the response received from the above request
    return [product_url, extract_ingre(soup), extract_key(soup)]

# print(heritage_stone("https://heritagestore.com/products/rosewater-toner"))
# print(heritage_stone("https://heritagestore.com/products/rosewater-glycerin-w-atomizer"))
# print(heritage_stone("https://heritagestore.com/products/castor-oil?pr_prod_strat=collection_fallback&pr_rec_id=f268efc0f&pr_rec_pid=4543411257390&pr_ref_pid=4354550825006&pr_seq=uniform"))
# print(heritage_stone("https://heritagestore.com/collections/rosewater/products/rosewater-jelly-mask"))
# print(heritage_stone("https://heritagestore.com/collections/aura-glow/products/aura-glow-gel-cream-hydrating-rose"))
# print(heritage_stone("https://heritagestore.com/collections/castor-oil/products/black-castor-oil"))
# print(heritage_stone("https://heritagestore.com/collections/castor-oil/products/cotton-flannel"))
# print(heritage_stone("https://heritagestore.com/collections/castor-oil/products/castor-serum"))
# print(heritage_stone("https://heritagestore.com/collections/all-products/products/colloidal-silver-soap"))
# print(heritage_stone("https://heritagestore.com/collections/all-products/products/rosewater-gallon"))
# print(heritage_stone("https://heritagestore.com/collections/skin-care/products/rosewater-moisturizer"))
# print(heritage_stone("https://heritagestore.com/collections/body-care/products/castor-oil"))
# print(heritage_stone("https://heritagestore.com/collections/body-care/products/colloidal-silver-soap"))
# print(heritage_stone("https://heritagestore.com/collections/oral-care/products/activated-charcoal-toothpaste"))
# print(heritage_stone("https://heritagestore.com/collections/oral-care/products/ipsab-toothpowder"))
# print(heritage_stone("https://heritagestore.com/collections/oral-care/products/hydrogen-peroxide-mouthwash-wintermint"))
# print(heritage_stone("https://heritagestore.com/collections/aura-glow/products/aura-glow"))
# print(heritage_stone("https://heritagestore.com/collections/skin-care/products/rosewater-concentrate"))
# print(heritage_stone("https://heritagestore.com/collections/all-products/products/black-castor-oil"))
print(heritage_stone("https://heritagestore.com/collections/all-products/products/rosewater"))
