import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import ast

def nailberry_ingre(product_url):
    def extract_ingre(soup):
        ingre_div = soup.find('div', {'id':"tab-4"})

        if ingre_div is not None and ingre_div.text.strip() != '':
            return ingre_div.text.strip().title()

        return 'N/A'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36'}  # Defining the User-Agent to fake browser
    response = requests.get(product_url, headers=headers)  # Requesting the product page using product url and headers
    soup = bs(response.content,
              'html.parser')  # Creating the soup using the beautifulsoup library and the response received from the above request
    return [product_url, extract_ingre(soup), 'N/A']

print(nailberry_ingre("https://www.nailberry.co.uk/collections/loxygene-12-free-of-chemicals/products/copy-of-cherry-cherie"))
print(nailberry_ingre("https://www.nailberry.co.uk/collections/loxygene-12-free-of-chemicals/products/no-regrets"))
print(nailberry_ingre("https://www.nailberry.co.uk/collections/loxygene-12-free-of-chemicals/products/pink-guava"))
print(nailberry_ingre("https://www.nailberry.co.uk/collections/nail-care/products/acai-nail-elixir"))
print(nailberry_ingre("https://www.nailberry.co.uk/collections/gift-sets/products/everyday-nudes-collection"))

