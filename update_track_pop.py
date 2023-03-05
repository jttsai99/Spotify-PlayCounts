import sqlite3
import pandas as pd
from func_doc_api import *
import numpy as np
from tqdm import tqdm
import time

# RUN THIS EVERYDAY AFTER 12PM for updated values

#read in the csv with all track_id
track_info = pd.read_csv("/Users/jaspertsai/Documents/GitHub/Spotify-PlayCounts/data/tracks.csv")
## get all track_id
track_ids = track_info['track_id']

def update_track_today():
    # Get client id and secret to create a token
    CLIENT_ID, CLIENT_SECRET= configure()
    token = get_token(CLIENT_ID,CLIENT_SECRET)

    # index by 50 to use the more efficient search function 
    track_by_50_ind = np.arange(0,len(track_ids),50)
    track_by_50_ind = np.concatenate((track_by_50_ind, [len(track_ids)]))

    #keep track of the track_ids and popularity score
    track_ids_ls = []
    track_pop_ls = []

    #Loop through 50 track each time then loop through last
    for i in tqdm( range(len(track_by_50_ind)-1), desc='Updating track popularity info'):
        lower = track_by_50_ind[i]
        upper = track_by_50_ind[i+1]
        #subset to allow function to search 50 tracks at once
        subset_id = track_ids[lower:upper]
        temp_id,temp_pop = get_pop_by_tracks_limit_50(token,subset_id)
        #adds onto the list instead of append which adds list within list
        track_ids_ls.extend(temp_id)
        track_pop_ls.extend(temp_pop)
        time.sleep(0.1)

    data = pd.DataFrame({'track_id':track_ids_ls, 'track_popularity':track_pop_ls})
    data['date_tracked'] = pd.Timestamp.today().strftime('%Y-%m-%d')



#define connection and cursor
    ##connects to Spotify.db or create if not exist
    connection = sqlite3.connect('/Users/jaspertsai/Documents/GitHub/Spotify-PlayCounts/data/Spotify.db')
    cursor = connection.cursor()

    # Command to create the datatable if not exist
    create_main_table = """
        CREATE TABLE IF NOT EXISTS Tracks_Popularity (
            track_id TEXT,
            track_popularity INTEGER,
            date_tracked DATE)
            """

    # Create database table
    cursor.execute(create_main_table)

    # insert dataframe into sqlite3 table
    data.to_sql(name='Tracks_Popularity',con=connection, if_exists='append',index=False)
    #print(data)
    connection.commit()
    connection.close()
    print("successfully updated track popularity table")

    
#update_track_today()