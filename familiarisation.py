# -*- coding: utf-8 -*-
'''
Playing around with a few examples to get the hang of the basics.
'''
import requests
import time
from bs4 import BeautifulSoup
print('---- ---- new run ---- ----')
# initializing
cities_dict = {"Antwerp":"https://weather.com/weather/today/l/BEXX0539:1:BE", \
        "Mol":"https://weather.com/weather/today/l/69e6ef05c2719d0dc9545bba8797a8cf95a8b71ca9e3defa17c67e881627f07a",\
        "Wageningen":"https://weather.com/weather/today/l/4e606702b02d3d535950b8512a4d51fdf491481a810e74da96cfa77cfc15d5b0",\
        "Athens":"https://weather.com/weather/today/l/GRXX0004:1:GR"}
days_dict = {"today":"daypart-0","tommorow":"daypart-2","day_after":"daypart-4"}
info_dict = {}
# looping over cities
for city, url in cities_dict.items():
    #
    day_dict = {}
    # timegap between requests to the site
    print('sleeping for 20')
    time.sleep(20)
    print('making request')
    page = requests.get(url, verify=False)
    print('parsing reply')
    weather_soup = BeautifulSoup(page.content, 'html.parser')
    # looping through the days
    for day, html_elem_name in days_dict.items():
        values_dict = {}
        info_section = weather_soup.find('div', id=str(html_elem_name))
        precipitation = info_section.find('span', class_='precip-val')
        values_dict['precipitation'] = precipitation.find('span').getText()
        temperature = info_section.find('div', class_='today-daypart-temp')
        values_dict['temperature'] = temperature.find('span').getText()
        day_dict[day] = values_dict
    #
    info_dict[city] = day_dict

print(info_dict)

# page = requests.get("http://dataquestio.github.io/web-scraping-pages/simple.html")
# # getting page and contents
# print(page.status_code, '\n')
# print(page.content, '\n')
# # using beautifulsoup to masage the contents
# soup = BeautifulSoup(page.content, 'html.parser')
# print(soup.prettify(), '\n')
# # workking with nested componentes
# page_components = list(soup.children)
# print(page_components, '\n')
# # the same can be done with the components
# html_components = list(list(soup.children)[2])
# print(html_components, '\n')
# p1 = html_components[1]
# p3 = html_components[3]
# print(p1, '\n')
# print(p1.get_text(), '\n')
# print(p3, '\n')
# print(p3.get_text(), '\n')
# print('---------- array of all tags -------------')
# # find all tags
# print(soup.find_all('p'), '\n')
# print(soup.find_all('title'), '\n')
# print('---------- first tag found -------------')
# # find first instance specific tag
# print(soup.find('p'), '\n')
# print(soup.find('title'), '\n')
# print('---------- new page -------------')
# # working with classes and ids in the page
# new_page = requests.get("http://dataquestio.github.io/web-scraping-pages/ids_and_classes.html")
# new_soup = BeautifulSoup(new_page.content, 'html.parser')
# print('---------- new soup -------------')
# print(new_soup.prettify(), '\n')
# all_outer_text = new_soup.find_all('p', class_='outer-text')
# print(all_outer_text, '\n')
# print('---------- more realistic example -------------')
# weather_page = requests.get("http://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168")
# weather_soup = BeautifulSoup(weather_page.content, 'html.parser')
# seven_day = weather_soup.find(id="seven-day-forecast")
# forecast_items = seven_day.find_all(class_="tombstone-container")
# tonight = forecast_items[0]
# print(tonight.prettify())
