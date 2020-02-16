import csv
from database.my_database import PostgresqlInterface

interface = PostgresqlInterface()

all_id_page_results = interface.select_all_pages()

with open('output/the_drive.txt', 'r') as my_file:
    # read file
    file_info = csv.reader(my_file)
    drive_list = list(file_info)
 

with open('output/war_zone.txt', 'r') as my_file:
    # read file
    file_info = csv.reader(my_file)
    war_zone_list = list(file_info)

# to sets to remove duplicates
set_all_id_page_results = set(all_id_page_results)
set_drive_list = set(drive_list)
set_war_zone_list = set(war_zone_list)
