import requests
from bs4 import BeautifulSoup
import re
import os
import time
import random
import logging
from database.my_database import PostgresqlInterface
from config import my_config
from robots.my_robots import check_content
#
logger = logging.getLogger('scraping')
#
interface = PostgresqlInterface()


def get_sitemap_urls(robot_page_content, webpage_url):
    '''
    '''
    URL_REGULAR_EXPRESSION = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    # split the robots.txt in lines to start the process
    robot_lines = robot_page_content.splitlines()
    # go over all lines and build list of sitemaps
    sitemap_urls = []
    for line in robot_lines:
        # check if sitemaps is present in the lins
        if check_content(line, my_config.config_values['robots_keywords'][0]):
            # for true get the urls
            urls = re.findall(URL_REGULAR_EXPRESSION, line)
            for url in urls:
                sitemap_urls.append(url)
    # insert to database
    for url in sitemap_urls:
        logger.info('working with sitemap url : %s',url)
        try:
            interface.insert_to_sitemaps(webpage_url,url)
        except Exception as exc:
            logger.error('Error saving sitemap url to DB: %s', exc)
    # randomize the urls to avoid being predictable.
    logger.info('shuffling the sitemap urls')
    random.shuffle(sitemap_urls)
    return sitemap_urls

def iterate_sitemap_urls(website,sitemap_urls):
    '''
    '''
    war_zone_articles = []
    other_articles = []
    # iterate through each url of the sitemap
    for item in sitemap_urls:
        # be nice to the site and don't spam
        time.sleep(20)
        logger.info('requesting url : %s',item.strip("'"))
        get_sitemap_page = requests.get(item.strip("'"))
        xml_soup = BeautifulSoup(get_sitemap_page.content, 'xml')
        get_all_listed_urls = xml_soup.find_all('url')
        # randomize this list as well
        random.shuffle(get_all_listed_urls)
        # iterate through that list and get the war zone articles
        for article in get_all_listed_urls:
            try:     
                location = article.find('loc').getText()
                last_mod = article.find('lastmod').getText()
            except Exception as exc:
                logger.error('Error parsing location and date: %s', exc)
            try:
                interface.insert_to_pages(website,item,location)
            except Exception as exc:
                logger.error('Error saving page url to DB: %s', exc)

    # # when done write values to files files
    # with open('output/war_zone.txt', 'w') as my_file:
    #     my_file.write('url,date\n')
    #     for given_tuple in war_zone_articles:
    #         entry_line = str(given_tuple[0])+','+str(given_tuple[1])+'\n'
    #         my_file.write(entry_line)

    # with open('output/the_drive.txt', 'w') as my_file:
    #     my_file.write('url,date\n')
    #     for given_tuple in other_articles:
    #         entry_line = str(given_tuple[0])+','+str(given_tuple[1])+'\n'
    #         my_file.write(entry_line)

    return


