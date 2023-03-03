from dotenv import load_dotenv
import os
import base64
import requests
import pandas as pd
import numpy as np

# Get configuration file that has all the api tokens
def configure():
    load_dotenv()
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    return CLIENT_ID, CLIENT_SECRET
    #Grab the Client_id and Client_secret from the env for the documented api


# Get token for the documented API (needs to be run after every hour)
def get_token(CLIENT_ID,CLIENT_SECRET):
    '''Takes the Client_ID and Client_Secret to request access token.
        Access tokens expire every hour so have to request new one'''
    ## Setup the authorization str and convert to base64  
    auth_str = CLIENT_ID + ":" + CLIENT_SECRET
    #encode str with utf-8 first
    auth_bytes = auth_str.encode("utf-8")
    #encoding it to required base64
    auth_base64 = str(base64.b64encode(auth_bytes),"utf-8")

    ## Run the Actual Request with Post, setting up required header fields
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}

    ## actually make the request to Spotify
    result = requests.post(url, headers = headers, data = data)
    json_result = result.json()
    token = json_result["access_token"]
    return token

# Get mandatory header for all documented API request
def get_auth_header(token):
    '''Creates Authorization header with the access token for requests to official Spotify API'''
    header = {
        "Authorization": "Bearer " + token
        }
    return header

############################

## Search for artist_id and return a dictionary of info
def search_artist(token, artist_name):
    '''Search the Artist name and get their info including ID and popularity'''
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)

    querystring = {
                "q": artist_name,
                "type": "artist",
                "limit": 1
                }

    result = requests.request("GET",url, headers= headers, params=querystring)
    
    json_result = result.json()

    try:
        #returns a artist_id, artist name,
        answer = json_result['artists']['items'][0]
        artist_info = {'artist_name':answer['name'],'artist_id':answer['id'], 'artist_followers':answer['followers']['total'], 'artist_popularity':answer['popularity'], 'artist_genres':answer['genres']}
        return artist_info
    except:
        #give error
        print("No artist with this name on Spotify")
        return None


## Request singles and albums by artist_id limited to 50 results each request
def get_singles_albums_by_artist_limit_50(token, artist_id,offset):
    '''Search "album" and "singles" given artist_id limit 50 per request at a time
        Return list of items '''
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
    headers = get_auth_header(token)

    querystring = {
                "include_groups": "album,single",
                "limit": 50,
                "offset": offset
                }

    result = requests.request("GET",url, headers= headers, params=querystring)
    
    json_result = result.json()
    items = json_result['items']
    return items

## Loops get_singles_albums_by_artist_limit_50() and get all the albums and singles of an artist
def get_all_singles_albums_by_artist(token, artist_id):
    '''Grabs all the singles and albums for the artist and return a dataframe
        with album_group, name, id, release_date, total_tracks, uri'''
    offset_counter = 0
    data = []
    while True:
        results = get_singles_albums_by_artist_limit_50(token,artist_id,offset_counter)
        offset_counter += 50
        data.extend(results)

        if len(results) != 50:
            break

    dataframe = pd.DataFrame(data, columns = ["album_group","name","id","release_date","total_tracks",'uri'])
    #drop duplicates
    dataframe = dataframe.drop_duplicates(subset=['name'], keep='first')
    dataframe = dataframe.reset_index(drop=True)
    return dataframe

## Request a single popularity score by album_id
def get_album_single_popularity_by_id(token, single_album_id):
    '''input one single/album id to search and return an popularity score'''

    url = f"https://api.spotify.com/v1/albums/{single_album_id}"
    headers = get_auth_header(token)

    result = requests.request("GET",url, headers= headers)
    
    json_result = result.json()
    popularity_score = json_result['popularity']
    return popularity_score

## Get all the popularity score by looping through each album_id in a given dataframe
def get_all_pop_for_album_single(token,albums_singles_df):
    '''input dataframe of all albums and singles of an artist and use the id column to get the popularity score return updated dataframe'''
    # get the number of rows in the dataframe
    n = len(albums_singles_df.index)
    #create a list of id
    id_list = albums_singles_df['id']
    #create an array of the same size as id to get the popularity score
    pop_score_list = np.empty(n)

    for i in range(len(id_list)):
        pop_score_list[i] = get_album_single_popularity_by_id(token,id_list[i])
    
    albums_singles_df['album_popularity'] = pop_score_list
    return albums_singles_df

## Request the tracks of an album given album_id limited to 50 results each request
def get_tracks_by_album_limit_50(token, single_album_id,offset):
    '''input one single/album id to search and return first 50 tracks in the album'''

    url = f"https://api.spotify.com/v1/albums/{single_album_id}/tracks"
    headers = get_auth_header(token)

    querystring = {
                "limit": 50,
                "offset": offset
                }

    result = requests.request("GET",url, headers= headers, params=querystring)
    
    json_result = result.json()
    items = json_result['items']
    return items

## Loops get_tracks_by_album_limit_50() and get all the tracks for a single album
def get_all_tracks_for_one_album(token, single_album_id):
    '''Grabs all the tracks of the album (function mainly useful if album has more than 50 tracks) and return dataframe with album_id attached'''
    offset_counter = 0
    data = []
    while True:
        results = get_tracks_by_album_limit_50(token,single_album_id,offset_counter)
        offset_counter += 50
        data.extend(results)

        if len(results) != 50:
            break
    
    ##dataframe = pd.DataFrame(data)
    #extract only relevant fields
    dataframe = pd.DataFrame(data, columns = ["name","id",'uri', "track_number"])
    dataframe = dataframe.reset_index(drop=True)
    
    #include album id for easier identification later on
    album_id = np.full(shape = len(dataframe),fill_value = single_album_id)
    dataframe['album_id'] = album_id
    return dataframe

## Loops a list of album_id from a dataframe and return a dataframe of all the tracks with album_id as last column
def get_all_tracks_from_albums(token, albums_singles_df):
    '''Input dataframe of album and singles extract album_id and run get_all_tracks_for_one_album() on for each album_id
        return dataframe of all tracks '''
    # Create empty dataframe to concatenate
    all_tracks = pd.DataFrame()
    album_ids = albums_singles_df['id']
    #loop through each album_id to get all the tracks within
    for i in album_ids:
        #the searched dataframe of one album
        temp = get_all_tracks_for_one_album(token,i)
        #concatenating onto the previous dataframe
        all_tracks = pd.concat([all_tracks,temp], axis = 0)
    all_tracks = all_tracks.reset_index(drop=True)
    return all_tracks

## Request a track's information by their track_id
def get_track_popularity_by_id(token, track_id):
    '''Search the track_id and get their popularity score'''
    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    headers = get_auth_header(token)

    result = requests.request("GET",url, headers= headers)
    
    json_result = result.json()
    popularity_score = json_result['popularity']
    return popularity_score

## Loops through a dataframe of all tracks and get the popularity score and return an updated dataframe
def get_pop_for_all_tracks(token,all_tracks_df):
    '''input dataframe of all tracks and use the id column to get the popularity score return updated dataframe'''
    # get the number of rows in the dataframe
    n = len(all_tracks_df.index)
    #create a list of id
    id_list = all_tracks_df['id']
    #create an array of the same size as id to get the popularity score
    pop_score_list = np.empty(n)

    for i in range(len(id_list)):
        pop_score_list[i] = get_track_popularity_by_id(token,id_list[i])
    
    all_tracks_df['track_popularity'] = pop_score_list
    return all_tracks_df
