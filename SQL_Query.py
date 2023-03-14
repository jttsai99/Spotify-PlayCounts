import sqlite3 as sql
import pandas as pd
import os

#make it so that others can run the app directly
db = sql.connect(f"{os.getcwd()}/data/Spotify.db")


def SQL_get_artist_pop(artist_name):
    df = pd.read_sql(
    f'''
    SELECT * 
    FROM Artists_Popularity
    WHERE artist_name = '{artist_name}'
    ''', db)
    return df

def SQL_get_albums_pop_artist(artist_name):
    df = pd.read_sql(
            f'''
            SELECT DISTINCT art.artist_name, alb.album_group, alb.album_name, alb.album_release_date, ap.album_popularity, ap.date_tracked
            FROM albums_popularity AS ap
            LEFT JOIN albums AS alb
            ON ap.album_id = alb.album_id
            LEFT JOIN artists AS art
            ON art.artist_id = alb.artist_id

            WHERE art.artist_name = '{artist_name}'
            '''
        , db)
    return df

def SQL_get_tracks_playpop_artist(artist_name):
    df = pd.read_sql(
        f''' 

        SELECT DISTINCT artist_name, album_name, album_group ,track_name, playc.track_id, track_number, track_popularity, track_playcount, playc.date_tracked
        FROM tracks_playcount AS playc

        LEFT JOIN tracks_popularity AS pop
        ON playc.track_id = pop.track_id AND playc.date_tracked = pop.date_tracked
        
        LEFT JOIN tracks
        USING(track_id)

        LEFT JOIN 
        (SELECT albums.album_id, albums.artist_id, albums.album_name, albums.album_group
        FROM albums) AS alb
        USING(album_id)

        LEFT JOIN artists
        USING (artist_id)

        WHERE artist_name = '{artist_name}' AND track_playcount > 0
        '''
    ,db)
    return df

def SQL_get_all_art_pop():
    df = pd.read_sql(
    f'''
    SELECT * 
    FROM Artists_Popularity
    ''', db)
    return df




