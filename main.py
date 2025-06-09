from http.client import responses

import mysql.connector

import requests
from bs4 import BeautifulSoup

url = 'https://www.hockey-reference.com/leagues/NHL_2025_skaters.html'

response=requests.get(url)
soup= BeautifulSoup(response.content,'html.parser')


##print(soup.prettify())

