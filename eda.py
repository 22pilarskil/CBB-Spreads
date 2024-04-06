import pandas as pd 
import json
import os
import seaborn as sn
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_absolute_error

#covariance matrix
def covariance_matrix(cov_df):
    cov_matrix = cov_df.cov()
    sn.heatmap(cov_matrix, annot=True, fmt='g')
    plt.show()

#corrlelation matrix
def correlation_matrix(df):
    matrix = df.corr()
    cor_target = abs(matrix['score-diff'])
    #Selecting highly correlated features
    relevant_features = cor_target[cor_target>=0.25]
    relevant_features = relevant_features.sort_values(kind = "quicksort")
    print(relevant_features)
    #plotting correlation matrix 
    plt.imshow(matrix, cmap='Blues')

    #adding colorbar 
    plt.colorbar()

    #extracting variable names 
    variables = []
    for i in matrix.columns:
        variables.append(i)

    # Adding labels to the matrix
    plt.xticks(range(len(matrix)), variables, rotation=45, ha='right')
    plt.yticks(range(len(matrix)), variables)

    # Display the plot
    plt.show()

# feature selection
def select_features(X_train, y_train, X_test, input_features):
 # configure to select a subset of features
 fs = SelectKBest(score_func=f_classif, k=7)
 
 # learn relationship from training data
 fs.fit(X_train, y_train)
 print(fs.get_feature_names_out(input_features))
 # transform train input data
 X_train_fs = fs.transform(X_train)
 # transform test input data
 X_test_fs = fs.transform(X_test)
 return X_train_fs, X_test_fs, fs


# assign directory
directory = 'dataset_mens'
 
# iterate over files in
# that directory
list_data = []
columns = []
fileCount = 1
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        jf = open(f, "r")
        data = json.loads(jf.read())
        
        
        #maxPlayerCount = min(len(data[0]['stats']), len(data[1]['stats']))
        maxPlayerCount = 8
        currList = []
        home_or_away = ""
        home_score = 0
        away_score = 0
        for i in range(len(data)):
            if data[i]['home'] == True:
                home_or_away = "home"
                home_score = data[i]['score']
            else:
                home_or_away = 'away'
                away_score = data[i]['score']
            for key in data[i]:
                if key == 'stats':
                    playerCount = 1
                    for player in data[i]['stats']:
                        for stat in data[i]['stats'][player]:
                           if fileCount == 1:
                               columns.append("team-" + home_or_away + "-player" + str(playerCount) + "-" + stat)
                           currList.append(data[i]['stats'][player][stat])
                        if playerCount > maxPlayerCount:
                            break
                        playerCount += 1
                else:
                    if fileCount == 1:
                        if key == 'home':
                            columns.append(home_or_away + "-marker")
                        else:
                            columns.append(key + "-" + home_or_away)
                    # if key == 'home' and data[i][key] == True:
                    #     currList.append(1)
                    # elif key == 'home' and data[i][key] == False:
                    #     currList.append(0)
                    # else:
                    
                    currList.append(data[i][key])

        directory2 = "dataset_mens_diff"
        filename = filename.partition(".json")[0]
        for diffilename in os.listdir(directory2):
            if diffilename.find(filename) >= 0:
                f = os.path.join(directory2, diffilename)
                # checking if it is a file
                if os.path.isfile(f):
                    jf = open(f, "r")
                    data = json.loads(jf.read())
                    for key in data['sorted_stats_diff']:
                        for i in range(min(maxPlayerCount, len(data['sorted_stats_diff'][key]))):
                            if fileCount == 1:
                                columns.append(key + "-" + str(i + 1) + "-diff")
                            currList.append(data['sorted_stats_diff'][key][i])
                            
        if fileCount == 1:
            columns.append('score-diff')
        currList.append(home_score - away_score)
        list_data.append(currList)
        fileCount += 1
        jf.close()

df = pd.DataFrame(list_data)
df.columns = columns
print(df)

features_df = df.drop(columns = ['team-home', 'team-away', 'score-home', 'score-away', 'score-diff'])


X = df.drop(columns = ['team-home', 'team-away', 'score-home', 'score-away', 'score-diff']).astype(float)
y = df['score-diff']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

# feature selection
X_train_fs, X_test_fs, fs = select_features(X_train, y_train, X_test, X.columns)


model = LogisticRegression(solver='liblinear')
model.fit(X_train_fs, y_train)
# evaluate the model
yhat = model.predict(X_test_fs)
#print(len(yhat))
#print(len(y_test))

print(yhat - y_test)

print(mean_absolute_error(y_test, yhat))

corr_df = df.drop(columns = ['team-home', 'team-away', 'score-home', 'score-away'])
correlation_matrix(corr_df)

