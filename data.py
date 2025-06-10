from pydoc import describe

import mysql.connector
import pandas as pd

mydb=mysql.connector.connect(
    host='localhost',
    user='root',
    password='Elhockey123',
    port='3306',
    database='hockey_db'


)
#cursor for adding data to database
cursor = mydb.cursor()

csv_columns=''
#the column names gotten from the most recent csv
columns= pd.read_csv('./data/hockey_stat2025.csv').columns
for col in columns:
    csv_columns=csv_columns+ ', ' + col.lower()
csv_columns=csv_columns+', year'
csv_columns=csv_columns[2:]
print(csv_columns)


# the sql column names
cursor.execute("SHOW COLUMNS FROM player_stats")
sql_columns = [row[0] for row in cursor.fetchall()]
print(sql_columns)


#look at every csv
for year in range(1950, 2026):
    try:
        df = pd.read_csv(f'./data/hockey_stat{year}.csv')
        #
        #NEED TO CHECK IF 1950.CSV COLUMNS MATCH THE NAMES OF THE COLUMNS IN COLUMNS VARIABLE - THE VARIABLE WE CHECK AGAINST IS JUST CALLED COLUMNS!
        #

        for row in range(len(df)):
            row_data=''
            for i in df.iloc[row]:
                #need to check if each has the right columns if not set value to null
                row_data=row_data+','+ str(i)
            print(f'INSERT INTO player_stats ({csv_columns}) values ({row_data[1:] +"," +str(year)})')
            cursor.execute(f'INSERT INTO player_stats ({csv_columns}) values ({row_data[1:] +"," +str(year)})')


    except FileNotFoundError:
        print(f"{year}: File not found")



