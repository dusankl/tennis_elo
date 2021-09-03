#This file is for functions which I want to shar between all py files in project


class DbHandling:
    def __init__(self, cursor):
        self.cursor = cursor

    # Function to insert row into matches table
    def add_match(self, dict_data):
        sql_querry = "INSERT INTO matches( {columns} ) VALUES ( {place} );" \
            .format(columns=", ".join(dict_data.keys()), place=", ".join(["%s"] * len(dict_data)))
        print(sql_querry)
        self.cursor.execute(sql_querry, list(dict_data.values()))

    # Function to check, if given id is present in matches table
    def check_id_in_database(self, id):
        sql_select = "SELECT COUNT(*) FROM matches WHERE lvs_id='{}'".format(id)
        self.cursor.execute(sql_select)

        if self.cursor.fetchone()[0] == 1:
            return True
        else:
            return False


#Function used for reading password to database from text file
def get_passw():
    f = open("/home/dusan/Documents/sample_file.txt", "r")
    passw = f.read()
    f.close()

    return passw


