import pandas as  pd

file = 'src\data\csvs\\balanced_goals_and_results2.0.csv'
data = pd.read_csv(file)

statistics_dict = {'home_win': 0, 'draw': 0, 'away_win': 0}

for i, row in data.iterrows():
    if row['home_team_score'] in statistics_dict.keys():
        statistics_dict[row['home_team_score']] += 1
    else:
        statistics_dict[row['home_team_score']] = 1

    if row['away_team_score'] in statistics_dict.keys():
        statistics_dict[row['away_team_score']] += 1
    else:
        statistics_dict[row['away_team_score']] = 1

    if row['away_team_score'] == row['home_team_score']:
        statistics_dict['draw'] += 1
    elif row['away_team_score'] > row['home_team_score']:
        statistics_dict['away_win'] += 1
    else:
        statistics_dict['home_win'] += 1

pass