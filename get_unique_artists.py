import csv

input_file = 'billboard_hot_100_songs_with_wikipedia_links.csv'
output_file = 'billboard_hot_100_unique_artists.csv'
column_name = 'Artist'

unique_values = set()

with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
    # EACH row yields a Dictionary, where Column Headers are 'Keys' and Column Values are 'Values'
    # {'Artist': 'The Beatles', 'Song': 'Love Me Do'}
    reader = csv.DictReader(infile)
    for row in reader:
        value = row[column_name].strip()
        if value:
            unique_values.add(value)

with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    # Write Header
    writer.writerow([column_name])
    # Write Values
    for value in sorted(unique_values):
        writer.writerow([value])

print(f"Extracted {len(unique_values)} unique values to '{output_file}'.")