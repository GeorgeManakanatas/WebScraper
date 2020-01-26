import requests
import logging
import re
import random
from custom_logger import setup_custom_logger
from the_drive import the_drive_sitemap_urls
from the_war_zone import war_zone_map
#
logger = setup_custom_logger('scraping')
#
def check_robots_page(contents):
    # check if Disallow is in the page
    if "Disallow" in str(contents):
        logger.info('Disallow present in robots page')
    # check if Disallow is in the page
    if "Sitemap" in str(contents):
        logger.info('Sitemap present in robots page')
    return

def robot_page_access(robot_page_url):
    try:
        # making request to page
        robot_page = requests.get(robot_page_url)
        # working with the reply
        if robot_page.status_code == 200:
            logger.info('Return code 200 for : %s',robot_page_url)
            robot_page_text = robot_page.content
        else: 
            logger.warning('Retun code not 200 for : %s', robot_page_url)
        return robot_page_text
    except Exception as exc:
            logger.warning('Error accessing the robots page: %s', exc)

# Getting "The Drive" robots page contents
page_url = 'https://www.thedrive.com/robots.txt'
robot_page_content = robot_page_access(page_url)
# 
check_robots_page(robot_page_content)
# get all urls from page
urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(robot_page_content))
logger.info('Getting all urls from : %s',page_url)
# randomize the urls to avoid being predictable.
logger.info('shuffling the sitemap urls')
random.shuffle(urls)
# visiting each page and gettign the article contents
logger.info('Working with the sitemap urls')
the_drive_sitemap_urls(urls)

# visiting each article and filling in the missing information
war_zone_map('output/war_zone.txt')
