import requests
import logging
import re
import random
import time
import json
from bs4 import BeautifulSoup
import urllib.robotparser
from robots.my_robots import get_page, check_content, check_keywords
from database.my_database import PostgresqlInterface
from config import my_config
from logger.custom_logger import setup_custom_logger
from sitemaps.my_sitemap import get_all_sitemap_urls
from pages.my_pages import get_page_urls, iterate_page_urls

# Reading config file into global variable
my_config.config_file()
# setting up scraping logger
logger = setup_custom_logger('scraping')
# initialize the postgres interface
interface = PostgresqlInterface()

if my_config.config_values['initialize_db']:
    logger.info('Initializing database')
    interface.init_postgresql()


if my_config.config_values['scrape_websites']:
    logger.info('number of websites: %s',str(len(my_config.config_values['website_urls'])))
    # go through all websites
    for url in my_config.config_values['website_urls']:
        logger.info('Looking at : %s',url)
        # Check the page is accessible
        page_content, page_found = get_page(url)
        # Getting robots page contents if page is found
        if page_found:
            logger.info('%s found',url)
            robot_page_url = url + '/robots.txt'
            robot_page_content, robot_page_found = get_page(robot_page_url)
        logger.info('Robot page: \n %s',str(robot_page_content))
        logger.info('Robot page found: \n %s',str(robot_page_found))
        # if robot page is found get info out of it
        # TODO: redo this to work with urllib.robotparser
        keyword_results = check_keywords(robot_page_content)
        logger.info('Keyword results: \n %s',str(keyword_results))
        # save to database
        try:
            interface.insert_to_websites(website_url=url, has_robots_txt=robot_page_found, has_sitemap_xml=keyword_results['Sitemap'])
        except Exception as exc:
            logger.error('Error saving website url to DB: %s', exc)


if my_config.config_values['scrape_sitemaps']:
    # database call here to get list of all websites from DB
    website_info = interface.select_all_websites()
    logger.info('Website info: \n %s',str(website_info))
    # if website info false
    if not website_info:
        logger.info('Not getting sitemap info, because website table not retrieved')
    else:
        logger.info('Looking for sitemap urls')
        # look for new sitemap URLs and save them in databasee
        new_urls_found = get_all_sitemap_urls(website_info)
        logger.info('Urls found %s',str(new_urls_found))
        # log the output
        if new_urls_found:
            logger.info('New sitemap urls found')
        else:
            logger.info('No new sitemap urls')


if my_config.config_values['scrape_pages']:
    # database call to get list of sitemap URLs
    sitemaps_info = interface.select_sitemaps_and_websites()
    logger.info('Number of Sitemaps \n %s',str(len(sitemaps_info)))
    random.shuffle(sitemaps_info) # shuffle the sitemaps
    # read the sitemaps one at a time
    for table_row in sitemaps_info:
        sitemap_url = table_row[1]
        website = table_row[4]
        # logger.info('Sitemap url string \n %s',str(sitemap_url))
        # get all webpages in sitemap page
        page_urls = get_page_urls(sitemap_url)
        logger.info('Number of webpages: %s',str(len(page_urls)))
        # iterate_page_urls(website, sitemap_url, page_urls)
        for page_url in page_urls:
            try:
                logger.info('saving page url: %s',page_url)
                interface.insert_to_pages(website,sitemap_url,page_url)
            except Exception as exc:
                logger.warning('Error waving page data : %s', exc)

if my_config.config_values['scrape_raw_data']:
    logger.info('Getting raw data')
    all_id_page_results = interface.select_all_pages()
    # randomize pages
    random.shuffle(all_id_page_results)
    for id_page_result in all_id_page_results:
        # getting page
        logger.info('getting page : %s',id_page_result[1])
        # sleep random time
        time.sleep(random.randint(10,60))
        page_content, page_found = get_page(id_page_result[1])
        try:
            logger.info('saving page data: %s',id_page_result[1])
            interface.insert_to_page_info(id_page_result[1],page_content.encode('utf-8'))
        except Exception as exc:
            logger.warning('Error waving page data : %s', exc)
if my_config.config_values['check_product_prices']:
    logger.info('Getting product prices')
    # read configuration file
    with open('config/tracked_products_list.json', 'r') as prods:
        products_config = json.load(prods)
    #
    for product in products_config['items_list']:
        time.sleep(random.randint(10,60))
        page = requests.get(product['url'],headers={"User-Agent":"Defined"})
        logger.info(str(product['price_class']))
        logger.info(str(page))
        product_soup = BeautifulSoup(page.content, 'html.parser')
        price = product_soup.find('span', class_=product['price_class'])
        logger.info('The price is: '+str(price))
            
