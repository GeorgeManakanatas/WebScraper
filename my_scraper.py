import requests
import logging
import re
import random
import time
import urllib.robotparser
from robots.my_robots import get_page, save_main_webpage, check_content
from database.my_database import PostgresqlInterface
from config import my_config
from logger.custom_logger import setup_custom_logger
from sitemaps.my_sitemap import iterate_sitemap_urls, get_sitemap_urls
from pages.my_pages import iterate_page_urls

# Reading config file into global variable
my_config.config_file()
# setting up scraping logger
logger = setup_custom_logger('scraping')
# initialize the postgres interface
interface = PostgresqlInterface()

if my_config.config_values['initialize_db']:
    interface.init_postgresql()

if my_config.config_values['scrape_websites']:
    page_urls = ['https://www.thedrive.com','https://medium.com','https://theintercept.com']

    logger.info('Looking at : %s',page_urls[0])
    # Getting "The Drive" robots page contents
    robot_page_url = page_urls[0] + '/robots.txt'
    # try to get the page
    robot_page_content = get_page(robot_page_url)
    # depending on the content save the main page
    save_main_webpage(robot_page_content, page_urls[0])
    # get randomized sitemap urls
    sitemap_urls = get_sitemap_urls(robot_page_content, page_urls[0])
    # visiting each sitemap and gettign the article urls
    logger.info('Visiting the sitemap urls')
    iterate_sitemap_urls(page_urls[0],sitemap_urls)
    # visiting each article and filling in the missing information
    # iterate_page_urls('output/war_zone.txt')

if my_config.config_values['get_raw_data']:
    logger.info('Getting raw data')
    all_id_page_results = interface.select_all_pages()
    # randomize pages
    random.shuffle(all_id_page_results)
    for id_page_result in all_id_page_results:
        # getting page
        logger.info('getting page : %s',id_page_result[1])
        # sleep random time
        time.sleep(random.randint(1,60))
        page_html = get_page(id_page_result[1])
        try:
            logger.info('saving page data: %s',id_page_result[1])
            interface.insert_to_page_info(id_page_result[1],page_html.encode('utf-8'))
        except Exception as exc:
            logger.warning('Error waving page data : %s', exc)
            
            