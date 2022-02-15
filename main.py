import requests
import spotipy
from spotipy import SpotifyOAuth
from bs4 import BeautifulSoup

CLIENT_ID = "b5b6c09d55e64cd2a4fbd591903df744"
CLIENT_SECRET = "1c54a26962a747c9bf43dc227e098d76"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

date = input("Please insert the date that you would like to travel to in the following format YYYY-MM-DD:\n")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
billboard_page = response.text

soup = BeautifulSoup(billboard_page, "html.parser")

musics_list = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")
artists_list = soup.find_all(name="span", class_="chart-element__information__artist")

song_artist_list = []

for i in range(len(musics_list)):
    song_artist_list.append((musics_list[i].getText().replace("'", ""), artists_list[i].getText().split("Featuring")[0]))

song_uris = []
year = date.split("-")[0]

search_years = f"{int(year)-1}-{year}"

for (music, artist) in song_artist_list:
    result = sp.search(q=f"track:{music} artist:{artist} year:{search_years}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{music} doesn't exist in Spotify. It was skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
# print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
