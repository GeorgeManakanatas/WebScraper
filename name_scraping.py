import requests
import logging
import html
import random
import time
import json
from lxml import html
from lxml import etree
from bs4 import BeautifulSoup
import urllib.robotparser
from robots.my_robots import get_page, check_content, check_keywords
from database.my_database import PostgresqlInterface
from config import my_config
from logger.custom_logger import setup_custom_logger
from sitemaps.my_sitemap import iterate_sitemap_urls, get_all_sitemap_urls
from pages.my_pages import recursive_search_in_sitemap

# Reading config file into global variable
my_config.config_file()
# setting up scraping logger
logger = setup_custom_logger('scraping')
# initialize the postgres interface
interface = PostgresqlInterface()

if my_config.config_values['get_random_belgians']:
    # number of people to generate
    PERSON_SAMPLE_SIZE = 1000
    # initialize array
    full = []
    # get website from config
    for url in my_config.config_values['name_generator_url']:
        #logger.info('Looking at : %s',url)
        # repeat for sample size
        for i in range (0, PERSON_SAMPLE_SIZE):
            content = {}
            # sleep random time
            time.sleep(random.randint(10,20))
            # get the page
            page_content, page_found = get_page(url)
            # page_content=requests.get(url)
            # logger.info('page_content type : %s',type(page_content))
            tree = html.fromstring(page_content)
            #
            address = tree.xpath('/html/body/div[3]/div[1]/div[7]/div[12]//text()')
            website = tree.xpath('/html/body/div[3]/div[1]/div[7]/div[18]//text()')
            card_number = tree.xpath('/html/body/div[3]/div[1]/div[7]/div[24]//text()')
            card_expire = tree.xpath('/html/body/div[3]/div[1]/div[7]/div[26]//text()')
            security_code = tree.xpath('/html/body/div[3]/div[1]/div[7]/div[28]//text()')
            occupation = tree.xpath('/html/body/div[3]/div[1]/div[7]/div[30]//text()')
            company = tree.xpath('/html/body/div[3]/div[1]/div[7]/div[32]//text()')
            weight = tree.xpath('/html/body/div[3]/div[1]/div[7]/div[40]//text()')
            blood_type = tree.xpath('/html/body/div[3]/div[1]/div[7]/div[44]//text()')
            interested_movies = tree.xpath('/html/body/div[3]/div[1]/div[7]/div[50]//text()')
            favorite_actors = tree.xpath('/html/body/div[3]/div[1]/div[7]/div[52]//text()')
            favorite_actresses = tree.xpath('/html/body/div[3]/div[1]/div[7]/div[54]//text()')
            loved_songs = tree.xpath('/html/body/div[3]/div[1]/div[7]/div[56]//text()')
            idols = tree.xpath('/html/body/div[3]/div[1]/div[7]/div[58]//text()')
            #
            content["address"] = address
            content["website"] = website
            content["card_number"] = card_number
            content["card_expire"] = card_expire
            content["security_code"] = security_code
            content["occupation"] = occupation
            content["company"] = company
            content["weight"] = weight
            content["blood_type"] = blood_type
            content["interested_movies"] = interested_movies
            content["favorite_actors"] = favorite_actors
            content["favorite_actresses"] = favorite_actresses
            content["loved_songs"] = loved_songs
            content["idols"] = idols
            # content[i][""] = tree.xpath('//text()')
            # person_info = tree.xpath('/html/body/div[3]/div[1]/div[7]/div[2]/span//text()')
            #logger.info('content : %s',content)
            # store contents in array
            full.append(content)
        # after loop save to file
        with open('output/people.txt', 'a') as prods:
            products_config = json.dump(full,prods)