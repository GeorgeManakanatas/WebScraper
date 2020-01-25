import requests
from bs4 import BeautifulSoup
import re
import os
import time
import random
from xml.etree import ElementTree as ET
import logging

logger = logging.getLogger()
robot_page = requests.get("https://www.thedrive.com/robots.txt")

if robot_page.status_code == 200:
    print('Retun code 200! ')
    robot_page_text = robot_page.content
else: 
    print('Retun code not 200: ',robot_page.status_code)

"""
f = open("robots.txt", "r")
robot_page_text = f.read()
print(robot_page_text)
"""
# check if Disallow is in the page
if "Disallow" in str(robot_page_text):
    print('Disallow present')
# check if Disallow is in the page
if "Sitemap" in str(robot_page_text):
    print('Sitemap present')

#print(robot_page.status_code)
#print(robot_page.content)
#robot_soup = BeautifulSoup(robot_page.content, 'html.parser')

urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(robot_page_text))
# randomize the sitemap list
random.shuffle(urls)
# iterate through each page of the sitemap
war_zone_articles = []
other_articles = []

for item in urls:
    # be nice to the site and don't spam
    time.sleep(20)
    print('REQUEST URL: ',item.strip("'"))
    get_sitemap_page = requests.get(item.strip("'"))
    xml_soup = BeautifulSoup(get_sitemap_page.content, 'xml')
    #print('xml_soup \n',xml_soup)
    get_all_listed_urls = xml_soup.find_all('url')
    # randomize this list as well
    random.shuffle(get_all_listed_urls)
    # iterate through that list and get the war zone articles
    for article in get_all_listed_urls:
        # time.sleep(20)
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
with open('warZone.txt', 'w') as MyFile:
    MyFile.write('url,date\n')
    for given_tuple in war_zone_articles:
        entry_line = str(given_tuple[0])+','+str(given_tuple[1])+'\n'
        MyFile.write(entry_line)

with open('theDrive.txt', 'w') as MyFile:
    MyFile.write('url,date\n')
    for given_tuple in other_articles:
        entry_line = str(given_tuple[0])+','+str(given_tuple[1])+'\n'
        MyFile.write(entry_line)


