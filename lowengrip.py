import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import ast

def lowengrip_ingre(product_url):
    def extract_key(soup):
        try:
            key_ingre = "N/A"
            imgs = soup.find_all('img', {'data-mce-selected': 1})

            for img in imgs:
                parent = img.parent
                while "<p>" not in str(parent) and "<ul>" not in str(parent):
                    parent = parent.parent

                last_p = None
                if parent.find('ul') is None and parent.find('strong') is not None:
                    if key_ingre == "N/A":
                        key_ingre = ""
                    key_ingre += parent.find('strong').text.title().strip().replace(':', "").replace(";", "") + ", "
                    last_p = parent

                if last_p is not None:
                    current_p = last_p
                    next_p =current_p.find_next('p')
                    while next_p is not None and next_p.find('img') is None and "cruelty free" not in next_p.text.lower()\
                        and "cruelty-free" not in next_p.text.lower() and next_p.find('strong') is not None:
                            key_ingre += next_p.find('strong').text.title().strip().replace(':', "").replace(";", "") + ", "
                            next_p = next_p.find_next('p')
            key_ingre = key_ingre.strip()
            if key_ingre != "N/A":
                while True:
                    if key_ingre[-1] == ",":
                        key_ingre = key_ingre[:-1]
                    else:
                        break

            return key_ingre
        except Exception:
            return "N/A"
    def extract_ingre(soup):
        try:
            return soup.find('p', {'data-info': 'ingredients'}).text.strip().title()
        except:
            return 'N/A'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36'}  # Defining the User-Agent to fake browser
    response = requests.get(product_url, headers=headers)  # Requesting the product page using product url and headers
    soup = bs(response.content,
              'html.parser')  # Creating the soup using the beautifulsoup library and the response received from the above request
    return [product_url, extract_ingre(soup), extract_key(soup)]

# print(lowengrip_ingre("https://lowengrip.com/collections/value-sizes/products/healthy-glow-hand-balm-1"))
# print(lowengrip_ingre("https://lowengrip.com/collections/moisturizes-spf/products/healthy-glow-hand-balm-1"))
# print(lowengrip_ingre("https://lowengrip.com/collections/serums/products/the-serum-facial-serum"))
# print(lowengrip_ingre("https://lowengrip.com/collections/lotions-balms/products/balance-my-skin-body-lotion"))
# print(lowengrip_ingre("https://lowengrip.com/collections/shower-creams/products/healthy-glow-shower-cream"))
# print(lowengrip_ingre("https://lowengrip.com/collections/dry-shampoos/products/good-to-go-dry-shampoo-jasmine-amber-100ml"))
# print(lowengrip_ingre("https://lowengrip.com/collections/conditioners/products/blonde-perfection-silver-conditioner"))
# print(lowengrip_ingre("https://lowengrip.com/collections/level-up/products/level-up-volumizing-lotion"))
# print(lowengrip_ingre("https://lowengrip.com/collections/self-tan/products/luminous-bronze-self-tan-body-mist"))
print(lowengrip_ingre("https://lowengrip.com/collections/hand-foot-balm/products/healthy-glow-hand-balm-1"))
print(lowengrip_ingre("https://lowengrip.com/collections/deodorants/products/count-on-me-triple-value-pack"))
print(lowengrip_ingre("https://lowengrip.com/collections/lotions-balms/products/balance-my-skin-body-lotion"))
print(lowengrip_ingre("https://lowengrip.com/collections/moisturizes-spf/products/healthy-glow-hand-balm-1"))