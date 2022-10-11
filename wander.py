import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import ast


def wander_ingre(product_url):
    def normalize_para(para):
        try:
            while True:
                if para[-1] == ';' or para[-1] == ":" or para[-1] == " ":
                    para = para[:-1]
                elif para[0] == " " or para[0] == ":":
                    para = para[1:]
                else:
                    break

            for word in re.findall(r':[A-Za-z0-9\s]+:', para):
                para = para.replace(word, word.replace(":", "")+": ")

            return para.title().replace(";:", ";")
        except:
            return 'N/A'

    def extract_key_ingre(soup):
        try:
            key_ingredients = soup.find('div', attrs={'class': "key-ingredients"})
            keys = [key.text.strip() for key in key_ingredients.find_all('strong')]
            return ", ".join(keys).strip().replace(":", "")
        except:
            return 'N/A'

    def extract_full_ingre(soup):
        try:
            full_ingre = ""
            ingredients_popup = soup.find('modal-dialog', attrs={'id': "PopupModal-ingredients"})
            paragraphs = ingredients_popup.find_all('p')

            if len(paragraphs) == 0:
                paragraphs = [bs(f"<p>{p.strip()}</p>", "html.parser") for p in ingredients_popup.text.split('\n') if p.lower() != "ingredients list" and p.strip() != ""]

            for p in paragraphs:
                if not ("made in" in p.text.lower() or "does not contain" in p.text.lower() or
                        (("oz" in p.text.lower() or "g" in p.text.lower()) and len(p.text.split(" ")) <= 4)):

                    if not ("always free of" in p.text.lower() or "cruelty free" in p.text.lower() or
                        "cruelty-free" in p.text.lower() or "ingredients in this composition may" in p.text.lower() or "gluten free" in p.text.lower() or
                        "vegan friendly" in p.text.lower() or "bpa free" in p.text.lower()):
                            if len(p.text.split()) <= 6:
                                full_ingre += p.text.strip().replace("\xa0", ' ') + ": "
                            else:
                                full_ingre += p.text.strip().replace("\xa0", ' ') + ";"
                    else:
                        if len(p.text.split(" ")) > 10:
                            if len(p.text.split()) <= 6:
                                full_ingre += p.text.strip().replace("\xa0", ' ') + ": "
                            else:
                                full_ingre += p.text.strip().replace("\xa0", ' ') + ";"


            return normalize_para(full_ingre)
        except:
            return 'N/A'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36'}  # Defining the User-Agent to fake browser
    response = requests.get(product_url, headers=headers)  # Requesting the product page using product url and headers
    soup = bs(response.content,
              'html.parser')  # Creating the soup using the beautifulsoup library and the response received from the above request
    return [product_url, extract_full_ingre(soup), extract_key_ingre(soup)]


# print(wander_ingre("https://www.wanderbeauty.com/collections/makeup-face/products/smooth-sailing-perfecting-primer"))
# print(wander_ingre("https://www.wanderbeauty.com/products/upgraded-brows-pencil-gel-duo"))
# print(wander_ingre("https://www.wanderbeauty.com/collections/skincare/products/hidden-glow-brightening-cream"))
# print(wander_ingre("https://www.wanderbeauty.com/collections/skincare/products/pack-up-and-glow"))
# print(wander_ingre("https://www.wanderbeauty.com/collections/skincare/products/baggage-claim-eye-masks"))
# print(wander_ingre("https://www.wanderbeauty.com/collections/makeup-face/products/pack-up-and-glow"))
# print(wander_ingre("https://www.wanderbeauty.com/collections/makeup-face/products/nude-illusion-liquid-foundation"))
# print(wander_ingre("https://www.wanderbeauty.com/collections/makeup-face/products/trip-for-two-blush-and-bronzer-duo"))
# print(wander_ingre("https://www.wanderbeauty.com/collections/sets/products/wander-beauty-x-tenoverten-mask-mani-set"))
# print(wander_ingre("https://www.wanderbeauty.com/collections/sets/products/good-to-go-mini-hair-and-body-kit"))
# print(wander_ingre("https://www.wanderbeauty.com/collections/mascara/products/upgraded-lashes-thickening-mascara"))
# print(wander_ingre('https://www.wanderbeauty.com/collections/best-sellers/products/on-the-glow-blush-and-illuminator'))
# print(wander_ingre("https://www.wanderbeauty.com/collections/skincare/products/bom-voyage-cleansing-balm"))
print(wander_ingre("http://www.wanderbeauty.com/collections/sets/products/wander-beauty-x-tenoverten-mask-mani-set"))
