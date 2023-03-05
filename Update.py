from update_artist_pop import *
from update_album_pop import *
from update_track_pop import *
from func_doc_api import *
import time

# Update for today
update_artist_today()
print("cool down to prevent api lock")
time.sleep(5)
update_album_today()
print("cool down to prevent api lock")
time.sleep(5)
update_track_today()