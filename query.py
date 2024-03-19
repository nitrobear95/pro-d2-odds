#!/usr/bin/env python3
import numpy as np
import pandas as pd
import os

def cumulative_table(season, round: int):

    ### open csv and put in df ###
    if not 1 <= round <= 30:
        print('Invalid round number')
    rows_to_read = round*8
    file = pd.read_csv(f'{season}.csv', nrows=rows_to_read)
    results = pd.DataFrame(file)
    team_stats = {}

    ### Update team statistics based on the results ###
    for index, row in results.iterrows():
        home_team = row['Home team']
        away_team = row['Away team']

        if home_team not in team_stats:
            team_stats[home_team] = {'Wins': 0, 'Draws': 0, 'Losses': 0, 'Points Scored': 0, 'Points Against': 0, 'Bonus Pts': 0, 'Total Points': 0}
        if away_team not in team_stats:
            team_stats[away_team] = {'Wins': 0, 'Draws': 0, 'Losses': 0, 'Points Scored': 0, 'Points Against': 0, 'Bonus Pts': 0, 'Total Points': 0}

        if row['Home score'] > row['Away score']:
            team_stats[home_team]['Wins'] += 1
            team_stats[away_team]['Losses'] += 1
        elif row['Home score'] < row['Away score']:
            team_stats[away_team]['Wins'] += 1
            team_stats[home_team]['Losses'] += 1
        else:
            team_stats[home_team]['Draws'] += 1
            team_stats[away_team]['Draws'] += 1

        team_stats[home_team]['Points Scored'] += row['Home score']
        team_stats[away_team]['Points Scored'] += row['Away score']
        team_stats[home_team]['Points Against'] += row['Away score']
        team_stats[away_team]['Points Against'] += row['Home score']
        team_stats[home_team]['Bonus Pts'] += row['Home bonus']
        team_stats[away_team]['Bonus Pts'] += row['Away bonus']

    ### Calculate total points for each team ###
    for team, stats in team_stats.items():
        stats['Total Points'] = (stats['Wins'] * 4) + (stats['Draws'] * 2) + stats['Bonus Pts']

    ### Create a DataFrame for the league table ###
    league_table = pd.DataFrame(team_stats).T.reset_index()
    league_table = league_table.rename(columns={'index': 'Team'}).sort_values(by='Total Points', ascending=False).reset_index(drop=True)
    league_table['Position'] = league_table.index + 1
    league_table['PD'] = league_table['Points Scored'] - league_table['Points Against']
    league_table = league_table[['Position', 'Team', 'Wins', 'Draws', 'Losses', 'Points Scored', 'Points Against', 'PD', 'Bonus Pts', 'Total Points']]

    # print(league_table.to_string(index=False))
    return league_table.to_string(index=False)

### query a team's results in any set of gameweeks in a given season ###
def team_query(team, season, round_end=30, round_start=1):
    """
    query a team's blah blah blah
    """

    df = pd.read_csv(f'{season}.csv')

    if not df['Home team'].isin([team]).any() and not df['Away team'].isin([team]).any():
        print(f'Invalid team: Valid teams are {[team for team in df["Home team"][:8]]+[team for team in df["Away team"][0:8]]}')

    if round_end > 30:
        print('Error: round number out of range')
    elif round_start < 1:
        print('Error: round number out of range')

    filtered_df = df[(df['Home team'].str.contains(team)) | (df['Away team'].str.contains(team))]
    filtered_df = filtered_df[(filtered_df['Round'] >= round_start) & (filtered_df['Round'] <= round_end)]

    # print(filtered_df)
    return filtered_df

def home_win_percentage(team):
    seasons = ['2008-2009',
               '2009-2010',
               '2010-2011',
               '2011-2012',
               '2012-2013',
               '2013-2014',
               '2014-2015',
               '2015-2016',
               '2016-2017',
               '2017-2018',
               '2018-2019',
               '2020-2021',
               '2021-2022',
               '2022-2023']
    home_wins = 0
    matches = 0
    total_seasons = 0
    for season in seasons:

        df = pd.read_csv(f'{season}.csv')
        filtered_df = df[df['Home team'].str.contains(team)]

        if not filtered_df.empty:
            total_seasons += 1
            home_wins += (filtered_df['Home score'] > filtered_df['Away score']).sum()
            matches += len(filtered_df)

    win_percentage = (home_wins / matches) * 100

    # print(f'{team} won {win_percentage:.2f}% ofthe time at home over {total_seasons} seasons')
    return win_percentage

def main():
    cumulative_table('2008-2009', 25)
    team_query('Auch', '2008-2009', 12, 5)
    home_win_percentage('Auch')

if __name__ == '__main__':
    main()
