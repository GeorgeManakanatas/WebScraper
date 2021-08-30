import logging
import csv
import requests
import random
import time
from bs4 import BeautifulSoup
from logger.custom_logger import setup_custom_logger
from database.my_database import PostgresqlInterface
#
logger = logging.getLogger('scraping')
# initialize the postgres interface
interface = PostgresqlInterface()


def page_article_details(article_url):
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

def get_page_urls(request_url):
    all_urls = []
    # random wait period
    time.sleep(random.randint(10,60))
    try:
        # get page
        logger.info('getting page %s',str(request_url))
        page_cont = requests.get(request_url)
    except Exception as exc:
            logger.error('Error connecting to page : %s', exc)
            return all_urls
    try:
        # parse page
        page_soup = BeautifulSoup(page_cont.content, 'xml')
        all_elements = page_soup.findAll("url")
        logger.info('found %s loc elements',str(len(all_elements)))
    except Exception as exc:
        logger.error('Error parsing page contents : %s', exc)
        return all_urls
    # cleanup results
    for element in all_elements:
        all_urls.append(element.find("loc").getText())

    return all_urls

#
# def iterate_page_urls(file_path):
#     # initialize the array
#     articles_with_details = []
#     # open the war zone file
#     with open(file_path, 'r') as my_file:
#         # read file
#         file_reader = csv.DictReader(my_file, delimiter=',')
#         # get info from each URL
#         for row in file_reader:
#             # spacing the time
#             time.sleep(random.randint(10,60))
#             logger.info('going after URL : %s',row['url'])
#             article_info = page_article_details(row['url'])
#             articles_with_details.append(article_info)
#     #
#     with open('output/new_file.txt', 'w') as my_file:
#         for line in articles_with_details:
#             my_file.write(line+'\n')

def iterate_page_urls(website, sitemap, pages):
    '''
    Go over all the page urls in the sitemap page 
    '''
    # iterate through each url of the sitemap
    for item in pages:
        # be nice to the site and don't spam
        time.sleep(random.randint(10,60))
        logger.info('requesting url : %s',item.strip("'"))
        get_page = requests.get(item.strip("'"))
        xml_soup = BeautifulSoup(get_page.content, 'xml')
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
    return