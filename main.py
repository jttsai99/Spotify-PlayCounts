import streamlit as st
from SQL_Query import *
from plotting import *


st.title("Spotify Popularity and Playcounts")

artist_list = ["Ariana Grande", "Avicii", "BTS", "Coldplay", "Drake", "ILLENIUM", "JMIN", "Joji", "Martin Garrix",  "Mike Williams", "NIKI" ,"Taylor Swift"]


artist_selected = st.selectbox(
    'Select the artist you are interested in', options= artist_list)

st.header(f":red[{artist_selected}]")
theme = st.sidebar.checkbox('Toggle Plotly Theme')

with st.spinner('Generating plot...'):

    #get artist popularity df
    df = SQL_get_artist_pop(artist_selected)

    st.write(df.drop(columns='artist_id'))
    #get album popularity df
    df1 = SQL_get_albums_pop_artist(artist_selected)


    #get track playcount and popularity df
    df2 = SQL_get_tracks_playpop_artist(artist_selected)
    ## allow select albums
    album_names = df2['album_name'].unique()

    #get tracks that are singles
    df3 = SQL_get_tracks_playpop_artist(artist_selected).drop_duplicates(subset=['track_id','date_tracked','artist_name'])
    df3 = df3[df3['album_group'] == "single"]
    single_names = df3['track_name'].unique()

    #get tracks that are in albums (create new column with album and track name to avoid some album with same track name)
    df4 = SQL_get_tracks_playpop_artist(artist_selected).drop_duplicates(subset=['track_id','date_tracked','artist_name'])
    df4 = df4[df4['album_group'] == "album"]
    df4['album_track_name'] = df4['album_name'] + ': ' + df4['track_name']
    albumtrack_names = df4['album_track_name'].unique()






    # Generate the artist popularity plot
    fig = plot_artist(df)

    #Sidebar start
    st.sidebar.header("Control the plots")
    # Second plot
    st.sidebar.subheader("Latest Albums or Singles")
    # Generate the artist popularity plot
    ## slider to allow latest number of albums or singles
    album_slider1 = st.sidebar.slider("Select number of albums or singles", min_value=1, max_value=10, value=1)
    ## button to toggle album or single
    ablum_single = st.sidebar.radio("Plot by Album or Single", ('Album', 'Single'))
    if ablum_single == 'Album':
        album_val = True
    else:
        album_val = False
    # Create the actual plot with the parameters
    fig1 = plot_latest_albums_or_singles(df1, album = album_val,number = album_slider1)


    # Third plot
    st.sidebar.subheader("Album Tracks")
    album_name_selected = st.sidebar.selectbox(
    'Select the Album/Single you are interested in', options= album_names)
    ## button to toggle popularity score or playcount
    pop_status = st.sidebar.radio("Plot by Album or Single", ('Playcount', 'Popularity score'))
    if pop_status == 'Popularity score':
        pop_val = True
    else:
        pop_val = False
    # Generate the album tracks plots
    fig2 = plot_album_tracks(df2, album_name=album_name_selected, pop = pop_val)


    # Fourth plot
    st.sidebar.subheader("Single Tracks's Playcount vs. Popularity")
    single_track_selected = st.sidebar.selectbox(
    'Select the Track from Singles you are interested in', options= single_names)
    fig3 = plot_track_single(df3,single_track_selected)

    # Fifth plot
    st.sidebar.subheader("Album Tracks's Playcount vs. Popularity")
    album_track_selected = st.sidebar.selectbox(
    'Select the Track from Albums you are interested in', options= albumtrack_names)
    fig4 = plot_track_album(df4,album_track_selected)


    tab1, tab2 = st.tabs(
        ["Individual Artist Info", "All Artist Comparison" ])
with tab1:
    if theme == False:
    # Use the Streamlit theme.
    # This is the default. So you can also omit the theme argument.
        artist_plot1 = st.plotly_chart(fig, theme="streamlit", use_container_width=True)
        album_plot1 = st.plotly_chart(fig1, theme="streamlit", use_container_width=True)
        albumtracks_plot1 = st.plotly_chart(fig2, theme="streamlit", use_container_width=True)
        track_single_plot1 = st.plotly_chart(fig3, theme="streamlit", use_container_width=True)
        track_album_plot1 = st.plotly_chart(fig4, theme="streamlit", use_container_width=True)

    else:
    # Use the native Plotly theme.
        artist_plot2 = st.plotly_chart(fig, theme=None, use_container_width=True)
        album_plot2 = st.plotly_chart(fig1, theme=None, use_container_width=True)
        albumtracks_plot2 = st.plotly_chart(fig2, theme=None, use_container_width=True)
        track_single_plot2 = st.plotly_chart(fig3, theme=None, use_container_width=True)
        track_album_plot2 = st.plotly_chart(fig4, theme=None, use_container_width=True)

with tab2:
    pass

# Remove the spinner once the plot is displayed
st.spinner(False)



