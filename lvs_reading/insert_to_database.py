#This script is used for parsing HTML files saved by 'read_lvs.py' and than inserting values into database.
#It checks if the id from website (which is part of the filename) is already present in the database.
#If not dictionary where keys are same as column names in table is created and than inserted into table.
#imports
import json
import bs4 as bs
import re
import os
import mysql.connector as mysql
from shared_func import *


def get_file_html(file):
    f = open(file)
    text = f.read()
    f.close()

    soup = bs.BeautifulSoup(text, "html.parser")

    return soup


def read_json_file(f_path):
    f = open(f_path)
    dict = json.load(f)
    f.close()

    return dict


main_dir = "/home/dusan/tennis_betting/lvs_stats/"
subdirs = [os.path.join(main_dir, d) for d in os.listdir(main_dir) if os.path.isdir(os.path.join(main_dir, d))]

dict_surface = read_json_file("/home/dusan/tennis_betting/lvs2sql/surface.txt")

#sign to database
db_tennis = mysql.connect(host="localhost", database="tennis", user="CODE", passwd=get_passw())
db_tennis_cursor = db_tennis.cursor()

tennis_db = DbHandling(db_tennis_cursor)

for d in subdirs:
    for file in os.listdir(d):
        db_dict = {}
        db_dict["lvs_id"] = re.match("[^_]+", file).group()
        if "_stat" in file or tennis_db.check_id_in_database(db_dict["lvs_id"]):
            continue

        print(file)
        file_soup = get_file_html(os.path.join(d, file))
        title_text = file_soup.find("title").get_text()

        score = re.search("[0-3]-[0-3]", title_text).group()
        name_one = re.search("(?<=\|)[^-]+(?=-)",title_text).group().strip()
        name_two = re.search("(?<=-)[^|]+(?=\|[^|]+\Z)",title_text).group().strip()

        if score.split("-")[0] > score.split("-")[1]:
            db_dict["winner_first_name"] = name_one.split(" ")[0]
            db_dict["loser_first_name"] = name_two.split(" ")[0]
            db_dict["winner_last_name"] = name_one.split(" ")[-1]
            db_dict["loser_last_name"] = name_two.split(" ")[-1]
        else:
            db_dict["winner_first_name"] = name_two.split(" ")[0]
            db_dict["loser_first_name"] = name_one.split(" ")[0]
            db_dict["winner_last_name"] = name_two.split(" ")[-1]
            db_dict["loser_last_name"] = name_one.split(" ")[-1]

        tournament_text = file_soup.find("span", {"class": re.compile("country.*")}).findChild().get_text()
        print(tournament_text)
        try:
            surface = re.search("(?<=,).+?(?=-)", tournament_text).group().strip()
            db_dict["surface"] = dict_surface[surface]
        except AttributeError:
            db_dict["surface"] = "neznamy"

        tennis_db.add_match(db_dict)

        print(db_dict)


db_tennis.commit()
