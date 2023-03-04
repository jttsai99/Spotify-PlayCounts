import sqlite3
import pandas as pd
from func_doc_api import *
import numpy as np
from tqdm import tqdm

## Create the initial dataframe with 12 artists
track_artist_list = np.array(["Ariana Grande", "Avicii", "BTS", "Coldplay", "Drake", "ILLENIUM", "JMIN", "Joji",
                              "Martin Garrix",  "Mike Williams", "NIKI" ,"Taylor Swift"], dtype = object)

# Get client id and secret to create a token
CLIENT_ID, CLIENT_SECRET= configure()
token = get_token(CLIENT_ID,CLIENT_SECRET)

# list to combine all json object(dict)
object_lists = []

for artist in tqdm(track_artist_list):
    object_lists.append(search_artist(token, artist))

#convert it to dataframe
data = pd.DataFrame(object_lists)

# drop all column except artist_name and artist_id
data = data.drop(['artist_followers','artist_popularity','artist_genres'], axis=1)
data = data[['artist_id', 'artist_name']]



#define connection and cursor
##connects to Spotify.db or create if not exist
connection = sqlite3.connect('/Users/jaspertsai/Documents/GitHub/Spotify-PlayCounts/data/Spotify.db')
cursor = connection.cursor()

# Command to create the datatable if not exist
create_main_table = """
    CREATE TABLE IF NOT EXISTS Artists (
        artist_id TEXT,
        artist_name TEXT)
        """

# Create database table
cursor.execute(create_main_table)

# insert dataframe into sqlite3 table
data.to_sql(name='Artists',con=connection, if_exists='replace', index= False)
#print(data)
connection.commit()
connection.close()


data.to_csv("/Users/jaspertsai/Documents/GitHub/Spotify-PlayCounts/data/artists.csv", index=False)
print("artist database created")
