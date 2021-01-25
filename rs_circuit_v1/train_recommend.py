import pandas as pd
import numpy as np
import os
import sklearn
from sklearn.ensemble import RandomForestClassifier

def train_and_recommend(root_dir, directory, province) :
	training_set = pd.read_csv(directory + '/training_set.csv')
	training_set.dropna(inplace=True)
	sample = pd.read_csv(root_dir + '/to_recommend_' + str(province) + '.csv')

	X_train = training_set.iloc[:, 0:len(training_set.columns)-1].values
	y_train = training_set.iloc[:, len(training_set.columns)-1].values
	X_pred = sample.iloc[:,1:].values
	clf = RandomForestClassifier(n_estimators = 20)
	clf.fit(X_train, y_train)
	predicted = clf.predict(X_pred)
	predictions = clf.predict_proba(X_pred)
	a = pd.DataFrame(columns=['product_id', 'Class', 'Confidence'])
	classes = clf.classes_.tolist()
	for i in range(len(X_pred)):
	    if (predicted[i]):
	        a = a.append({'product_id': sample.at[i,'0'], 'Class': int(predicted[i]), 'Confidence' : predictions[i, classes.index(predicted[i])]}, ignore_index=True)
	a['Class'] = a['Class'].astype(int)
	a = a.sort_values(by = ['Confidence'], ascending = False)
	taffy = pd.read_json(directory + '/taffy.json', dtype = {'i' : 'string'})
	newprods = pd.read_json(root_dir + '/weekly_products_'+ str(province) + '.json', dtype = {0 : 'string'})
	recommendation = pd.DataFrame()
	for idx in a.head(15).index :
	    recommendation = recommendation.append(newprods.loc[newprods[0] == a.at[idx, 'product_id']], ignore_index = True)
	recommendation['c'] = 1111111111111
	recommendation['quantity'] = 1
	recommendation['___id'] = 1
	recommendation['___s'] = 'True'
	recommendation.rename(columns={0 : 'i', 5:'d', 6:'e', 2:'r', 3:'s'}, inplace=True)
	#recommendation = recommendation.append(taffy, ignore_index = True)
	print(len(a))
	recommendation = recommendation[['c', 'd', 'e', 'i', 'quantity','r'  ,'s', '___id', '___s']]
	recommendation.to_json(directory + '/taffy_to_site.json', orient='records')