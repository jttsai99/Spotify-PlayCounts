from update_artist_pop import *
from update_album_pop import *
from update_track_pop import *
from update_track_playcount import *
import time

# Update for today
try:
    update_track_playcount_today()
except:
    raise ValueError('Undocumented API keys need updating')
update_artist_today()
print("cool down to prevent api lock")
time.sleep(5)
update_album_today()
print("cool down to prevent api lock")
time.sleep(5)
update_track_today()