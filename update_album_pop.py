import sqlite3
import pandas as pd
from func_doc_api import *
import numpy as np
from tqdm import tqdm

# RUN THIS EVERYDAY AFTER 12PM for updated values

#read in the csv with all album_id
album_info = pd.read_csv("/Users/jaspertsai/Documents/GitHub/Spotify-PlayCounts/data/albums.csv")
## get all album_id
album_ids = album_info['album_id']

def update_album_today():
    # Get client id and secret to create a token
    CLIENT_ID, CLIENT_SECRET= configure()
    token = get_token(CLIENT_ID,CLIENT_SECRET)

    # index by 20 to use the more efficient search function 
    album_by_20_ind = np.arange(0,len(album_ids),20)
    album_by_20_ind = np.concatenate((album_by_20_ind, [len(album_ids)]))
    
    #keep track of the album_ids and popularity score
    album_ids_ls = []
    album_pop_ls = []

    #Loop through 20 album each time then loop through last
    for i in tqdm( range(len(album_by_20_ind)-1) ):
        lower = album_by_20_ind[i]
        upper = album_by_20_ind[i+1]
        #subset to allow function to search 20 albums at once
        subset_id = album_ids[lower:upper]
        temp_id,temp_pop = get_pop_by_album_limit_20(token,subset_id)
        #adds onto the list instead of append which adds list within list
        album_ids_ls.extend(temp_id)
        album_pop_ls.extend(temp_pop)

    data = pd.DataFrame({'album_id':album_ids_ls, 'album_popularity':album_pop_ls})
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