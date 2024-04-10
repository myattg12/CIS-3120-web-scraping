import requests
from bs4 import BeautifulSoup
import pandas as pd

# putting multiple websites to scrape
# start using the url to get into the scraping process
urls = [
    'https://lehmanathletics.com/sports/mens-volleyball/roster?view=2',
    'https://johnjayathletics.com/sports/mens-volleyball/roster/',
    'https://athletics.baruch.cuny.edu/sports/mens-volleyball/roster/',
    'https://ccnyathletics.com/sports/mens-volleyball/roster',
    'https://mecathletics.com/sports/mens-volleyball/roster',
    'https://www.huntercollegeathletics.com/sports/mens-volleyball/roster',
    'https://yorkathletics.com/sports/mens-volleyball/roster',
    'https://ballstatesports.com/sports/mens-volleyball/roster'
]

# defining the data/ it is important to create the data frame using pandas in the future
data = []

# Iterate over the URLs
for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # use soup find all to scrape the whole table
    players = soup.find_all('tr')
    
    for player in players:
        # use td and class to get into details with names and heights 
        player_names = player.find('td', class_='sidearm-table-player-name')
        player_heights = player.find('td', class_='height')
        
        # If both name and height elements are found, extract the text
        if player_names and player_heights:
            name = player_names.text.strip()
            height = player_heights.text.strip()
            data.append({'Name': name, 'Height': height})

# Convert data into a DataFrame
df = pd.DataFrame(data)
df['Height'] = df['Height'].str.replace('-', "'") + '"' # Convert to a more uniform format, e.g., 6'5"

# Function to convert height from feet-inches to inches
def height_to_inches(height):
    feet, inches = height.split("'")
    inches = inches.replace('"', '')  # Remove the inch symbol
    return int(feet) * 12 + int(inches)

# Apply the conversion to the DataFrame
df['Height_in_inches'] = df['Height'].apply(height_to_inches)

# started changing to the table and convert into the csv
# Calculate the average height in inches and sort data for analysis
average_height_in_inches = df['Height_in_inches'].mean()
df_sorted = df.sort_values(by='Height_in_inches', ascending=True)
tallest_players = df_sorted.tail(5)
shortest_players = df_sorted.head(5)

# Save to CSV
df.to_csv('men_volleyball.csv', index=False) # convert the dataframe to csv file

# Output results
print(f"The average height of the players across all teams is {average_height_in_inches:.2f} inches.")
print("\nTallest Players:\n", tallest_players[['Name', 'Height']])
print("\nShortest Players:\n", shortest_players[['Name', 'Height']])
print("\nData saved to men_volleyball.csv") # to make sure that is saved to the file




