import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import ast


def designessentials_ingre(product_url):
    def key_ingre(soup):
        try:
            div = soup.find('div', attrs={'id': 'tab-description'})
            key_ingre = ""
            for p in div.find_all('strong'):
                if "key ingredients" in p.text.lower().strip():
                    ul = p.find_next('ul')
                    for li in ul.find_all('li'):
                        key_ingre += re.match(r'^[A-Z,\s&]+', li.text.strip().replace('&amp;', '&')).group(0).strip() + ", "
                    return key_ingre.strip()[:-1].title().strip()
            return 'N/A'
        except Exception as ex:
            print(ex)
            return 'N/A'

    def extract_ingre(soup):
        try:
            set_flag = False

            divs = soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['prod-ingredients'])

            if len(divs) <= 1:
                if divs[0].find('ul') is None:
                    return divs[0].text.strip().title()
                else:
                    set_flag = True

            if not set_flag:
                for div in divs:
                    if div.find('a') is not None or div.find('ul') is not None:
                        set_flag = True

            if not set_flag:
                for div in divs:
                    if div.text.strip() != "":
                        return " ".join(div.text.strip().title().split())
            else:
                full_ingre = ""
                for div in divs:
                    if div.find('ul') is not None:
                        for li in div.find_all('li'):
                            a_ele = li.find('a')
                            full_ingre += ";" + a_ele.find('span').text.strip().title() + ":" + \
                                          designessentials_ingre(a_ele.get('href'))[1]
                    else:
                        if div.find('a') is not None:
                            product_title = None
                            if div.find('strong') is not None:
                                product_title = div.find('strong').text.strip().title()
                            else:
                                product_title = div.find('span').text.strip().title()
                            a_ele = div.find('a')
                            full_ingre += ";" + product_title + ":" + \
                                          designessentials_ingre(a_ele.get('href'))[1]
                return " ".join(full_ingre[1:].strip().split())

        except:
            return 'N/A'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36'}  # Defining the User-Agent to fake browser
    response = requests.get(product_url, headers=headers)  # Requesting the product page using product url and headers
    soup = bs(response.content,
              'html.parser')  # Creating the soup using the beautifulsoup library and the response received from the above request

    return [product_url, extract_ingre(soup), key_ingre(soup)]


############ Individual Products
# print(designessentials_ingre("https://designessentials.com/sleek-edge-control/"))
# print(designessentials_ingre("https://designessentials.com/bamboo-silk-hco-leave-in-conditioner/"))
# print(designessentials_ingre("https://designessentials.com/wash-day-deep-moisture-masque/"))
print(designessentials_ingre("https://designessentials.com/sleek-max-edge-control/"))
print(designessentials_ingre("https://designessentials.com/phusion-satin-hair-wrap-plus-sleep-mask/"))
print(designessentials_ingre("https://designessentials.com/volumizing-shampoo-step-1/"))
print(designessentials_ingre("https://designessentials.com/agave-lavender-detangling-conditioner/"))
print(designessentials_ingre("https://designessentials.com/twist-set-setting-lotion/"))
print(designessentials_ingre("https://designessentials.com/scalp-skin-care-anti-itch-tension-relief/"))
print(designessentials_ingre("https://designessentials.com/scalp-skin-care-detoxifying-tonic/"))
print(designessentials_ingre("https://designessentials.com/formations-finishing-spritz/"))

########### SETS ######################
print(designessentials_ingre("https://designessentials.com/agave-lavender-silk-press-collections/"))
print(designessentials_ingre("https://designessentials.com/protective-style-maintenance-pack/"))
print(designessentials_ingre("https://designessentials.com/kid-easy-as-1-2-3-style-pack/"))
print(designessentials_ingre("https://designessentials.com/youve-got-style-bundle/"))