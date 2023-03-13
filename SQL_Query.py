import sqlite3 as sql
import pandas as pd

db = sql.connect("/Users/jaspertsai/Documents/GitHub/Spotify-PlayCounts/data/Spotify.db")


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

def plot_track_single(df,track_name):
    
    #grab only the data from the track and remove duplicates
    df = df[df['track_name'] == track_name]

    #grab from track popularity datafram queried
    dates = df['date_tracked']
    playcount = df['track_playcount']
    popularity = df['track_popularity']

    lower_play, upper_play = plot_range_playcount_followers(playcount)
    lower_pop, upper_pop = plot_range_popularity(popularity)
    
    #create the histograms
    fig = go.Figure(
        data=go.Bar(
            x= dates,
            y= playcount,
            name="Playcount",
            marker=dict(color="LightSkyBlue"),
        )
    )
    #add the lines 
    fig.add_trace(
        go.Scatter(
            x= dates,
            y= popularity,
            yaxis= "y2",
            name= "Popularity",
            marker=dict(color="purple"),
            mode='lines+markers'
        )
    )

    fig.update_layout(
        title={
            'text': f"{track_name}'s Playcount vs. Popularity",
            'font': {'size': 24},
            'x': 0.5,
            'xanchor': 'center'
        },
        legend=dict(orientation="h"),
        yaxis=dict(
            title=dict(text="Playcount"),
            range = [lower_play,upper_play], #change the range here
            side="left",
        ),
        yaxis2=dict(
            title=dict(text="Popularity Score"),
            side="right",
            range=[lower_pop, upper_pop], #change the range here
            overlaying="y",
            tickmode="auto",
        ),
    )
    fig.show()





