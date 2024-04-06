import json
import os
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import VotingRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.tree import DecisionTreeRegressor

sns.set_style("whitegrid")

X = []
y = []
for filename in os.listdir("dataset_mens_diff"):
    with open(f"dataset_mens_diff/{filename}", "r") as file:
        data = json.load(file)

        sorted_stats_diff = data["sorted_stats_diff"]

        team_diff = []
        for key in sorted_stats_diff:
            team_diff.extend(sorted_stats_diff[key])
        X.append(team_diff)
        y.append(data["score_diff"])


max_len = max(len(feature_vector) for feature_vector in X)


X = [np.pad(feature_vector, (0, max_len - len(feature_vector))) for feature_vector in X]

X = np.array(X)
y = np.array(y)

# Perform PCA to reduce the dimensionality of X
pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X)


plt.figure(figsize=(10, 6))
plt.scatter(X_reduced[:, 0], X_reduced[:, 1], c=y, cmap='viridis')
plt.colorbar(label='score_diff')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('PCA of X with y as color')
plt.show()



# # Now you can convert X into a numpy array
# X = np.array(X)
# X_reshaped = X.reshape(-1, 143)
#
# # Calculate the correlation coefficients
# correlations = [np.corrcoef(X_reshaped[:, i], y)[0, 1] for i in range(X_reshaped.shape[1])]
#
# # Define the feature names
# features = ["GP", "MIN", "PTS", "REB", "AST", "STL", "BLK", "TO", "FG%", "FT%", "3P%"]
#
# # Create a bar plot of the correlation coefficients
# plt.figure(figsize=(10, 6))
# plt.bar(features, correlations)
# plt.xlabel('Features')
# plt.ylabel('Correlation with score_diff')
# plt.title('Correlation of Features with score_diff')
# plt.xticks(rotation=90)  # Rotate x-axis labels for better readability
# plt.show()

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a linear regression
model1 = LinearRegression()
model1.fit(X_train, y_train)

# Visualize the residuals of the model
y_train_pred = model1.predict(X_train)
residuals = y_train - y_train_pred
plt.figure(figsize=(10, 6))
sns.histplot(residuals, kde=True, color='skyblue')
plt.title('Residuals of Linear Regression Model', fontsize=20)
plt.xlabel('Residuals', fontsize=15)
plt.ylabel('Frequency', fontsize=15)
plt.show()

# Gradient boosting
model2 = GradientBoostingRegressor()
model2.fit(X_train, y_train)

# Visualize the residuals of the model
y_train_pred = model2.predict(X_train)
residuals = y_train - y_train_pred
plt.figure(figsize=(10, 6))
sns.histplot(residuals, kde=True, color='skyblue')
plt.title('Residuals of Gradient Boosting Model', fontsize=20)
plt.xlabel('Residuals', fontsize=15)
plt.ylabel('Frequency', fontsize=15)
plt.show()

# Random Forest
model3 = RandomForestRegressor()
model3.fit(X_train, y_train)

# Visualize the residuals of the model
y_train_pred = model3.predict(X_train)
residuals = y_train - y_train_pred
plt.figure(figsize=(10, 6))
sns.histplot(residuals, kde=True, color='skyblue')
plt.title('Residuals of Random Forest Model', fontsize=20)
plt.xlabel('Residuals', fontsize=15)
plt.ylabel('Frequency', fontsize=15)
plt.show()

# Neural Network
model4 = MLPRegressor()
model4.fit(X_train, y_train)


# Visualize the residuals of the model
y_train_pred = model4.predict(X_train)
residuals = y_train - y_train_pred
plt.figure(figsize=(10, 6))
sns.histplot(residuals, kde=True, color='skyblue')
plt.title('Residuals of Neural Network Model', fontsize=20)
plt.xlabel('Residuals', fontsize=15)
plt.ylabel('Frequency', fontsize=15)
plt.show()

# Decision Tree

model5 = DecisionTreeRegressor()
model5.fit(X_train, y_train)

# Visualize the residuals of the model
y_train_pred = model5.predict(X_train)
residuals = y_train - y_train_pred
plt.figure(figsize=(10, 6))
sns.histplot(residuals, kde=True, color='skyblue')
plt.title('Residuals of Decision Tree Model', fontsize=20)
plt.xlabel('Residuals', fontsize=15)
plt.ylabel('Frequency', fontsize=15)
plt.show()

# model 6 is SVM
from sklearn.svm import SVR
model6 = SVR()
model6.fit(X_train, y_train)





# Visualize the residuals of the model
y_train_pred = model6.predict(X_train)
residuals = y_train - y_train_pred
plt.figure(figsize=(10, 6))
sns.histplot(residuals, kde=True, color='skyblue')
plt.title('Residuals of SVM Model', fontsize=20)
plt.xlabel('Residuals', fontsize=15)
plt.ylabel('Frequency', fontsize=15)
plt.show()

# model 7 is knn
from sklearn.neighbors import KNeighborsRegressor
model7 = KNeighborsRegressor()
model7.fit(X_train, y_train)

# Visualize the residuals of the model
y_train_pred = model7.predict(X_train)
residuals = y_train - y_train_pred
plt.figure(figsize=(10, 6))
sns.histplot(residuals, kde=True, color='skyblue')
plt.title('Residuals of KNN Model', fontsize=20)
plt.xlabel('Residuals', fontsize=15)
plt.ylabel('Frequency', fontsize=15)
plt.show()


#Ensemble all 5 models
model = VotingRegressor(estimators=[('lr', model1), ('gb', model2), ('rf', model3), ('nn', model4), ('dt', model5), ('svm', model6), ('knn', model7)])
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# print the actual spread and the predicted spread for each game
correct_predictions = 0
for i in range(len(y_test)):
    print('Actual:', y_test[i], 'Predicted:', y_pred[i])
    # Check if the model correctly predicted the winning team
    if np.sign(y_test[i]) == np.sign(y_pred[i]):
        correct_predictions += 1

# Create a list of colors based on the actual spread
colors = ['green' if spread > 0 else 'red' if spread < 0 else 'blue' for spread in y_test]

# Visualize the actual vs predicted spread with different colors for home team win, loss, or tie
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, color=colors)
plt.xlabel('Actual Spread', fontsize=15)
plt.ylabel('Predicted Spread', fontsize=15)
plt.title('Actual vs Predicted Spread', fontsize=20)
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='black')  # a black line showing the perfect prediction
plt.show()

# Calculate the accuracy of winning team predictions
winning_team_accuracy = correct_predictions / len(y_test)
print('Winning Team Prediction Accuracy:', winning_team_accuracy)

# List of models
models = [model1, model2, model3, model4, model5, model6, model7, model]
model_names = ['Linear Regression', 'Gradient Boosting', 'Random Forest', 'Neural Network', 'Decision Tree', 'SVM', 'KNN', 'Ensemble']

for model, name in zip(models, model_names):
    # Make predictions
    y_pred = model.predict(X_test)

    # Calculate the MSE and RMSE
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)

    print(f'{name} Model:')
    print('Mean Squared Error:', mse)
    print('Root Mean Squared Error:', rmse)
    print('-------------------------')