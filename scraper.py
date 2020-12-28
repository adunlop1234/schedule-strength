'''
Set of scripts that scrapes all weekly offence, kicker and 
defence player data from https://fantasy.nfl.com.
'''

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import datetime
import sys, os

def main():
    for week in range(1, 18, 1):
        scrape_schedule(week)


# Function to return the schedule for a given week in the future. 
# Previous weeks don't work or weeks with undefined times.
def scrape_schedule(week):

    # Define the URL for the week in question
    URL = 'https://www.espn.co.uk/nfl/fixtures/_/week/1'.replace('week/1', 'week/' + str(week))

    # Get page
    page = requests.get(URL, allow_redirects=True)

    # Parse the html using soup
    soup = BeautifulSoup(page.content, 'html.parser')

    # Define the headings
    columns = ['Home', 'Away', 'Day', 'Time']

    # Initialise the dataframe
    df = pd.DataFrame(columns = columns)

    # Find the rows
    rows = soup.find_all('tr', class_=re.compile('^(even|odd)$'))

    # Scrape home, away, day, time, early, mid, late, mnf, tnf
    for row in rows:
        
        # Skip byeweeks
        if len(row) == 1:
            continue

        # Find the home and away team abbreviation
        teams = [team.getText() for team in row.find_all('abbr')]
        home, away = teams
        
        # Identify the datatime and split into day and time - all in GMT
        try:
            date, time = row.find('td', {'data-behavior' : 'date_time'})['data-date'].split('T')
            year, month, day = date.split('-')
            day = datetime.date(int(year), int(month), int(day)).strftime("%a")
            time = time.split('Z')[0]
        except TypeError:
            print('WARNING: Scraping schedule after the initial game has been played.')
            day = 'N/A'
            time = 'N/A'

        # Pandas dict for entry
        new_dict = {'Home' : home,
                    'Away' : away,
                    'Day' : day,
                    'Time' : time}

        # Add to the pandas dataframe
        df = df.append(new_dict, ignore_index = True)

    # Write csv output file
    df.to_csv(os.path.join('schedules', 'Schedule_Week_' + str(week) + '.csv'))

    return df

if __name__ == "__main__":
    main()