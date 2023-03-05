from func_undoc_api import *
import sqlite3


# RUN THIS EVERYDAY AFTER 12PM for updated values

#read in the csv with all album_id
album_info = pd.read_csv("/Users/jaspertsai/Documents/GitHub/Spotify-PlayCounts/data/albums.csv")
## get all album_id
album_ids = album_info['album_id']

def update_track_playcount_today():
    UNDOC_AUTHORIZATION, UNDOC_CLIENT_TOKEN = configure_undoc()
    data = get_all_playcounts_today(UNDOC_AUTHORIZATION,UNDOC_CLIENT_TOKEN,album_ids)
    #regex to convert track_uri to track_id
    data['track_uri'].replace( { r"\Aspotify:track:" : '' }, inplace= True, regex = True)
    data = data.rename(columns={"track_uri": "track_id","playcount":"track_playcount"})

    #define connection and cursor
    ##connects to Spotify.db or create if not exist
    connection = sqlite3.connect('/Users/jaspertsai/Documents/GitHub/Spotify-PlayCounts/data/Spotify.db')
    cursor = connection.cursor()

    # Command to create the datatable if not exist
    create_main_table = """
        CREATE TABLE IF NOT EXISTS Tracks_Playcount (
            track_id TEXT,
            track_playcount BIGINT,
            date_tracked DATE)
            """

    # Create database table
    cursor.execute(create_main_table)

    # insert dataframe into sqlite3 table
    data.to_sql(name='Tracks_Playcount',con=connection, if_exists='append',index=False)
    #print(data)
    connection.commit()
    connection.close()
    print("successfully updated track playcount table")

#update_track_playcount_today()