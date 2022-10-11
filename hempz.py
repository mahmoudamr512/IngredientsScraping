import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import ast

def hempz_ingre(product_url):
    def format_word(word):
        first_word = ""
        second_word = ""

        if len(word.split()) > 1:
            words_list = word.split()
            upper = False

            for i in range(0, len(words_list)):
                if words_list[i].isupper():
                    if i != len(words_list) - 1:
                        if words_list[i + 1].isupper():
                            upper = True

                    if upper:
                        second_word += words_list[i] + " "
                    else:
                        first_word += words_list[i] + " "
                else:
                    first_word += words_list[i] + " "

            return first_word.strip(), second_word.strip()
        else:
            return word, ""

    def format_string(input_text):
        final_text = ""
        input_list = input_text.split(',')
        for i in range(0, len(input_list)):
            fword, sword = format_word(input_list[i].strip())
            if i == 0:
                if fword != "":
                    final_text += fword + ", "
                else:
                    final_text += sword.title() + ": "
            else:
                if fword != '' and sword != '':
                    final_text += fword + ";"
                    final_text += sword.title() + ": "
                elif fword != '' and sword == '':
                    final_text += fword + ", "

        return final_text.strip()[:-1]

    def extract_ingredients(soupHTML):
        for div in soupHTML.find_all('p', {'class': 'Product-Details__Copy'}):
            parent = div.parent
            if "Collapsible__Content" in parent["class"]:
                return format_string(div.text.strip())
        return 'N/A'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36'}  # Defining the User-Agent to fake browser
    response = requests.get(product_url, headers=headers)  # Requesting the product page using product url and headers
    soup = bs(response.content,
              'html.parser')  # Creating the soup using the beautifulsoup library and the response received from the above request
    return [product_url, extract_ingredients(soup), 'N/A']

# print(hempz_ingre("https://hempz.com/collections/new-and-limited-edition/products/travel-size-bare-body-soft-citrus-sweet-creme-herbal-body-moisturizer"))
# print(hempz_ingre("https://hempz.com/collections/face-moisturizers/products/cbd-balancing-act-hydrating-facial-serum"))
# print(hempz_ingre("https://hempz.com/collections/face-moisturizers/products/cbd-sweet-dreams-gift-set"))
print(hempz_ingre("https://hempz.com/collections/hempz-petz/products/my-best-friend-petz-sweet-pineapple-honey-melon-deodorizing-hydrating-herbal-mist-happy-lip-balm-set"))