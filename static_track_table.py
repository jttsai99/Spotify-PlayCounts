import sqlite3
import pandas as pd
from func_doc_api import *
import numpy as np
from tqdm import tqdm
import time

# Get client id and secret to create a token
CLIENT_ID, CLIENT_SECRET= configure()
token = get_token(CLIENT_ID,CLIENT_SECRET)


#read in the csv with all artist_id
album_info = pd.read_csv("/Users/jaspertsai/Documents/GitHub/Spotify-PlayCounts/data/albums.csv")
## get all artist_id
album_ids = album_info['album_id']

#check number of tracks 
## print(sum(album_info['total_tracks']))

#create dataframe to concatenate to 
data = pd.DataFrame()
for alb_id in tqdm(album_ids):
    temp = get_all_tracks_for_one_album(token,alb_id)
    data = pd.concat([data,temp], axis = 0)
    time.sleep(0.05)
data = data.reset_index(drop=True)



#define connection and cursor
##connects to Spotify.db or create if not exist
connection = sqlite3.connect('/Users/jaspertsai/Documents/GitHub/Spotify-PlayCounts/data/Spotify.db')
cursor = connection.cursor()

# Command to create the datatable if not exist
create_main_table = """
    CREATE TABLE IF NOT EXISTS Tracks (
        track_name TEXT,
        track_id TEXT,
        track_uri TEXT,
        track_number INTEGER,
        album_id TEXT
        )
        """

# Create database table
cursor.execute(create_main_table)

# insert dataframe into sqlite3 table
data.to_sql(name='Tracks',con=connection, if_exists='replace', index= False)
#print(data)
connection.commit()
connection.close()


data.to_csv("/Users/jaspertsai/Documents/GitHub/Spotify-PlayCounts/data/tracks.csv", index=False)
print("tracks database created")
