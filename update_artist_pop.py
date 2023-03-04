import sqlite3
import pandas as pd
from func_doc_api import *
import numpy as np
from tqdm import tqdm

# RUN THIS EVERYDAY AFTER 12PM for updated values


## Create the dataframe with 12 artists
track_artist_list = np.array(["Ariana Grande", "Avicii", "BTS", "Coldplay", "Drake", "ILLENIUM", "JMIN", "Joji",
                              "Martin Garrix",  "Mike Williams", "NIKI" ,"Taylor Swift"], dtype = object)
def update_artist_today():
    # Get client id and secret to create a token
    CLIENT_ID, CLIENT_SECRET= configure()
    token = get_token(CLIENT_ID,CLIENT_SECRET)

    # list to combine all json object(dict)
    object_lists = []

    for artist in tqdm(track_artist_list):
        object_lists.append(search_artist(token, artist))

    #convert it to dataframe
    data = pd.DataFrame(object_lists)

    # drop artist_genres becuse it is harder to store list in SQL
    data = data.drop(['artist_genres'], axis=1)
    data['date_tracked'] = pd.Timestamp.today().strftime('%Y-%m-%d')



    #define connection and cursor
    ##connects to Spotify.db or create if not exist
    connection = sqlite3.connect('/Users/jaspertsai/Documents/GitHub/Spotify-PlayCounts/data/Spotify.db')
    cursor = connection.cursor()

    # Command to create the datatable if not exist
    create_main_table = """
        CREATE TABLE IF NOT EXISTS Artists_Popularity (
            artist_name TEXT,
            artist_id TEXT,
            artist_followers BIGINT,
            artist_popularity INTEGER,
            date_tracked DATE)
            """

    # Create database table
    cursor.execute(create_main_table)

    # insert dataframe into sqlite3 table
    data.to_sql(name='Artists_Popularity',con=connection, if_exists='append',index=False)
    #print(data)
    connection.commit()
    connection.close()
    print("successfully updated artist popularity table")

update_artist_today()