This project is mostly about web scraping. I use it to read livesport.cz/tenis website and store data in database. The HTML content of match details is also saved for future use (for example for mining different statistics).
Main purpose of this project is getting data for future development. Now I am counting ELO rating of each player, but in the future I wouls like to implement and try some ML models to find out if it is possible beat betting company.

There are two directories:
    1) lvs_reading contains two script. 
        -read_lvs is scraping all unknown matches (not inserted in database) on livesport website and saving HTML content into file.
        -insert_to_database, is reading these HTML files, parsing data and inserting them into database. These scripts are separeted because I want to store raw data for the reason, that I may find out, that diferrent data is needed so I can create new database ind fill it from these files.
    2) ELO contains also two files.
        -ELO files is used for counting ELO rating for each player and updating after each match. 
        -database_handling was used only time for reading data from different source (csv files)

There is also one file (modul) in the main directory which contains shared functions for all scripts.       
