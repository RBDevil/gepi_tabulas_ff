import pickle
import os
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import RadiusNeighborsClassifier
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score
from sklearn import preprocessing


out_dir = 'experiments/balanced_goals_linear_and_results2.0'
os.mkdir(out_dir)
file = 'src\data\csvs\\balanced_goals_and_results2.0.csv'

data = pd.read_csv(file)
data = data.drop(columns=['Unnamed: 0'], axis=1)

def encode_column(data, column_name):
    encoder = preprocessing.LabelEncoder()
    dic = {}
    keys = data[column_name]
    data[column_name] = encoder.fit_transform(data[column_name])
    for i in range(len(data[column_name])):
        dic[keys[i]] = data[column_name][i]
    return dic

home_team_dic = encode_column(data, 'home_team')
with open('home_team_dict.pickle', 'wb') as handle:
    pickle.dump(home_team_dic, handle)
away_team_dic = encode_column(data, 'away_team')
with open('away_team_dict.pickle', 'wb') as handle:
    pickle.dump(away_team_dic, handle)
# data['away_team'] = away_team_dic
home_team_continent_dic = encode_column(data, 'home_team_continent')
with open('home_team_continent_dict.pickle', 'wb') as handle:
    pickle.dump(home_team_continent_dic, handle)
# data['home_team_continent'] = home_team_continent_dic
away_team_continent_dic = encode_column(data, 'away_team_continent')
with open('away_team_continent_dict.pickle', 'wb') as handle:
    pickle.dump(away_team_continent_dic, handle)
# data['away_team_continent'] = away_team_continent_dic

#split train test data 70/30
#define target values
Y = data[['home_team_score', 'away_team_score']]
#drop score columns
data = data.drop(columns=['home_team_score', 'away_team_score', 'home_team_result'])
#split
x_train, x_test, y_train, y_test = train_test_split(data, Y)
#create models
model = LinearRegression()

#fit models
model.fit(x_train, y_train)
with open(f'{out_dir}/log.txt', 'w') as writer:
    writer.write(f'model: {str(model.__class__)}\n')
    writer.write(f'data: {file}\n')

#predict then round values
predict = model.predict(x_test)
for i in range(len(predict)):
    predict[i][0] = round(predict[i][0])
    predict[i][1] = round(predict[i][1])

#calculate score based on goals
correct_score = 0
for i in range(len(predict)):
    if predict[i][0] == y_test['home_team_score'].values[i] and predict[i][1] == y_test['away_team_score'].values[i]:
        correct_score += 1

score = correct_score / len(predict)
with open(f'{out_dir}/log.txt', 'a') as writer:
    writer.write(f'{str(score)}\n')
print(score)

# Lists to store predicted and actual results
predicted_results = []
actual_results = []

for i in range(len(predict)):
    # Predicted result
    if predict[i][0] > predict[i][1]:
        predicted_result = 'Win'
    elif predict[i][0] < predict[i][1]:
        predicted_result = 'Lose'
    else:
        predicted_result = 'Draw'
    
    # Actual result
    if y_test['home_team_score'].values[i] > y_test['away_team_score'].values[i]:
        actual_result = 'Win'
    elif y_test['home_team_score'].values[i] < y_test['away_team_score'].values[i]:
        actual_result = 'Lose'
    else:
        actual_result = 'Draw'

    # Append predicted and actual results to the respective lists
    predicted_results.append(predicted_result)
    actual_results.append(actual_result)

# Calculate accuracy
accuracy = accuracy_score(actual_results, predicted_results)

# Calculate precision for each class
precision = precision_score(actual_results, predicted_results, average=None, labels=['Win', 'Lose', 'Draw'])

# Print accuracy and precision for each class
print(f"Accuracy: {accuracy}")
print("Precision for each class:")
for label, prec in zip(['Win', 'Lose', 'Draw'], precision):
    print(f"{label}: {prec}")


with open(f'{out_dir}/log.txt', 'a') as writer:
    writer.write(f'Accuracy: {accuracy}\n')
    writer.write("Precision for each class:\n")
    for label, prec in zip(['Win', 'Lose', 'Draw'], precision):
        writer.write(f"\t{label}: {prec}\n")

with open(f'{out_dir}/model.pkl', 'wb') as f:
    pickle.dump(model, f)


