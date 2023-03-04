import sqlite3
import pandas as pd
from func_doc_api import *
import numpy as np
from tqdm import tqdm

# RUN THIS EVERYDAY AFTER 12PM for updated values

#read in the csv with all artist_id
album_info = pd.read_csv("/Users/jaspertsai/Documents/GitHub/Spotify-PlayCounts/data/albums.csv")
## get all artist_id
album_ids = album_info['album_id']

def update_album_today():
    # Get client id and secret to create a token
    CLIENT_ID, CLIENT_SECRET= configure()
    token = get_token(CLIENT_ID,CLIENT_SECRET)

    #keep track of the popularity score
    pop_score_lists = []

    for id in tqdm(album_ids):
            pop_score_lists.append(get_album_single_popularity_by_id(token, id))

    data = pd.DataFrame({'album_id':album_ids, 'album_popularity':pop_score_lists})

    data['date_tracked'] = pd.Timestamp.today().strftime('%Y-%m-%d')



#define connection and cursor
    ##connects to Spotify.db or create if not exist
    connection = sqlite3.connect('/Users/jaspertsai/Documents/GitHub/Spotify-PlayCounts/data/Spotify.db')
    cursor = connection.cursor()

    # Command to create the datatable if not exist
    create_main_table = """
        CREATE TABLE IF NOT EXISTS Albums_Popularity (
            album_id TEXT,
            album_popularity INTEGER,
            date_tracked DATE)
            """

    # Create database table
    cursor.execute(create_main_table)

    # insert dataframe into sqlite3 table
    data.to_sql(name='Albums_Popularity',con=connection, if_exists='append',index=False)
    #print(data)
    connection.commit()
    connection.close()
    print("successfully updated album popularity table")


update_album_today()