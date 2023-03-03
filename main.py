from doc_api import *

CLIENT_ID, CLIENT_SECRET= configure()
token = get_token(CLIENT_ID,CLIENT_SECRET)

#search for artist
artist = search_artist(token, "martin garrix")
artist_id = artist['artist_id']
print(artist)
# #get all artist's album
# all_artist_albums = get_all_singles_albums_by_artist(token, artist_id)
# #get all popularity for albums
# all_artist_albums = get_all_pop_for_album_single(token, all_artist_albums)

# #get all tracks and put into dataframe 
# all_tracks_df = get_all_tracks_from_albums(token, all_artist_albums)
# #get popularity score of all tracks
# all_tracks_df = get_pop_for_all_tracks(token,all_tracks_df)
# print(all_tracks_df)