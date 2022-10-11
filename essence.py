import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import ast

def essence_ingre(product_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36'}  # Defining the User-Agent to fake browser
    response = requests.get(product_url, headers=headers)  # Requesting the product page using product url and headers
    soup = bs(response.content,
              'html.parser')  # Creating the soup using the beautifulsoup library and the response received from the above request

    ingredientsDiv = soup.find('div', {'class': 'js-product-custom-ingredients'})

    return [product_url,ingredientsDiv.text.title().replace("Ingredients: ", "").replace('"', "").strip(), 'N/A']

print(essence_ingre("https://essencemakeup.com/collections/eyes/products/benvenuti-a-roma-eyeshadow-palette"))