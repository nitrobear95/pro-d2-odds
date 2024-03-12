import requests
import matplotlib as plt
from bs4 import BeautifulSoup as bs
import pandas as pd

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
rounds = ['j1',
 'j2',
 'j3',
 'j4',
 'j5',
 'j6',
 'j7',
 'j8',
 'j9',
 'j10',
 'j11',
 'j12',
 'j13',
 'j14',
 'j15',
 'j16',
 'j17',
 'j18',
 'j19',
 'j20',
 'j21',
 'j22',
 'j23',
 'j24',
 'j25',
 'j26',
 'j27',
 'j28',
 'j29',
 'j30']

for i in range(len(seasons)):
    season_df = pd.DataFrame()

    for j in range(len(rounds)):

        url = f'https://prod2.lnr.fr/calendrier-et-resultats/{seasons[i]}/{rounds[j]}?'
        response = requests.get(url)
        soup = bs(response.text, 'html.parser')

        ### find teams ###
        home_teams = soup.find_all('div', class_="club-line club-line--reversed club-line--table-format")
        home_list = []
        for team in home_teams:
            team = team.find('a', class_="club-line__name base-link base-link--black")
            home_list.append(team.text.strip())

        away_teams = soup.find_all('div', class_="club-line club-line--table-format")
        away_list = []
        for team in away_teams:
            team = team.find('a', class_="club-line__name base-link base-link--black")
            away_list.append(team.text.strip())

        ### find bonus points ###
        bonus_points = soup.find_all('div', class_='match-line')
        home_bonus = [1 if bonus.find('div', class_="match-line__result match-line__result--left") or bonus.find('div', class_= "match-line__result match-line__result--left match-line__result--right") else 0 for bonus in bonus_points]
        away_bonus = [1 if bonus.find('div', class_="match-line__result match-line__result--right") or bonus.find('div', class_= "match-line__result match-line__result--left match-line__result--right") else 0 for bonus in bonus_points]

        ### find scores ###
        results = soup.find_all('div', class_='match-line__score')
        home_score = []
        away_score = []
        for result in results:
            result = result.text.strip()
            home_score.append(int(result[0:2]))
            away_score.append(int(result[-2:]))

        ### compile and save df as csv ###
        gameweek_df = pd.DataFrame({'Round': j+1,
                    'Home team': home_list,
                    'Home score': home_score,
                    'Away score': away_score,
                    'Away team': away_list,
                    'Home bonus': home_bonus,
                    'Away bonus': away_bonus
                    })

        season_df = pd.concat([season_df, gameweek_df], ignore_index=True)
        print(f'Round {rounds[j]} completed')
        # print(season_df)

    season_df.to_csv(f'{seasons[i]}.csv', index=False)
    print(f'Season {seasons[i]} completed')

    # print(season_df)
