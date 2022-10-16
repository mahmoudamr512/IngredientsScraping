import time

import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import ast


def oseamalibu_ingre(product_url):
    def normalize_para(para):
        para = para.strip().replace("Ingredients", "").title()

        while True:
            if para[-1] == "," or para[-1] == ';':
                para = para[:-1]
            elif para[0] == ":" or para[0] == " " or para[0] == ";":
                para = para[1:]
            else:
                break
        return para

    def get_chrome_options() -> webdriver.ChromeOptions:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument("--window-size=1200,800")
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--enable-javascript")
        options.add_argument('--disable-application-cache')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("disable-infobars")
        options.add_argument('--disable-gpu')
        options.add_argument('--incognito')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36')
        return options

    def open_selenium(open_url):

        with webdriver.Chrome(executable_path="./chromedriver", options=get_chrome_options()) as chrome:
            chrome.get(open_url)
            body = WebDriverWait(chrome, 15).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            return body.get_attribute('innerHTML')

    def extract_key_ingre(soup):
        try:
            key_ingre = ""
            ingre_heading = soup.find('h2', text='Key Ingredients')
            ingre_paragraphs = ingre_heading.find_next('div').find_all('p')
            for p in ingre_paragraphs:
                if p.text.strip() != "":
                    search = re.findall(r'.*:', p.text)
                    for group in search:
                        key_ingre += group.replace(':', ', ')

            return normalize_para(key_ingre.strip())
        except:
            return 'N/A'

    def extract_full_ingre(soup):
        try:
            full_ingre = ""
            ingre_heading = soup.find('label', text="Ingredients")
            paragraphs = ingre_heading.find_next("div", attrs={'class': 'css-accordion__content-wrapper'}).find_all('p')
            for p in paragraphs:
                if "is a blend of" not in p.text.lower().strip():
                    if len(paragraphs) > 1:
                        if p.find('b') is not None:
                            product_name = p.find('b')
                            product_name.extract()
                            full_ingre += ";" + product_name.text + ": " + p.text.strip()
                        elif p.find('strong') is not None:
                            product_name = p.find('strong')
                            product_name.extract()
                            full_ingre += ";" + product_name.text + ": " + p.text.strip()
                        else:
                            full_ingre += p.text.strip()
                    else:
                        para_list = str(p).split('<br/>')

                        for p in para_list:
                            if p != "":
                                paragraph = bs(p, 'html.parser')
                                if paragraph.find('b') is not None:
                                    full_ingre += ";" + paragraph.find('b').text + ": "
                                else:
                                    full_ingre += paragraph.text.strip()

            return normalize_para(full_ingre.replace('.;', ';'))
        except:
            return 'N/A'

    soup = bs(open_selenium(product_url),
              'html.parser')  # Creating the soup using the beautifulsoup library and the response received from the above request

    return [product_url, extract_full_ingre(soup), extract_key_ingre(soup)]

# print(oseamalibu_ingre("https://oseamalibu.com/products/vagus-nerve-bath-oil"))
# print(oseamalibu_ingre("https://oseamalibu.com/products/undaria-algae-body-butter"))
# print(oseamalibu_ingre("https://oseamalibu.com/products/body-glow-trio"))
# print(oseamalibu_ingre("https://oseamalibu.com/products/salts-of-the-earth-body-scrub"))
# print(oseamalibu_ingre("https://oseamalibu.com/products/ocean-cleansing-mudd"))
# print(oseamalibu_ingre("https://oseamalibu.com/products/sea-minerals-mist"))
# print(oseamalibu_ingre("https://oseamalibu.com/products/anti-aging-sea-serum"))
# print(oseamalibu_ingre("https://oseamalibu.com/products/ocean-eyes"))
# print(oseamalibu_ingre("https://oseamalibu.com/products/eye-care-duo"))
# print(oseamalibu_ingre("https://oseamalibu.com/products/blemish-balm"))
############################################################################
# print(oseamalibu_ingre("https://oseamalibu.com/products/seaglow-overnight-serum"))
# print(oseamalibu_ingre("https://oseamalibu.com/products/gua-sha-sculptor"))
# print(oseamalibu_ingre("https://oseamalibu.com/products/gua-sha-glow-duo"))
# print(oseamalibu_ingre("https://oseamalibu.com/products/advanced-protection-cream"))
# print(oseamalibu_ingre("https://oseamalibu.com/products/copy-of-anti-aging-ritual"))
# print(oseamalibu_ingre("https://oseamalibu.com/collections/skin-brightening/?page=1&sort_by=manual"))

print(oseamalibu_ingre('https://oseamalibu.com/products/miracle-moisture-trio'))