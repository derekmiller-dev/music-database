import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time

# Set up Spotify API
client_id = 'c275ff1df0754d72a5662e869b85a0fb'
client_secret = '4190b1c368d34475be252430164f186c'
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id, client_secret))

# Load your CSV
df = pd.read_csv("billboard_chart_data.csv")  # adjust filename if needed

# Prepare new columns
df['Primary Genre'] = None
df['Secondary Genre'] = None

# Loop through each song-artist pair
for i, row in df.iterrows():
    query = f"track:{row['Song Name']} artist:{row['Artist']}"
    try:
        results = sp.search(q=query, type='track', limit=1)
        if results['tracks']['items']:
            artist_id = results['tracks']['items'][0]['artists'][0]['id']
            artist_info = sp.artist(artist_id)
            genres = artist_info['genres']
            df.at[i, 'Primary Genre'] = genres[0] if len(genres) > 0 else None
            df.at[i, 'Secondary Genre'] = genres[1] if len(genres) > 1 else None
            print(f"{row['Artist']}: {genres[0] if len(genres) > 0 else None} | {genres[1] if len(genres) > 1 else None}")
    except Exception as e:
        print(f"Error processing {row['Artist']} - {row['Song Name']}: {e}")
    time.sleep(0.2)  # avoid hitting rate limits

# Save enriched CSV
df.to_csv("billboard_with_genres.csv", index=False)
print("Genre enrichment complete.")
