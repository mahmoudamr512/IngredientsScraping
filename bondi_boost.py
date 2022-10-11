import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import ast

def bondiboost_ingre(product_url):
    def extract_ingredients(div, inner=None):
        if inner == None:
            strong_spans = div.find_all('strong')
            if len(strong_spans) <= 1:
                return div.text.replace("*Certified Organic Ingredients", '').strip().replace('\n', '').replace('\xa0', '')
            else:
                for i in range(1, len(strong_spans)):
                    strong_spans[i].replace_with(";" + strong_spans[i].text)
                return div.text.replace("*Certified Organic Ingredients", '').strip().replace('\n', '').replace('\xa0', '')\
                    .replace('..', '')
        else:
            ingredients = div.find('h6')
            return ingredients.text.replace("Ingredients: ", '').replace('\n', '').replace('*Certified Organic Ingredients', '')\
                .replace('\xa0', '')


    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36'}  # Defining the User-Agent to fake browser
    response = requests.get(product_url, headers=headers)  # Requesting the product page using product url and headers
    soup = bs(response.content,
              'html.parser')  # Creating the soup using the beautifulsoup library and the response received from the above request

    for div in soup.find_all('div', {'class', 'collapsible-content collapsible-content--all'}):
        if "certified organic ingredients" in div.text.lower():
            return [product_url, extract_ingredients(div), 'N/A']

    for div in soup.find_all('div', {'class', 'product-description rte'}):
        if "Ingredients:" in div.text and div.find('h6') != None:
            return [product_url, extract_ingredients(div, 'inner'), 'N/A']

    for innerDiv in soup.find('div', {'class': 'tab-description'}).find_all('div', {'class', 'collapsibles-wrapper'}):
        btns = innerDiv.find_all('button')
        description_divs = innerDiv.find_all('div',  {'class', 'collapsible-content collapsible-content--all'})
        for i in range(0, len(btns)):
            if "ingredients" in btns[i].text.lower():
                return [product_url, extract_ingredients(description_divs[i]), 'N/A']

    return [product_url, 'N/A', 'N/A']

print(bondiboost_ingre("https://www.bondiboost.co.uk/collections/all/products/vitamin-b-redness-enlarged-pores-with-vitamin-b"))
# print(bondiboost_ingre("https://bondiboost.com/collections/best-selling-hair-products/products/shampoo-conditioner-bundle"))