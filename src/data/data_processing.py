import pandas as pd
from sklearn import preprocessing
from sklearn import preprocessing
from scipy.stats import logistic
from sklearn.utils import resample

# TODO
# Original dataset
# Remove outliers
# Balance

# Training:
# Load dataset and preprocess
#   - encode
#   - split to train and val
# Train model

file =('src/data/csvs/international_matches.csv')
data = pd.read_csv(file)

columns_to_drop = [
    'home_team_goalkeeper_score', 'away_team_goalkeeper_score', 'home_team_mean_defense_score', 'away_team_mean_defense_score', 
    'home_team_mean_offense_score', 'away_team_mean_offense_score', 'home_team_mean_midfield_score', 'away_team_mean_midfield_score',
    'shoot_out', 'home_team_total_fifa_points', 'away_team_total_fifa_points', 'city', 'country', 'tournament',  'Unnamed: 0', 'Unnamed: 0.1',
    ]

columns_to_drop_filtered = []
for column in columns_to_drop:
    if column in data.columns:
        columns_to_drop_filtered.append(column)

columns_to_drop = columns_to_drop_filtered

#drop columns that are not needed/target value columns
data = data.drop(labels=columns_to_drop, axis=1)



#convert date to float
dates = []
for i in range(len(data['date'])):
    dates.append(data['date'][i].split('-')[0])
data['date'] = dates

# data.to_csv('src/data/csvs/original.csv')

filtered_df = data[(data['home_team_score'] <= 7)]
filtered_df = filtered_df[(filtered_df['away_team_score'] <= 7)]
filtered_df.to_csv('src/data/csvs/removed_outliers.csv')

data = filtered_df

balanced_data = pd.DataFrame()

# Define the number of samples you want for each combination of 'home_team_score' and 'away_team_score'
samples_per_combination = 1000

# Iterate over unique combinations of 'home_team_score' and 'away_team_score'
for i in range(10):
    for j in range(10):
        # Filter rows where 'home_team_score' equals the current value of 'i' and 'away_team_score' equals 'j'
        filtered_rows = data[(data['home_team_score'] == i) & (data['away_team_score'] == j)]

        # If there are more than 'samples_per_combination' rows, randomly sample 'samples_per_combination' rows
        if len(filtered_rows) > samples_per_combination:
            sampled_rows = resample(filtered_rows, n_samples=samples_per_combination, random_state=42)
        else:
            # If there are fewer than 'samples_per_combination' rows, include all of them
            sampled_rows = filtered_rows

        # Concatenate the sampled rows to the balanced_data DataFrame
        balanced_data = pd.concat([balanced_data, sampled_rows])

# Reset the index of the balanced_data DataFrame
balanced_data = balanced_data.reset_index(drop=True)

data = pd.DataFrame()

filtered_wins = balanced_data[balanced_data['home_team_score'] > balanced_data['away_team_score']]
if len(filtered_wins) > 3000:
    sampled_rows = resample(filtered_wins, n_samples=3000, random_state=42)
else:
    sampled_rows = filtered_wins
data = pd.concat([data, sampled_rows])

filtered_losses = balanced_data[balanced_data['home_team_score'] < balanced_data['away_team_score']]
if len(filtered_losses) > 3000:
    sampled_rows = resample(filtered_losses, n_samples=3000, random_state=42)
else:
    sampled_rows = filtered_losses
data = pd.concat([data, sampled_rows])

filtered_draws = balanced_data[balanced_data['home_team_score'] == balanced_data['away_team_score']]
if len(filtered_draws) > 4000:
    sampled_rows = resample(filtered_draws, n_samples=4000, random_state=42)
else:
    sampled_rows = filtered_draws
data = pd.concat([data, sampled_rows])

data.to_csv('src/data/csvs/balanced_goals_and_results2.0.csv')