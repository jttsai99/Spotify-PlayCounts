import pandas as pd
import requests
from dotenv import load_dotenv
import os
import numpy as np
from tqdm import tqdm

# Get configuration file that has all the api tokens
def configure_undoc():
    load_dotenv()
    UNDOC_AUTHORIZATION = (os.getenv('UNDOC_AUTHORIZATION'))
    UNDOC_CLIENT_TOKEN = (os.getenv('UNDOC_CLIENT_TOKEN'))
    return UNDOC_AUTHORIZATION, UNDOC_CLIENT_TOKEN

# Get album playcount return track_uri list and playcount list
def request_album_playcounts(UNDOC_AUTHORIZATION,UNDOC_CLIENT_TOKEN,album_ID):
    '''Search ID of albums and return response to get playcounts and track_uri'''
    url = "https://api-partner.spotify.com/pathfinder/v1/query"

    querystring = {
                "operationName":"queryAlbumTracks",
                "variables":'{\"uri\":\"spotify:album:' +album_ID+ '\",\"offset\":0,\"limit\":300}',
                "extensions":"{\"persistedQuery\":{\"version\":1,\"sha256Hash\":\"f387592b8a1d259b833237a51ed9b23d7d8ac83da78c6f4be3e6a08edef83d5b\"}}"
                }

    headers = {
    "authority": "api-partner.spotify.com",
    "accept": "application/json",
    "accept-language": "en",
    "app-platform": "WebPlayer",
    "authorization":"Bearer {}".format(UNDOC_AUTHORIZATION),
    "client-token": str(UNDOC_CLIENT_TOKEN),
    "content-type": "application/json;charset=UTF-8",
    "origin": "https://open.spotify.com",
    "referer": "https://open.spotify.com/"
}

    #prcoessing the result
    result = requests.request("GET", url, headers=headers, params=querystring)
    json_result = result.json()
    #getting each track object
    items = json_result['data']['albumUnion']['tracks']['items']
    
    # get the number of items to determine the loop size
    n = len(items)
    track_uri_list = np.empty(n, dtype=object)
    playcount_list = np.empty(n)
    for i in range(n):
        track_uri_list[i] = items[i]['track']['uri']
        playcount_list[i] = items[i]['track']['playcount']

    return track_uri_list, playcount_list

# Create a dataframe with current play counts of single album
def get_today_playcounts(UNDOC_AUTHORIZATION,UNDOC_CLIENT_TOKEN,album_ID):
    '''Using the undocumented API to request playcounts and return a dataframe of '''
    track_uri_list, playcount_list = request_album_playcounts(UNDOC_AUTHORIZATION,UNDOC_CLIENT_TOKEN,album_ID)
    df = pd.DataFrame({'track_uri':track_uri_list, 'playcount':playcount_list})
    df['date_tracked'] = pd.Timestamp.today().strftime('%Y-%m-%d')
    return df

## Loops through a dataframe of all albums and get playcounts of each track and return an updated dataframe
def get_all_playcounts_today(UNDOC_AUTHORIZATION,UNDOC_CLIENT_TOKEN,albums_ids):
    '''Takes in array of album_ids and loop through each one to get a dataframe to be able to append to SQL database'''
    dataframe = pd.DataFrame()
    for id in tqdm(albums_ids, desc = "Updating track playcounts"):
        temp = get_today_playcounts(UNDOC_AUTHORIZATION,UNDOC_CLIENT_TOKEN,id)
        dataframe = pd.concat([dataframe,temp], axis = 0)
    dataframe  = dataframe.reset_index(drop=True)
    return dataframe