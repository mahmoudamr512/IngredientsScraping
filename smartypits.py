import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import ast

def smartypits_ingre(product_url):
    def normalize(para):
        para = para.strip().replace("plant-based prebiotic.", "").replace("plant-based prebiotic", "").replace("phthalate-free fragrance",'')\
                    .replace('*','').replace(": : ",":").replace('††', '').replace('.*', '').replace("  ", "").strip().replace('..', "")\
            .replace("--;", ";").replace("-;", ';').title().replace("-Or;", ";").replace("::", ":").replace(". .", "")
        if para[0] == ';':
            para = para[1:]
        return para
    def extract_ingre(soup):
        try:
            full_ingredients = ""
            ingredients_heading = soup.find('h5', text="Ingredients", attrs= {'class':'accordion-title'})
            all_para = ingredients_heading.find_next('div', attrs={'class': 'pdp-accordion-content body1'})
            for s in all_para.find_all('strong'):
                s.replace_with(bs(';' + s.text + ": ", 'html.parser'))
            all_para = all_para.text.strip().split('\n')

            for p in all_para:
                if "OR" in p.strip():
                    full_ingredients += "-"

                if not ("SMARTYPITS TIP" in p.upper() or "super-strength formula contains" in p.lower()) and len(all_para) > 1:
                    full_ingredients += p.lower().replace("\xa0", " ")
                elif len(all_para) == 1:
                    full_ingredients += p.lower().replace("\xa0", " ")
            if full_ingredients != "":
                return normalize(full_ingredients)

            return 'N/A'
        except:
            try:
                ingredients_heading = soup.find("h5", attrs={"data-mce-fragment": "1"})
                paragraph = ingredients_heading.find_next('p').text
                if "ingredients" in paragraph.lower():
                    return paragraph.replace("Ingredients:", "").strip()
                else:
                    return 'N/A'
            except:
                return 'N/A'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36'}  # Defining the User-Agent to fake browser
    response = requests.get(product_url, headers=headers)  # Requesting the product page using product url and headers
    soup = bs(response.content,
              'html.parser')  # Creating the soup using the beautifulsoup library and the response received from the above request
    return [product_url, extract_ingre(soup), 'N/A']

# print(smartypits_ingre("https://smartypits.com/collections/super-strength-aluminum-free-deodorant/products/aluminum-free-deodorant-tweed-spice"))
# print(smartypits_ingre("https://smartypits.com/collections/super-strength-aluminum-free-deodorant/products/grapefruit-cardamom"))
# print(smartypits_ingre("https://smartypits.com/collections/super-strength-aluminum-free-deodorant/products/charcoal-tea-tree"))
# print(smartypits_ingre("https://smartypits.com/collections/sensitive-skin-formula-deodorant/products/charcoal-tea-tree-3"))
# print(smartypits_ingre("https://smartypits.com/collections/smartypits-teen/products/pineapple-mango-smartypits-teen"))
# print(smartypits_ingre("https://smartypits.com/collections/probiotic-deodorant-cream/products/deodorant-cream-tweed-spice"))
# print(smartypits_ingre("https://smartypits.com/collections/smartyscents-roll-on-perfume/products/roll-on-perfume-tweed-spice"))
# print(smartypits_ingre("https://smartypits.com/collections/smartyscrub-sugar-scrub/products/sugar-scrub-lavender-rose"))
# print(smartypits_ingre("https://smartypits.com/collections/gifts-sets/products/5-product-scent-collection-set-vanilla-coconut"))
# print(smartypits_ingre("https://smartypits.com/collections/smartyscrub-sugar-scrub/products/sugar-scrub-lavender-rose"))
print(smartypits_ingre("https://smartypits.com/collections/gifts-sets/products/5-product-scent-collection-set-vanilla-coconut"))