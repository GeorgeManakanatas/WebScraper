import requests
import random
import time
import json
from config import my_config
from logger.custom_logger import setup_custom_logger
from database.my_database import PostgresqlInterface

# Reading config file into global variable
my_config.config_file()
# setting up scraping logger
logger = setup_custom_logger('scraping')
# initialize the postgres interface
interface = PostgresqlInterface()

if my_config.config_values['initialize_db']:
    logger.info('Initializing database')
    interface.init_postgresql()


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
            