import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px


#Assist in plotting
def plot_range_popularity(df_column):
    '''Get the lower and upper range of popularity score (artist, album, track) to allow plotly to plot with padding'''
    lower = df_column.min()
    upper = df_column.max()

    lower = lower - 3
    upper = upper + 3
    if upper > 100:
        upper = 100
    if lower < 0:
        lower = 0
    
    return lower, upper

def plot_range_playcount_followers(df_column):
    '''Get the high and low of the popularity score '''
    lower = df_column.min()
    upper = df_column.max()

    data_range = upper - lower  # Calculate the data range
    padding = data_range * 0.1  # Set a padding of 10%
    lower = lower - padding  # Compute the lower limit of the range
    upper = upper + padding  # Compute the upper limit of the range

    return lower, upper




#Actual functions to plot
def plot_artist(df):
    '''plots the artist's followers and popularity score base on date_tracked'''
    #grab from artist popularity datafram queried
    artist_name = df['artist_name'][1]
    dates = df['date_tracked']
    followers = df['artist_followers']
    popularity = df['artist_popularity']

    lower_follower, upper_follower = plot_range_playcount_followers(followers)
    lower_pop, upper_pop = plot_range_popularity(popularity)
    
    #create the histograms
    fig = go.Figure(
        data=go.Bar(
            x= dates,
            y= followers,
            name="Followers",
            marker=dict(color="pink"),
        )
    )
    #add the lines 
    fig.add_trace(
        go.Scatter(
            x= dates,
            y= popularity,
            yaxis= "y2",
            name= "Popularity",
            marker=dict(color="crimson"),
            mode='lines+markers'
            #text = popularity,
            #textposition='top center'
        )
    )

    fig.update_layout(
        title={
            'text': f"{artist_name}'s Followers and Popularity",
            'font': {'size': 24},
            'x': 0.5,
            'xanchor': 'center'
        },
        legend=dict(orientation="h"),
        yaxis=dict(
            title=dict(text="Followers"),
            range = [lower_follower,upper_follower], #change the range here
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
    return fig

def plot_latest_albums_or_singles(df, album = True, number = 1):
    '''allow to toggle latest album or single and plot the popularity score'''

    ## Processing data
    artist_name = df['artist_name'][1]


    #select album or single
    if album == True:
        types = "Album(s)"
        df = df[df['album_group'] == 'album']

    else:
        types = "Single(s)"
        df = df[df['album_group'] == 'single']


    #grab the album_name of the first to the number selected
    temp_name = df['album_name'].iloc[0:number]
    new_df = df[df['album_name'].isin(temp_name)]

    #last check for duplicates
    new_df.drop_duplicates()

    # Use plotly express to create the graph
    fig = px.line(new_df, x='date_tracked', y='album_popularity', color='album_name')

    # Update the legend
    fig.update_layout(
        title={
            'text': f"{artist_name}'s Latest {number} {types} Popularity",
            'font': {'size': 24},
            'x': 0.5,
            'xanchor': 'center'
        },
        legend=dict(
        title=f"{types}", #legend title
        font=dict(size=12)
        ),
        xaxis_title="Date",
        yaxis_title="Popularity Score"
    )
    
    return(fig)
    
def plot_album_tracks(df, album_name, pop = True):

     ## Processing data
    artist_name = df['artist_name'][1]


    # grab only the data that is from one album
    new_df = df[df['album_name'] == album_name]
    #last check for duplicates
    new_df.drop_duplicates()

    #select album or single
    if pop == True:
        types = "Popularity Score"
            # Use plotly express to create the graph
        fig = px.line(new_df, x='date_tracked', y='track_popularity', color='track_name')

    else:
        types = "Playcount"
        fig = px.line(new_df, x='date_tracked', y='track_playcount', color='track_name')



    # Update the legend
    fig.update_layout(
        title={
            'text': f"Album/Single: {album_name} {types}",
            'font': {'size': 24},
            'x': 0.5,
            'xanchor': 'center'
        },
        legend=dict(
        title=f"{types}", #legend title
        font=dict(size=12)
        ),
        xaxis_title="Date",
        yaxis_title= f"{types}"
    )
    
    return(fig)

def plot_track_single(df,track_name):
    
    #grab only the data from the track and remove duplicates
    df = df[df['track_name'] == track_name]
    df = df.drop_duplicates(subset=['track_name','track_playcount','date_tracked'],keep = 'last')
    

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
    return(fig)

def plot_track_album(df,albumtrack_name):
    
    #grab only the data from the track and remove duplicates
    df = df[df['album_track_name'] == albumtrack_name]

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
            marker=dict(color="mediumorchid"),
        )
    )
    #add the lines 
    fig.add_trace(
        go.Scatter(
            x= dates,
            y= popularity,
            yaxis= "y2",
            name= "Popularity",
            marker=dict(color="deepskyblue"),
            mode='lines+markers'
        )
    )

    fig.update_layout(
        title={
            'text': f"{albumtrack_name}'s Playcount vs. Popularity",
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
    return(fig)



