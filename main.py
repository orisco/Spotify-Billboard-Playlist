from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import os
import pprint

date = input("which date would you like to be transported to? (YYYY-MM-DD) ")

website_url = f"https://www.billboard.com/charts/hot-100/{date}/"

data = requests.get(website_url)

soup = BeautifulSoup(data.text, "html.parser")

all_songs_titles = soup.findAll("li", class_="o-chart-results-list__item")

new_list = [all_songs_titles]

songs = {}

for song in all_songs_titles:
    try:
        title = song.find("h3", class_="c-title", id="title-of-a-story").getText().strip()
        artist = song.find("span", class_="c-label").getText().strip()
        songs[artist] = title
    except AttributeError:
        pass

SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = 'http://example.com'
SCOPE = "playlist-modify-private"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        show_dialog=True,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=SCOPE,
        cache_path="token.txt"
    )
)
user = sp.current_user()['id']

playlist = sp.user_playlist_create(user=user, name=f"{date} Billboard Top 100", public=False)

for song_title in songs:
    year = date.split('-')[0]
    try:
        spotify_song = sp.search(q=f"track:{song_title} year:{year}", limit=1, type='track')
        track = spotify_song['tracks']['items'][0]['uri']
        sp.playlist_add_items(playlist_id=playlist['id'], items=[track])
    except IndexError:
        pass

