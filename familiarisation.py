# -*- coding: utf-8 -*-
'''
Playing around with a few examples to get the hang of the basics.
'''
import requests
from bs4 import BeautifulSoup

page = requests.get("http://dataquestio.github.io/web-scraping-pages/simple.html")
# getting page and contents
print(page.status_code, '\n')
print(page.content, '\n')
# using beautifulsoup to masage the contents
soup = BeautifulSoup(page.content, 'html.parser')
print(soup.prettify(), '\n')
# workking with nested componentes
page_components = list(soup.children)
print(page_components, '\n')
# the same can be done with the components
html_components = list(list(soup.children)[2])
print(html_components, '\n')
p1 = html_components[1]
p3 = html_components[3]
print(p1, '\n')
print(p1.get_text(), '\n')
print(p3, '\n')
print(p3.get_text(), '\n')
print('---------- array of all tags -------------')
# find all tags
print(soup.find_all('p'), '\n')
print(soup.find_all('title'), '\n')
print('---------- first tag found -------------')
# find first instance specific tag
print(soup.find('p'), '\n')
print(soup.find('title'), '\n')
print('---------- new page -------------')
# working with classes and ids in the page
new_page = requests.get("http://dataquestio.github.io/web-scraping-pages/ids_and_classes.html")
new_soup = BeautifulSoup(new_page.content, 'html.parser')
print('---------- new soup -------------')
print(new_soup.prettify(), '\n')
all_outer_text = new_soup.find_all('p', class_='outer-text')
print(all_outer_text, '\n')
print('---------- more realistic example -------------')
weather_page = requests.get("http://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168")
weather_soup = BeautifulSoup(weather_page.content, 'html.parser')
seven_day = weather_soup.find(id="seven-day-forecast")
forecast_items = seven_day.find_all(class_="tombstone-container")
tonight = forecast_items[0]
print(tonight.prettify())
