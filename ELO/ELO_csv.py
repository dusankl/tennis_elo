#This script is used to count ELO index for each player in database.
#It goes through all matches in database (table matches) and reads winner and loser
#Then it use ELO formula to count new ELO index of player and updates the player table

#imports
import mysql.connector as mysql
import time
from shared_func import *

start_time = time.time()


#functions


def append_players_list(players_from_matches, list_players):
    for player in players_from_matches:
        if player not in list_players:
            list_players[player] = 1500
    return list_players


def count_new_elo(w_elo, l_elo):
    konst = 40
    w_prop = 1/(1 + pow(10, 1*(l_elo - w_elo)/ 400))
    l_prop = 1 - w_prop
    w_new_elo = round(w_elo + konst * (1 - w_prop), 2)
    l_new_elo = round(l_elo + konst * (0 - l_prop), 2)

    return w_new_elo, l_new_elo


def find_player(first_name, last_name):
    sql_querry = "SELECT * FROM elo_test WHERE name='{}' AND surname='{}'".format(first_name, last_name)
    db_tennis_cursor.execute(sql_querry)
    data_player = db_tennis_cursor.fetchone()
    data_player["name"] = str(data_player["name"]).replace("'", "''")
    data_player["surname"] = str(data_player["surname"]).replace("'", "''")

    return data_player


#sign to database

db_tennis = mysql.connect(host="localhost", database="tennis", user="CODE", passwd=get_passw())
db_tennis_cursor = db_tennis.cursor(dictionary=True, buffered=True)

#get match data from database

db_tennis_cursor.execute("SELECT winner_first_name, winner_last_name, loser_first_name, loser_last_name, surface "
                         "FROM matches")
list_matches = db_tennis_cursor.fetchall()


#elo count

for match in list_matches:
    winner = find_player(str(match["winner_first_name"]).replace("'", "''"), str(match["winner_last_name"]).replace("'", "''"))
    loser = find_player(str(match["loser_first_name"]).replace("'", "''"), str(match["loser_last_name"]).replace("'", "''"))

    if match["surface"] and str(match["surface"]).lower() != "none":
        surface = "elo_{}".format(str(match["surface"]).lower())
        w_elo_surface = winner[surface]
        l_elo_surface = loser[surface]
        new_elo = count_new_elo(w_elo_surface, l_elo_surface)
        sql_q = "UPDATE elo_test SET {}={} WHERE name='{}' AND surname='{}'".format(surface, new_elo[0], winner["name"], winner["surname"])
        db_tennis_cursor.execute(sql_q)
        sql_q = "UPDATE elo_test SET {}={} WHERE name='{}' AND surname='{}'".format(surface, new_elo[1], loser["name"], loser["surname"])
        db_tennis_cursor.execute(sql_q)

    new_elo = count_new_elo(winner["elo_mix"], loser["elo_mix"])
    sql_q = "UPDATE elo_test SET elo_mix={} WHERE name='{}' AND surname='{}'".format(new_elo[0], winner["name"], winner["surname"])
    db_tennis_cursor.execute(sql_q)
    sql_q = "UPDATE elo_test SET elo_mix={} WHERE name='{}' AND surname='{}'".format(new_elo[1], loser["name"], loser["surname"])
    db_tennis_cursor.execute(sql_q)

db_tennis.commit()

print("time: {}".format(time.time() - start_time))
