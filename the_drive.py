import requests
from bs4 import BeautifulSoup
import re
import os
import time
import random
import logging
#
logger = logging.getLogger('scraping')
#
def the_drive_sitemap_urls(urls):
    war_zone_articles = []
    other_articles = []
    # iterate through each url of the sitemap
    for item in urls:
        # be nice to the site and don't spam
        time.sleep(20)
        logger.info('requesting url : %s',item)
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
                logger.warning('Error parsing location and date: %s', exc)
            # adding to list
            if "the-war-zone" in str(location):
                war_zone_articles.append( (location, last_mod) )
            else:
                other_articles.append( (location, last_mod) )

    # when done write values to files files
    with open('output/war_zone.txt', 'w') as my_file:
        my_file.write('url,date\n')
        for given_tuple in war_zone_articles:
            entry_line = str(given_tuple[0])+','+str(given_tuple[1])+'\n'
            my_file.write(entry_line)

    with open('output/the_drive.txt', 'w') as my_file:
        my_file.write('url,date\n')
        for given_tuple in other_articles:
            entry_line = str(given_tuple[0])+','+str(given_tuple[1])+'\n'
            my_file.write(entry_line)
    return

