import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import ast

def danessamyricksbeauty_ingre(product_url) -> list:

    def extract_ingredients(soup) -> str:
        try:
            parent = soup.find('a', {'title': 'Open Ingredients'}).parent
            return parent.find('div', {'id': 'accordion_customTab2'}).text.strip()
        except:
            return 'N/A'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36'}  # Defining the User-Agent to fake browser
    response = requests.get(product_url, headers=headers)  # Requesting the product page using product url and headers
    soup = bs(response.content,
              'html.parser')  # Creating the soup using the beautifulsoup library and the response received from the above request

    return [product_url, extract_ingredients(soup), 'N/A']

print(danessamyricksbeauty_ingre("https://danessamyricksbeauty.com/collections/spring-shades/products/infinite-chrome-flakes-pixie-dust"))
print(danessamyricksbeauty_ingre("https://danessamyricksbeauty.com/collections/complexion/products/dewy-cheek-038-lip-palette-dew-it-undercover"))
print(danessamyricksbeauty_ingre("https://danessamyricksbeauty.com/collections/evolution-powder/products/evolution-powder-2"))
print(danessamyricksbeauty_ingre("https://danessamyricksbeauty.com/collections/enlight-halo-powders/products/enlight-illuminator-heaven-sent"))
print(danessamyricksbeauty_ingre("https://danessamyricksbeauty.com/collections/prime-set/products/bionic-gel-activator"))
print(danessamyricksbeauty_ingre("https://danessamyricksbeauty.com/collections/colorfix/products/colorfix-matte-chocolate"))