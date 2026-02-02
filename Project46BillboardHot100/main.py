from datetime import datetime
import requests
from bs4 import BeautifulSoup
import os
from pprint import pprint
import spotipy
from spotipy.oauth2 import SpotifyOAuth,SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()

URL = "https://en.wikipedia.org/wiki/Category:Lists_of_Billboard_Year-End_Hot_100_singles"

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                        "(KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"}

response = requests.get(url=URL, headers=header)
response.encoding = 'utf-8'

soup = BeautifulSoup(response.text, 'html.parser')

years = [int(a.text[-4:]) for a in soup.select('div.mw-category-group a')]

print(years)

while True:
    date_input = input(
        "Which year do you want to travel to? Type the date in this format YYYY-MM-DD\n"
    )

    try:
        date = datetime.strptime(date_input, "%Y-%m-%d")
        year = date.strftime("%Y")

        if int(year) in years:
            break
        else:
            print("This year is not available in the Billboard list.")

    except ValueError:
        print("Invalid input. Use this format YYYY-MM-DD (ex: 2015-06-21).")

print(year)
URL2 = f"https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_{year}"

response = requests.get(url=URL2, headers=header)
response.encoding = 'utf-8'

soup = BeautifulSoup(response.text, 'html.parser')

titles = []
artists = []

# songs_of_the_year = [row.get_text() for row in soup.select('table.wikitable tbody tr')]

for row in soup.select('table.wikitable tbody tr'):
    cols = row.find_all('td')

    title_cell = row.select_one('td:nth-of-type(2)')
    artist_cell = row.select_one('td:nth-of-type(3)')

    if title_cell and artist_cell:
        title = title_cell.get_text().strip('"')
        artist = artist_cell.get_text()

        titles.append(title)
        artists.append(artist)

print(titles)
print(artists)

SPOTIFY_CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]
SPOTIFY_REDIRECT_URI = os.environ["SPOTIFY_REDIRECT_URI"]
SPOTIFY_DISPLAY_NAME = os.environ["SPOTIFY_DISPLAY_NAME"]

spotify = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=SPOTIFY_REDIRECT_URI,
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
        username="YOUR SPOTIFY DISPLAY NAME",
    )
)
user_id = spotify.current_user()["id"]
print("Collecting songs URIs")

songs_uris = []
add = 0
for songs in titles:
    results = spotify.search(q=f'track: {songs} year: {year} artist: {artists[add]}', type='track')
    items = results['tracks']['items']
    try:
        uri = results['tracks']['items'][0]['uri']
        songs_uris.append(uri)
    except IndexError:
        print(f"{songs} not found. Skipped.")
    add += 1

print(songs_uris)

playlist_name = f"{date_input} Billboard 100"

playlists = spotify.user_playlists(user_id, limit=100, offset=0)

playlist_exists = False
playlist_id = None

for playlist in playlists['items']:
    if playlist['name'].lower() == playlist_name.lower():
        playlist_exists = True
        playlist_id = playlist['id']
        print("Playlist already exists:", playlist['name'])
        break

if not playlist_exists:
    new_playlist = spotify.user_playlist_create(
        user_id,
        playlist_name,
        public=False,
        collaborative=False,
        description=''
    )
    playlist_id = new_playlist['id']
    print(f"Playlist created: {playlist_name}\nID: {playlist_id}")

spotify.playlist_add_items(playlist_id, songs_uris)