import pandas as pd
import numpy as np

def preprocess_all_data(root_dir, directory) :

	df = pd.read_csv(directory + '/training_pool.csv')
	cats = pd.read_csv(root_dir + '/hashed_categories.csv')
	brands = pd.read_csv(root_dir + '/hashed_brands.csv')
	col_list = df.columns
	training_set = pd.read_csv(directory + '/training_pool.csv')
	training_set.drop(['n', 'd', 'q', 'z', 'pan'], axis = 1, inplace = True) # drop useless columns
	# zscore
	training_set['p'] = (training_set['p'] - training_set['p'].mean())/training_set['p'].std(ddof=0)
	training_set['s'] = (training_set['s'] - training_set['s'].mean())/training_set['s'].std(ddof=0)
	training_set['r'] = (training_set['r'] - training_set['r'].mean())/training_set['r'].std(ddof=0)

	training_set = training_set.merge(cats, how = 'left')
	training_set = training_set.merge(brands, how = 'left')
	training_set.drop(['m', 'c'], axis = 1, inplace = True)
	collist = training_set.columns
	collist = list(collist)
	rm = collist[73]
	collist.remove(rm)
	collist.append(rm) 
	training_set.to_csv(directory + '/training_set.csv', index = False, columns = collist)