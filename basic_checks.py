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

print(type(all_id_page_results),len(all_id_page_results))
print(type(drive_list),len(drive_list))
print(type(war_zone_list),len(war_zone_list))
print()
# to sets to remove duplicates
set_all_id_page_results = set(all_id_page_results)
print(type(set_all_id_page_results),len(set_all_id_page_results))
set_drive_list = set(drive_list)
set_war_zone_list = set(war_zone_list)
# 
print(len(set_drive_list))
print(len(set_war_zone_list))