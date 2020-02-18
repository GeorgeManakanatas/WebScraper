'''
Database functions for the scraper
'''
import psycopg2
import sys
import logging
import csv
import datetime
from config import my_config
#
logger = logging.getLogger('scraping')
#
class PostgresqlInterface:
    '''
    All interactions with the Postgresql datbase
    '''
    def __init__(self, host='host_not_set', port='port_not_set', dbname='db_name_not_set', schemaname='schema_not_set', user='user_not_set', password='password_not_set' ):
        '''
        The constructor for PostgresqlInterface class.
                
        '''
        try:
            # logger.info('postgresql connection : %s', my_config.config_values['postgresql_connection'])
            self.host = my_config.config_values['postgresql_connection']['host']
            self.schemaname = my_config.config_values['postgresql_connection']['schemaname']
            self.port = my_config.config_values['postgresql_connection']['port']
            self.dbname = my_config.config_values['postgresql_connection']['dbname']
            self.user = my_config.config_values['postgresql_connection']['user']
            self.password = my_config.config_values['postgresql_connection']['password']
        except KeyError:
            logger.info('postgresql connection key error : %s', my_config.config_values['postgresql_connection'])
            self.host = host
            self.schemaname = schemaname
            self.port = port
            self.dbname = dbname
            self.user = user
            self.password = password

        # building the connection string
        self.CONN_STRING = 'host='+self.host+' port='+self.port+' dbname='+self.dbname+' user='+self.user+' password='+self.password

    def init_postgresql(self):
        '''
        Function to initialize the postgresql database

        Parameters:
            no arguments

        Returns:
            Boolean: True on success, False if an exception is thrown
        '''
        #
        SQL_CREATE_DATABASE = "CREATE DATABASE "+self.dbname+";"
        SQL_CREATE_CONDITIONAL = "SELECT pg_database.datname FROM pg_database WHERE datname =\'"+self.dbname+"\';"
        SQL_CREATE_SCHEMA = "CREATE SCHEMA IF NOT EXISTS scraping_info;"
        SQL_CEATE_TABLE_WEBSITES = "CREATE TABLE IF NOT EXISTS scraping_info.websites (id BIGSERIAL , website_url varchar NULL, has_robots_txt bool NULL, has_sitemap_xml bool NULL, last_scrape date NULL, post_date date NULL, CONSTRAINT websites_pk PRIMARY KEY (id), CONSTRAINT websites_un UNIQUE (website_url));"
        SQL_CEATE_TABLE_SITEMAPS = "CREATE TABLE IF NOT EXISTS scraping_info.sitemaps (id BIGSERIAL , sitemap_url varchar NULL, website BIGSERIAL, CONSTRAINT sitemaps_pk PRIMARY KEY (id), CONSTRAINT sitemaps_un UNIQUE (sitemap_url), CONSTRAINT sitemaps_fk FOREIGN KEY (website) REFERENCES scraping_info.websites(id));"
        SQL_CEATE_TABLE_PAGES = "CREATE TABLE IF NOT EXISTS scraping_info.pages (id BIGSERIAL , page_url varchar NULL, website BIGSERIAL, sitemap BIGSERIAL, CONSTRAINT pages_pk PRIMARY KEY (id), CONSTRAINT pages_un UNIQUE (page_url), CONSTRAINT pages_fk FOREIGN KEY (website) REFERENCES scraping_info.websites(id), CONSTRAINT pages_fk_1 FOREIGN KEY (sitemap) REFERENCES scraping_info.sitemaps(id));"
        SQL_CEATE_TABLE_PAGE_INFO = "CREATE TABLE IF NOT EXISTS scraping_info.page_info (id BIGSERIAL , page BIGSERIAL, raw_content bytea NULL, parsed_content jsonb NULL, CONSTRAINT page_info_pk PRIMARY KEY (id), CONSTRAINT page_info_fk FOREIGN KEY (page) REFERENCES scraping_info.pages(id));"
        # Creating the database
        try:
            # when initializing use connection string without db name
            CONN_STRING_ONE= 'host='+self.host+' port='+self.port+' user='+self.user+' password='+self.password
            # logger.info('SQL is : %s', SQL_CREATE_CONDITIONAL)
            conn = psycopg2.connect(CONN_STRING_ONE) # connecting to postgres without specific database
            conn.autocommit = True # needed to create database if it isn't found
            cursor = conn.cursor()
            cursor.execute(SQL_CREATE_CONDITIONAL) # looking for database
            condition = cursor.fetchall()
            if len(condition) == 0:
                cursor.execute(SQL_CREATE_DATABASE) # if not found create it
            conn.commit()
            conn.close()
        except Exception as exc:
            logger.warning('Error creating database : %s', exc)
            return False
        # Creating the database schema and tables
        try:
            conn = psycopg2.connect(self.CONN_STRING) # connectingto specific database   
            cursor = conn.cursor()
            cursor.execute(SQL_CREATE_SCHEMA)
            cursor.execute(SQL_CEATE_TABLE_WEBSITES)
            cursor.execute(SQL_CEATE_TABLE_SITEMAPS)
            cursor.execute(SQL_CEATE_TABLE_PAGES)
            cursor.execute(SQL_CEATE_TABLE_PAGE_INFO)
            conn.commit()
            conn.close()
        except Exception as exc:
            logger.warning('Error setting database : %s', exc)
            return False
        # 
        logger.info('Database initiated')
        return True


    def insert_to_websites(self, website_url, **kwargs):
        '''
        Function to insert to websites table

        Parameters:
            website_url (str): main website url
            has_robots_txt (bool): True or False depending on robots.txt found, optional, default: False
            has_sitemap_xml (bool): True or False depending on sitemap.xml found, optional, default: False
            last_scrape (date): Last date the site was scraped, optional, default: current date
            post_date (date): Last date the site was updated, optional, default: 1821-3-25

        Returns:
            Boolean: True on success, False if an exception is thrown
        '''
        if 'has_robots_txt' in kwargs:
            has_robots_txt = kwargs['has_robots_txt']
        else:
            has_robots_txt = False
        #
        if 'has_sitemap_xml' in kwargs:
            has_sitemap_xml = kwargs['has_sitemap_xml']
        else:
            has_sitemap_xml = False
        #
        if 'last_scrape' in kwargs:
            last_scrape = kwargs['last_scrape']
        else:
            last_scrape = datetime.datetime.now().date()
        #
        if 'post_date' in kwargs:
            post_date = kwargs['post_date']
        else:
            post_date = '1821-03-25'
        #
        data = (website_url, has_robots_txt, has_sitemap_xml, last_scrape, post_date)
        #
        SQL_INSERT_ROW_WEBSITES = "INSERT INTO scraping_info.websites(website_url, has_robots_txt, has_sitemap_xml, last_scrape, post_date)VALUES(%s, %s, %s, %s, %s) ON CONFLICT (website_url) DO NOTHING;"
        #
        try:
            conn = psycopg2.connect(self.CONN_STRING)    
            cursor = conn.cursor()
            cursor.execute(SQL_INSERT_ROW_WEBSITES,data)
            conn.commit()
            conn.close()
            return True
        except Exception as exc:
            logger.warning('Error inserting to table website : %s', exc)
            return False


    def select_all_websites(self):
        '''
        Function to get complete website table from the database

        Parameters:
            None.
        
        Returns:
            List , Bool: The records if sucess, False if an exception is thrown
        '''
        SQL_GET_ALL_WEBSITES = "SELECT * FROM scraping_info.websites;"
        try:
            conn = psycopg2.connect(self.CONN_STRING)    
            cursor = conn.cursor()
            cursor.execute(SQL_GET_ALL_WEBSITES)
            records = cursor.fetchall()
            conn.commit()
            conn.close()
            return records
        except Exception as exc:
            logger.warning('Error selecting website urls : %s', exc)
            return False

    def select_all_sitemaps(self):
        '''
        Function to get complete sitemap URLs

        Parameters:
            None
        
        Returns:
            List , Bool: The records if success, False if an exception is thrown
        '''
        SQL_GET_ALL_SITEMAPS = "SELECT * FROM scraping_info.sitemaps;"
        try:
            conn = psycopg2.connect(self.CONN_STRING)    
            cursor = conn.cursor()
            cursor.execute(SQL_GET_ALL_SITEMAPS)
            records = cursor.fetchall()
            conn.commit()
            conn.close()
            return records
        except Exception as exc:
            logger.warning('Error selecting website urls : %s', exc)
            return False

    def insert_to_sitemaps(self, website_url_value, sitemap_url_value):
        '''
        Function to insert to sitemaps table

        Parameters:
            website_url (str): The url for the website associated with the sitemap, used to find the foreign key
            sitemap_url (str): The url for the sitemap

        Returns:
            Boolean: True on success, False if an exception is thrown
        '''
        #
        data = (sitemap_url_value, website_url_value)
        # using the website_url to get the ID from websites as foreign key
        SQL_INSERT_ROW_SITEMAPS = "INSERT INTO scraping_info.sitemaps(sitemap_url, website) VALUES ( %s , (SELECT id from scraping_info.websites WHERE website_url= %s )) ON CONFLICT (sitemap_url) DO NOTHING;"
        #
        try:
            conn = psycopg2.connect(self.CONN_STRING)    
            cursor = conn.cursor()
            cursor.execute(SQL_INSERT_ROW_SITEMAPS,data)
            conn.commit()
            conn.close()
            return True
        except Exception as exc:
            logger.warning('Error inserting to table sitemaps : %s', exc)
            return False
    
    
    def insert_to_pages(self,website_url_value,sitemap_url_value,page_url_value):
        '''
        Function to insert to pages table

        Parameters:
            website_url (str): The url for the website associated with the page, used to find the foreign key
            sitemap_url (str): The url for the sitemap associated with the page, used to find the foreign key
            page_url (str): The url of the page

        Returns:
            Boolean: True on success, False if an exception is thrown
        '''
        #
        data = (page_url_value, website_url_value, sitemap_url_value)
        # using the website_url to get the ID from websites as foreign key
        SQL_INSERT_ROW_PAGES = "INSERT INTO scraping_info.pages(page_url, website, sitemap)VALUES( %s , (SELECT id from scraping_info.websites WHERE website_url=%s), (SELECT id from scraping_info.sitemaps WHERE sitemap_url=%s)) ON CONFLICT (page_url) DO NOTHING;"
        #
        try:
            conn = psycopg2.connect(self.CONN_STRING)    
            cursor = conn.cursor()
            cursor.execute(SQL_INSERT_ROW_PAGES,data)
            conn.commit()
            conn.close()
            return True
        except Exception as exc:
            logger.warning('Error inserting to table pages : %s', exc)
            return False
    

    def select_all_pages(self):
        '''
        Function to get all page URLs from the database

        Parameters:
            None.
        
        Returns:
            Boolean: The records, False if an exception is thrown
        '''
        SQL_GET_ALL_PAGES = "SELECT id, page_url FROM scraping_info.pages ;"
        try:
            conn = psycopg2.connect(self.CONN_STRING)    
            cursor = conn.cursor()
            cursor.execute(SQL_GET_ALL_PAGES)
            records = cursor.fetchall()
            conn.commit()
            conn.close()
            return records
        except Exception as exc:
            logger.warning('Error selecting page urls : %s', exc)
            return False
    

    def insert_to_page_info(self,page_url_value,page_html):
        '''
        '''
        data = (page_url_value,page_html)
        # using the website_url to get the ID from websites as foreign key
        SQL_INSERT_ROW_PAGE_INFO = "INSERT INTO scraping_info.page_info(page, raw_content) VALUES ( (SELECT id from scraping_info.pages WHERE page_url=%s), %s );"
        try:
            conn = psycopg2.connect(self.CONN_STRING)    
            cursor = conn.cursor()
            cursor.execute(SQL_INSERT_ROW_PAGE_INFO,data)
            conn.commit()
            conn.close()
            return True
        except Exception as exc:
            logger.warning('Error inserting page data : %s', exc)
            return False
        