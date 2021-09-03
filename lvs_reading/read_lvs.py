#This script is used to mine HTML code of website livesport.cz/tenis
#Because the page is dynamic, it uses Selenium for that.
#It finds all ATP finished matches on present day, which are not saved in database yet and get their id.
#Then it goes to previous day and this process is repeated until there is no previous day(livesport provides only last
#7 days) OR there are not matches (id) in current day, which is not in database.
#After this, it used mined id for for navigating to URL with detailed match statistics and saved raw HTML to a text file

# imports
from selenium import webdriver
import bs4 as bs
import re
import time
import os.path as osp
import os
import mysql.connector as mysql
from shared_func import *

# functions


def get_matches_id_from_date():
    soup = get_page_html("")
    soup_tournaments = soup.find("div", class_="sportName tennis")

    matches_id_date = []
    current_html_row = soup_tournaments.find("div")

    while current_html_row:
        if re.match("\A<div class=\"event__header( top)?\">", str(current_html_row)):
            tournament_type = current_html_row.find("span", class_="event__title--type").text
        elif tournament_type == "ATP - DVOUHRY":
            try:
                match_stage = current_html_row.find("div", class_="event__stage--block").text
            except:
                print("Tento zapas nema stage:")
                print(current_html_row.prettify())
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                match_stage = "-1"
            if match_stage == "Konec":
                quot_value = re.match("\A<[^>]+id=\"(?P<id_val>[^\"]+)", str(current_html_row)).group("id_val")
                matches_id_date.append(re.search("(?<=_)[^_]+\Z", quot_value).group())

        current_html_row = current_html_row.next_sibling

    return matches_id_date


def get_page_html(url):
    if url != "":
        driver.get(url)
    time.sleep(2)
    sauce_match = driver.page_source
    soup = bs.BeautifulSoup(sauce_match, "html.parser")

    return soup


def save_html_to_file(url, name):
    page_soup = get_page_html(url)

    stats_folder_path = "/home/dusan/tennis_betting/lvs_stats/{}".format(time.strftime("%Y%m%d"))
    if not osp.isdir(stats_folder_path):
        os.mkdir(stats_folder_path)

    f = open(osp.join(stats_folder_path, name), "x")
    f.write(page_soup.prettify())
    f.close()


# open livesport

driver = webdriver.Firefox()
driver.get("https://www.livesport.cz/tenis/")
driver.maximize_window()

#sign to database
db_tennis = mysql.connect(host="localhost", database="tennis", user="CODE", passwd=get_passw())
db_tennis_cursor = db_tennis.cursor()

tennis_db = DbHandling(db_tennis_cursor)

#find all matches id

matches_id = []
matches_from_one_date = []

while True:
    current_date = driver.find_element_by_class_name("calendar__datepicker").text
    print(current_date)
    current_date = "{}.{}".format(str(current_date).split(" ")[0].replace("/", "."), time.localtime().tm_year)
    print("Koukam na den {}".format(current_date))
    matches_from_one_date = [id for id in get_matches_id_from_date() if not tennis_db.check_id_in_database(id)]

    if matches_from_one_date:
        for id in matches_from_one_date:
            matches_id.append(id)

    try:
        driver.find_element_by_xpath('//*[@title="Předchozí den"]').click()
    except Exception:
        break
    time.sleep(2)


#save match statistics pages html to file

for id in matches_id:
    print(id)
    save_html_to_file("https://www.livesport.cz/zapas/{match_id}/#prehled-zapasu/statistiky-zapasu/0"
                      .format(match_id=id), "{}_html_stat".format(id))
    save_html_to_file("https://www.livesport.cz/zapas/{match_id}/#prehled-zapasu"
                      .format(match_id=id), "{}_html_gen".format(id))


driver.close()
