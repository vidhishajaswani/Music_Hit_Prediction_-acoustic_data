# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 11:37:21 2018

@author: suvod
"""

from __future__ import print_function
import re
import requests
from bs4 import BeautifulSoup as bs
import csv
import pandas as pd
import os
import sys


data_loc = 'data'
col2 = " "
cwd = os.getcwd()
source_file = 'song_dataset_url.csv'
destination_file = 'song_dataset_final.csv'
data_path = os.path.join(cwd, data_loc)
source_file_path = os.path.join(data_path, source_file)
destination_file_path = os.path.join(data_path, destination_file)
df = pd.read_csv(source_file_path)
i = 0
print(df.shape)
links = df['link'].tolist()
artists = df['artist'].tolist()
links = list(zip(links,artists))
print(links)
pos = []
woc = []
k = 0

for link,artist in links:
    try:
        print("Iteration:",k)
        k += 1
        page = requests.get(link)
        print(link)
        
        content = page.content
        
        # Create a BeautifulSoup object
        soup = bs(content, 'html.parser')
        
        
        table = soup.findChildren('table')[0]
        
        rows = table.findChildren('tr')
        
        j = 0
        found = False
        col2 = ""
        for row in rows:
            cells = row.findChildren('td')
            i = 0
            for cell in cells:
                cell_content = cell.getText()
                clean_content = re.sub( '\s+', ' ', cell_content).strip()
                #print(clean_content)
                i = i + 1
                if "Sorry, there are no Official Singles Chart results" in clean_content:
                    print(0)
                    print(0)
                    found = True
                    pos.append('0')
                    woc.append('0')
                #if i in [5,4,3]:
                    #print(clean_content)
                if i == 2:
                    col2 = clean_content
                if artist.upper() in col2:
                    found = True
                    if i == 3:
                        pos.append(clean_content)
                        j += 1
                        print(clean_content)
                    elif i == 4:
                        woc.append(clean_content)
                        j += 1
                        print(clean_content)

            if j >= 2:
                break
        if not found:
            print(0)
            print(0)
            pos.append('0')
            woc.append('0')
        print("+++++++++++++++++++++++++++++++++++++++++++++++")
    except IndexError:
        print(0)
        print(0)
        pos.append('0')
        woc.append('0')
        continue
    except Exception:
        print("Unexpected error:", sys.exc_info()[0])
        print(0)
        print(0)
        pos.append('0')
        woc.append('0')
        continue
#artist_name_list1 = soup.find(class_='chart-results-content')
#artist_name_list2 = soup.find
#artist_name_list_items = artist_name_list1
df['Peak_Pos'] = pd.DataFrame(data = pos)
df['WoC'] = pd.DataFrame(data = woc)
#df.drop(['Unnamed: 0'], axis = 1, inplace = True)
df.to_csv(destination_file_path, encoding =  'utf-8')

#print(artist_name_list1.prettify())
#
#for artist_name in artist_name_list_items:
#    names = artist_name.contents[0]
#    print(names)