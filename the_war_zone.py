import logging
import csv
import requests
import time
from custom_logger import setup_custom_logger
from bs4 import BeautifulSoup
#
logger = logging.getLogger('scraping')
#
def war_zone_map(file_path):
    # initialize the array
    articles_with_details = []
    # open the war zone file
    with open(file_path, 'r') as my_file:
        # read file
        file_reader = csv.DictReader(my_file, delimiter=',')
        # get info from each URL
        for row in file_reader:
            # spacing the time
            time.sleep(20)
            logger.info('going after URL : %s',row['url'])
            article_info = get_war_zone_article_details(row['url'])
            articles_with_details.append(article_info)
    #
    with open('output/new_file.txt', 'w') as my_file:
        for line in articles_with_details:
            my_file.write(line+'\n')

def get_war_zone_article_details(article_url):
    # request the url
    page = requests.get(article_url)
    logger.info('got page : %s',article_url)
    # 
    soup = BeautifulSoup(page.content, 'html.parser')
    #
    title = soup.find('h1', class_='title').getText()
    dek = soup.find('h2', class_='dek').getText()
    metadata = soup.find('div', class_='article-metadata')

    temp_entry = [title, dek , str(metadata)]
    # logger.info(str(title),str(dek),metadata)
    #
    # logger.info('information!! : %s',data_string)
    return temp_entry