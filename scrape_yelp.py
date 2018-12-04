from pymongo import MongoClient
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
import json
import time
import random


we_eat_client = MongoClient()
we_eat_db = we_eat_client['we_eat']
website_collection = we_eat_db['websites']

def load_restaurant_aliases(filename='restaurant_aliases.txt'):
    with open(filename, 'r') as file: 
        for listitem in file:
            restaurant = listitem.strip() 
            yield restaurant

def scrape_yelp(url):
    browser.get(url)
    time.sleep(5 + random.random() * 10)
    return browser.page_source

def get_html(url):
    html = load_page_source(url)
    if html is None:
        html = scrape_yelp(url)
        save_page_source(url, html)
    return html

def load_page_source(url):
    search_result = website_collection.find_one({'url': url})
    if search_result is not None:
        return search_result['html']
    else:
        return None

def save_page_source(url, html):
    website_collection.delete_many({'url': url})
    website_collection.insert_one({'url': url, 'html': html})

def get_restaurant_html(restaurant_aliases):
    for restaurant_alias in restaurant_aliases:
        url = 'https://www.yelp.com/biz/' + restaurant_alias
        print(url)
        get_html(url)

#to add restaurants to the collection:
# browser = Chrome()
# restaurant_aliases = load_restaurant_aliases()
# get_restaurant_html(restaurant_aliases)