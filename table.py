import numpy as np
import pandas as pd

def cumulative_table(season, round):

    if not 1 <= round <= 30:
        print('Invalid round number')
    rows_to_read = round*8
    file = pd.read_csv(f'{season}.csv', nrows=rows_to_read)
    
    results = pd.DataFrame(file)
    return results
    

def team_results(team, cumulative_table):

    results[results['Home team'].isin(['Stade Rochelais']) | results['Away team'].isin(['Stade Rochelais'])]
    


#cumulative_table('2008-2009', 5)



