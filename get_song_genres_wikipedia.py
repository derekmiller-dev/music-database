import pandas as pd
import wikipedia
from wikipedia.exceptions import DisambiguationError, PageError
import urllib.parse
import re

# Build a safe Wikipedia URL from a title
def build_wikipedia_url(title):
    safe_title = title.strip().replace(' ', '_')
    encoded_title = urllib.parse.quote(safe_title)
    return f"https://en.wikipedia.org/wiki/{encoded_title}"

# Load your dataset
df = pd.read_excel("billboard_chart_hot_100_every_song.xlsx")

# Take a sample
# sample_df = df.head(20).copy()
# sample_df["Wikipedia URL"] = None

# Search Wikipedia and build URL
def search_wikipedia(artist, title):
    # query = f"{title} {artist}"
    query = f"{artist} {title}"
    words_of_song = re.findall(r"[a-zA-Z]+", str(title).lower())
    found_index = False
    current_index = None

    try:
        search_results = wikipedia.search(query, results=20)
        for i, item in enumerate(search_results):
            words_of_search_result = str(item).lower()
            # print(all(word in item for word in words_of_song))
            if all(word in words_of_search_result for word in words_of_song):       
                if "song" in str(words_of_search_result).lower():
                    print(f"Query: {query} → Top Result: {search_results[i]}")
                    found_index = True
                    return build_wikipedia_url(search_results[i])
                elif current_index == None:
                    current_index = i
        
        if found_index == False and current_index != None:
            print(f"Query: {query} → Top Result: {search_results[current_index]}")
            return build_wikipedia_url(search_results[current_index])
            
    except Exception as e:
        print(f"Error for query '{query}': {e}")
    return None

# Run search on sample
for i, row in df.iterrows():
    url = search_wikipedia(row["Artist"], row["Song Name"])
    df.at[i, "Wikipedia URL"] = url

# Save to CSV
df.to_csv("sample_with_wikipedia_links.csv", index=False)
print("✅ Saved as sample_with_wikipedia_links.csv")
