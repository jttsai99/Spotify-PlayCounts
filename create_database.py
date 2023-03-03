import sqlite3
import pandas as pd
from doc_api import *

## Create the initial dataframe with 10 artists





# #define connection and cursor
# ##connects to Spotify.db or create if not exist
# connection = sqlite3.connect('/Users/jaspertsai/Documents/GitHub/Spotify-PlayCounts/SQL_db/Spotify.db')
# cursor = connection.cursor()

# # Command to create the datatable if not exist
# create_main_table = """
#     CREATE TABLE IF NOT EXISTS artists (
#         pianist_id INTEGER PRIMARY KEY,
#         pianist_name TEXT)
#         """

# # get data from csv file into dataframe
# filename = "/Users/jaspertsai/Desktop/Pianist_Final/Create_database/pianists_info.csv"
# data = pd.read_csv(filename, usecols=['pianist_id', 'pianist_name'])

# # Create stock database table
# cursor.execute(create_main_table)

# # insert dataframe into sqlite3 table
# data.to_sql(name='pianists',con=connection, if_exists='replace')
# #print(data)
# connection.commit()
# connection.close()
