import pandas as pd
import numpy as np
import os
import sklearn
from fuzzywuzzy import fuzz
import json
from sklearn.ensemble import RandomForestClassifier

def train_and_recommend(root_dir, directory, province) :
	full_taffy = pd.read_json(directory+'/full_taffy.json', dtype = {'i': 'str'})
	full_taffy = full_taffy.loc[full_taffy['c']!=1111111111111]
	training_set = pd.read_csv(directory + '/training_set.csv')
	training_set.dropna(inplace=True)
	training_set.drop(['pan'], axis=1, inplace=True)
	sample = pd.read_csv(root_dir + '/to_recommend_' + str(province) + '.csv')

	X_train = training_set.iloc[:, 0:len(training_set.columns)-1].values
	y_train = training_set.iloc[:, len(training_set.columns)-1].values
	X_pred = sample.iloc[:,1:].values
	clf = RandomForestClassifier(n_estimators = 25, random_state=2)
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
	for idx in a.head(100).index :
		recommendation = recommendation.append(newprods.loc[newprods[0] == a.at[idx, 'product_id']], ignore_index = True)
	recommendation['c'] = 1111111111111
	recommendation['quantity'] = 1
	recommendation['___id'] = 1
	recommendation['___s'] = 'True'
	recommendation.rename(columns={0 : 'i', 5:'d', 6:'e', 2:'r', 3:'s'}, inplace=True)

	newprods = newprods[[0, 1, 7]]
	grouped = newprods.groupby(1)
	maximum_similarity_ratio = 60
	cleaned_recommendation = []
	for name, group in grouped :
		products = []
		for idx in group.index :
			products.append([str(group.at[idx,0]),str(group.at[idx,7])])
		for i in range(len(products)):
			for j in range(i+1, len(products)):
				tsr = fuzz.token_set_ratio(products[i][1], products[j][1])
				if tsr > maximum_similarity_ratio :
					products[j][1] = ''
		for i in range(len(products)):
			k = 0
			if "bière" in products[i][1].lower() :
				if k > 0 :
					products[i][1] = ''
				k+=1
		products = [x[0] for x in products if str(x[1]) != '']
		cleaned_recommendation.append(products)
	cleaned_recommendation = [item for sublist in cleaned_recommendation for item in sublist]
	recommendation = recommendation.loc[recommendation['i'].isin(cleaned_recommendation)]

	recommendation = recommendation.append(full_taffy, ignore_index = True)
	recommendation = recommendation[['c', 'd', 'e', 'i', 'quantity','r'  ,'s', '___id', '___s']]
	recommendation.to_json(directory + '/taffy_to_site.json', orient='records')