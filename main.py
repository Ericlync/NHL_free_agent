from http.client import responses

import mysql.connector
import pandas as pd
import time
import requests
from bs4 import BeautifulSoup
from django.template.defaultfilters import length

#build up the years to be able to loop and scrape each year
years = []
for i in range(1950, 2026):
    years.append(i)

#need to build headers because the http requests are getting blocked
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/114.0.0.0 Safari/537.36"
}

for year in years:
    #hockey-reference has a scraper delay of 3s in its robot.txso set timer to 3 between requests
    time.sleep(3)

    # create a loop to go through each season by changing the "NHL_2025" which each iteration
    url = 'https://www.hockey-reference.com/leagues/NHL_' + str(year) + '_skaters.html'
    response = requests.get(url,headers=headers)
    if response.status_code!=200:
        print(f'Failed to fetch {year}: Status code {response.status_code}')
        continue

    soup = BeautifulSoup(response.content, 'html.parser')

    # trying to build the list of attributes
    header = soup.find("thead")
    if header is None:
        continue
    columns = header.find_all('th')
    over_header = {
        'Scoring',
        'Assists',
        'Shots',
        'Ice Time',
        'Faceoffs',
        'Goals',
        'Rk'
    }
    attributes = []
    for column in columns:
        if column.get_text() not in over_header:
            # print(column.get_text())
            attributes.append(column.get_text())
    attributes = list(filter(bool, attributes))
    print(year)

    # this is for building the players columns
    tbody = soup.find("tbody")
    rows = tbody.find_all('tr')
    data = []
    # getting the data from each row
    # adding data to data list
    for row in rows:
        cells = row.find_all("td")
        cell_text = [cell.get_text(strip=True) for cell in cells]
        data.append(cell_text)

    df = pd.DataFrame(data=data, columns=attributes)
    df.to_csv("./data/hockey_stat" + str(year) + ".csv", index=False)
