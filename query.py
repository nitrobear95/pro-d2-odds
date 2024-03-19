#!/usr/bin/env python3
import os

import numpy as np
import pandas as pd

import util


SEASONS = ['2008-2009',
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

def cumulative_table(season, round: int):
    """
    Shows the table from any point during the season
    """

    ### open csv and put in df ###
    if not 1 <= round <= 30:
        print('Invalid round number')
    rows_to_read = round*8
    file = pd.read_csv(f'data/{season}.csv', nrows=rows_to_read)
    results = pd.DataFrame(file)
    team_stats = {}

    ### Update team statistics based on the results ###
    for index, row in results.iterrows():
        home_team = row['Home team']
        away_team = row['Away team']
        '\n'
        '\r\n'


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
    for stats in team_stats.values():
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

    if not 1 <= round_start <= 30:
        raise ValueError('Error: round_start number out of range')
    if not 1 <= round_end <= 30:
        raise ValueError('Error: round_end number out of range')
    if round_end <= round_start:
        raise ValueError('Error: round_end must be larger than round_end')

    df = pd.read_csv(f'data/{season}.csv')
    all_teams = util.get_all_teams(df)
    full_team = util.figure_out_team(team, all_teams)

    filtered_df = df[(df['Home team'] == full_team) | (df['Away team'] == full_team)]
    filtered_df = filtered_df[(filtered_df['Round'] >= round_start) & (filtered_df['Round'] <= round_end)]

    return filtered_df

def win_percentages(team):
    home_wins = 0
    away_wins = 0
    home_matches = 0
    away_matches = 0
    total_seasons = 0
    all_dfs = [] #pd.DataFrame()
    all_teams = set()

    for season in SEASONS:
        df = pd.read_csv(f'data/{season}.csv')
        current_teams = util.get_all_teams(df)
        all_teams |= current_teams
        all_dfs.append(df)# = pd.concat([all_dfs, df], axis=0)

    team = util.figure_out_team(team, all_teams)
    for df in all_dfs:
        filtered_df = df[df['Home team'] == team]
        filtered_df2 =  df[df['Away team'] == team]
        if not filtered_df.empty:
            total_seasons += 1
            home_wins += (filtered_df['Home score'] > filtered_df['Away score']).sum()
            home_matches += len(filtered_df)
        if not filtered_df2.empty:
            away_wins += (filtered_df2['Home score'] < filtered_df2['Away score']).sum()
            away_matches += len(filtered_df2)
    home_win_percentage = (home_wins / home_matches) * 100
    away_win_pc = (away_wins / away_matches) * 100

    print(f'{team} won {home_win_percentage:.2f}% ofthe time at home over {total_seasons} of {len(SEASONS)} seasons, and {away_win_pc:.2f}% away')
    return home_win_percentage, away_win_pc





def main():
    # cumulative_table('2008-2009', 25)
    # print(team_query("Auri", '2008-2009', 12, 5))
    win_percentages('Auch')

if __name__ == '__main__':
    main()





