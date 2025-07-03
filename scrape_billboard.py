import requests
from bs4 import BeautifulSoup
import csv
import time
from collections import defaultdict
from lxml import html

csv_filename = "billboard_chart_data.csv"

def get_chart_date(url):
    return url.rstrip("/").split("/")[-1]

def format_chart_date(date_str):
    parts = date_str.split("-")
    return f"{int(parts[1])}-{int(parts[2])}-{int(parts[0])}"

def extract_chart_data(tree, chart_date):
    # chart_items = soup.select("li.o-chart-results-list__item")
    chart_data = []

    # Rank Xpath
    # //span[@class='c-label  a-font-primary-bold-l u-font-size-32@tablet u-letter-spacing-0080@tablet']
    # Song Name Xpath
    # //li[contains(@class, 'o-chart-results-list__item')]//h3//text()
    # Artist Nae
    # //span[contains(@class, 'c-label  a-no-trucate')]//text()

    ranks = tree.xpath("//span[@class='c-label  a-font-primary-bold-l u-font-size-32@tablet u-letter-spacing-0080@tablet']//text()")
    titles = tree.xpath("//li[contains(@class, 'o-chart-results-list__item')]//h3//text()")
    artists = tree.xpath("//span[contains(@class, 'c-label  a-no-trucate')]//text()")

    for rank, title, artist in zip(ranks, titles, artists):
        chart_data.append((artist.strip(), title.strip(), rank.strip()))

    return chart_data

def main():

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
    }
    chart_matrix = defaultdict(dict) # { (artist, title): {date: position}}
    all_dates = []

    with open("billboard_hot_100_urls.csv", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        
        for row in reader:
            chart_date = row[0]
            url = row[1]

            print(f"Scraping: {url}")
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f"Failed to Fetch {url}")
                break
            tree = html.fromstring(response.content)
            chart_date_raw = get_chart_date(url)
            chart_date = format_chart_date(chart_date_raw)
            all_dates.append(chart_date)

            chart_data = extract_chart_data(tree, chart_date)

            for artist, title, rank in chart_data:
                chart_matrix[(artist, title)][chart_date] = rank

    all_dates_sorted = sorted(set(all_dates), key = lambda d: time.strptime(d, "%m-%d-%Y"))
    with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Artist", "Song Name"] + all_dates_sorted
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for (artist, title), week_data in chart_matrix.items():
            row = {
                "Artist": artist,
                "Song Name": title,
                **{date: week_data.get(date, "") for date in all_dates_sorted}
            }
            writer.writerow(row)

    print(f"Saved matrix to {csv_filename}")

if __name__ == "__main__":
    main()
