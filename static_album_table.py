import sqlite3
import pandas as pd
from func_doc_api import *
import numpy as np

# Get client id and secret to create a token
CLIENT_ID, CLIENT_SECRET= configure()
token = get_token(CLIENT_ID,CLIENT_SECRET)


#read in the csv with all artist_id
artist_identifier = pd.read_csv("/Users/jaspertsai/Documents/GitHub/Spotify-PlayCounts/data/artists.csv")
## get all artist_id
artist_ids = artist_identifier['artist_id']

# dataframe to concatinate each result to
data = pd.DataFrame()
for art_id in artist_ids:
    temp = get_all_singles_albums_by_artist(token,art_id)
    data = pd.concat([data,temp], axis = 0)
data = data.reset_index(drop=True)



#define connection and cursor
##connects to Spotify.db or create if not exist
connection = sqlite3.connect('/Users/jaspertsai/Documents/GitHub/Spotify-PlayCounts/data/Spotify.db')
cursor = connection.cursor()

# Command to create the datatable if not exist
create_main_table = """
    CREATE TABLE IF NOT EXISTS Albums (
        album_group TEXT,
        album_name TEXT,
        album_id TEXT,
        album_release_date DATE,
        total_tracks INTEGER,
        album_uri TEXT,
        artist_id TEXT)
        """

# Create database table
cursor.execute(create_main_table)

# insert dataframe into sqlite3 table
data.to_sql(name='Albums',con=connection, if_exists='replace', index= False)
#print(data)
connection.commit()
connection.close()


data.to_csv("/Users/jaspertsai/Documents/GitHub/Spotify-PlayCounts/data/albums.csv", index=False)
print("album database created")

