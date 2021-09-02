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