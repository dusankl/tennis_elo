#This python script is used to fill table in database with data from csv files, which contain all matches from 2010-2020
#There are two tables in database: players, which contains data about each player, who played at least one ATP match
#and matches, which contains results of all played matches

import mysql.connector as mysql
from os import listdir
from os.path import join
import csv
from datetime import datetime
from shared_func import *


def add_player(first_name, last_name):
    sql_querry = "INSERT INTO players (name, surname, elo_hard, elo_clay, elo_grass, elo_mix) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (first_name, last_name, 1500, 1500, 1500, 1500)
    db_tennis_cursor.execute(sql_querry, values)


#sign to database

db_tennis = mysql.connect(host="localhost", database="tennis", user="CODE", passwd=get_passw())
db_tennis_cursor = db_tennis.cursor()


f = open("/home/dusan/Downloads/ATP_men/players/all_players_elo", "r")
for line in f.readlines():
    full_name = line.split(",")
    add_player(full_name[0].split(" ")[0], full_name[0].split(" ")[-1])

#read all files

list_csv_files = listdir("/home/dusan/Downloads/ATP_men/matches")
list_dict_matches = []

for file in list_csv_files:
    with open(join("/home/dusan/Downloads/ATP_men/matches", file), mode="r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            list_dict_matches.append(row)

for match in list_dict_matches:
    dict_match_data = {}
    dict_match_data["tournament_id"] = match["tourney_id"]
    dict_match_data["tournament_name"] = match["tourney_name"]
    dict_match_data["surface"] = match["surface"]
    if match["draw_size"]:
        dict_match_data["tournament_players_count"] = match["draw_size"]
    else:
        dict_match_data["tournament_players_count"] = -1
    dict_match_data["tournament_level"] = match["tourney_level"]
    dict_match_data["tournament_date"] = datetime.strptime(str(match["tourney_date"]), "%Y%m%d").isoformat()
    dict_match_data["winner_id"] = match["winner_id"]
    dict_match_data["winner_first_name"] = str(match["winner_name"]).split(" ")[0]
    dict_match_data["winner_last_name"] = str(match["winner_name"]).split(" ")[-1]
    dict_match_data["winner_hand"] = match["winner_hand"]
    if match["winner_ht"]:
        dict_match_data["winner_height"] = match["winner_ht"]
    else:
        dict_match_data["winner_height"] = -1
    dict_match_data["winner_country"] = match["winner_ioc"]
    if match["winner_age"]:
        dict_match_data["winner_age"] = match["winner_age"]
    else:
        dict_match_data["winner_age"] = -1
    dict_match_data["loser_id"] = match["loser_id"]
    dict_match_data["loser_first_name"] = str(match["loser_name"]).split(" ")[0]
    dict_match_data["loser_last_name"] = str(match["loser_name"]).split(" ")[-1]
    dict_match_data["loser_hand"] = match["loser_hand"]
    if match["loser_ht"]:
        dict_match_data["loser_height"] = match["loser_ht"]
    else:
        dict_match_data["loser_height"] = -1
    dict_match_data["loser_country"] = match["loser_ioc"]
    if match["loser_age"]:
        dict_match_data["loser_age"] = match["loser_age"]
    else:
        dict_match_data["loser_age"] = -1
    dict_match_data["score"] = match["score"]
    dict_match_data["round"] = match["round"]

    if match["minutes"]:
        dict_match_data["match_minutes"] = match["minutes"]
    else:
        dict_match_data["match_minutes"] = -1

    if match["w_ace"]:
        dict_match_data["winner_ace"] = match["w_ace"]
    else:
        dict_match_data["winner_ace"] = -1

    if match["w_df"]:
        dict_match_data["winner_df"] = match["w_df"]
    else:
        dict_match_data["winner_df"] = -1

    if match["w_svpt"]:
        dict_match_data["winner_serve_points"] = match["w_svpt"]
    else:
        dict_match_data["winner_serve_points"] = -1

    if match["w_1stIn"]:
        dict_match_data["winner_first_serve_in"] = match["w_1stIn"]
    else:
        dict_match_data["winner_first_serve_in"] = -1

    if match["w_1stWon"]:
        dict_match_data["winner_first_serve_won"] = match["w_1stWon"]
    else:
        dict_match_data["winner_first_serve_won"] = -1

    if match["w_2ndWon"]:
        dict_match_data["winner_second_serve_won"] = match["w_2ndWon"]
    else:
        dict_match_data["winner_second_serve_won"] = -1

    if match["w_SvGms"]:
        dict_match_data["winner_serve_games"] = match["w_SvGms"]
    else:
        dict_match_data["winner_serve_games"] = -1

    if match["w_bpSaved"]:
        dict_match_data["winner_bp_saved"] = match["w_bpSaved"]
    else:
        dict_match_data["winner_bp_saved"] = -1

    if match["w_bpFaced"]:
        dict_match_data["winner_bp_faced"] = match["w_bpFaced"]
    else:
        dict_match_data["winner_bp_faced"] = -1

    if match["l_ace"]:
        dict_match_data["loser_ace"] = match["l_ace"]
    else:
        dict_match_data["loser_ace"] = -1

    if match["l_df"]:
        dict_match_data["loser_df"] = match["l_df"]
    else:
        dict_match_data["loser_df"] = -1

    if match["l_svpt"]:
        dict_match_data["loser_serve_points"] = match["l_svpt"]
    else:
        dict_match_data["loser_serve_points"] = -1

    if match["l_1stIn"]:
        dict_match_data["loser_first_serve_in"] = match["l_1stIn"]
    else:
        dict_match_data["loser_first_serve_in"] = -1

    if match["l_1stWon"]:
        dict_match_data["loser_first_serve_won"] = match["l_1stWon"]
    else:
        dict_match_data["loser_first_serve_won"] = -1

    if match["l_2ndWon"]:
        dict_match_data["loser_second_serve_won"] = match["l_2ndWon"]
    else:
        dict_match_data["loser_second_serve_won"] = -1

    if match["l_SvGms"]:
        dict_match_data["loser_serve_games"] = match["l_SvGms"]
    else:
        dict_match_data["loser_serve_games"] = -1

    if match["l_bpSaved"]:
        dict_match_data["loser_bp_saved"] = match["l_bpSaved"]
    else:
        dict_match_data["loser_bp_saved"] = -1

    if match["l_bpFaced"]:
        dict_match_data["loser_bp_faced"] = match["l_bpFaced"]
    else:
        dict_match_data["loser_bp_faced"] = -1

    if match["winner_rank"]:
        dict_match_data["winner_rank"] = match["winner_rank"]
    else:
        dict_match_data["winner_rank"] = -1

    if match["winner_rank_points"]:
        dict_match_data["winner_rank_points"] = match["winner_rank_points"]
    else:
        dict_match_data["winner_rank_points"] = -1

    if match["loser_rank"]:
        dict_match_data["loser_rank"] = match["loser_rank"]
    else:
        dict_match_data["loser_rank"] = -1

    if match["loser_rank_points"]:
        dict_match_data["loser_rank_points"] = match["loser_rank_points"]
    else:
        dict_match_data["loser_rank_points"] = -1

    add_match(dict_match_data, db_tennis_cursor)

db_tennis.commit()
