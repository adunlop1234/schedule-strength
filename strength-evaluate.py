import pandas as pd
import numpy as np
import sys, os

# Initialise totals
columns = ['Team', 'Win', 'Loss', 'Tie', 'Total']
df_totals = pd.DataFrame(columns=columns)

# Read in current W-L
df_record = pd.read_csv('record.csv', index_col=0)
df_record = df_record.fillna(0)

# Loop over each schedule and add to total
for week in range(1, 18, 1):
    
    # Read schedule for given week
    schedule = pd.read_csv(os.path.join('schedules', 'Schedule_Week_' + str(week) + '.csv'))
    
    # Find all teams played this week
    all_teams = list(schedule.Home) + list(schedule.Away)

    # Initialise totals array if it's week 1
    if week == 1:
        df_totals.Team = all_teams
        df_totals = df_totals.fillna(0)
        df_totals = df_totals.set_index('Team')

    # Loop over each team that played
    for team in all_teams:
        if team in schedule.Home.values:
            opp = schedule.Away[schedule.Home == team].values[0]
        elif team in schedule.Away.values:
            opp = schedule.Home[schedule.Away == team].values[0]

        df_totals.Win[team] += df_record.Win[opp]
        df_totals.Loss[team] += df_record.Loss[opp]
        df_totals.Tie[team] += df_record.Tie[opp]

# Add totals column
df_totals.Total = df_totals.Win + df_totals.Loss + df_totals.Tie

# Sort and output
df_totals = df_totals.sort_values(by=['Win', 'Tie', 'Loss'])
df_totals.to_csv('output.csv')