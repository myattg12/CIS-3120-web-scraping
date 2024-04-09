#!/usr/bin/env python
# coding: utf-8

# In[2]:


import requests
from bs4 import BeautifulSoup
import pandas as pd

# putting mutiple websites to scrape
# start using the url to get into the scraping process
#change the website details as I have changed to women's team roster
urls = [
    'https://bmccathletics.com/sports/womens-volleyball/roster?view=2',
    'https://yorkathletics.com/sports/womens-volleyball/roster',
    'https://hostosathletics.com/sports/womens-volleyball/roster',
    'https://bronxbroncos.com/sports/womens-volleyball/roster/2021','https://queensknights.com/sports/womens-volleyball/roster',
    'https://augustajags.com/sports/wvball/roster',
    'https://flaglerathletics.com/sports/womens-volleyball/roster','https://pacersports.com/sports/womens-volleyball/roster',
    'https://www.golhu.com/sports/womens-volleyball/roster'
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
            data.append({'Name': name  , 'Height': height })

# started changing to the table and convert into the csv
df = pd.DataFrame(data)
df['Height'] = df['Height'].str.replace('-', "'") + '"' # put in 5'-5" as a sample. 
print(df)# to see the whole list of names and heights
df.to_csv('women_volleyball.csv') #conver the dataframe to csv file
print('saved to file') #to make sure that is saved to the file


# In[ ]:




