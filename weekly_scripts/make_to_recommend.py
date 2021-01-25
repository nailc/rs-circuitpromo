import pandas as pd
import numpy as np
import os
import json
import re
import sys
import warnings
warnings.filterwarnings('ignore')

def process_weekly_products(root_dir) :
	province_id_list = list(range(1,21))
	for id in province_id_list :
		try :
			df = pd.read_json(root_dir + '/weekly_products_' + str(id) + '.json', dtype = {0 : 'str', 1 : 'int'})
			cats = pd.read_csv(root_dir + '/hashed_categories.csv')
			brands = pd.read_csv(root_dir + '/hashed_brands.csv')
			ensdf = pd.read_json(root_dir + '/enseigne.json')
			enslist = []
			ensdf.sort_values(by = ['ei'], inplace = True)
			for elem in ensdf.index :
			    enslist.append(str(ensdf.at[elem,'ei']))

			del ensdf
			df.drop([12,11,13,5],axis=1,inplace=True)
			for ens in enslist :
			    df[ens] = 0

			grouped = df.groupby([1,2,3,4,7,8,9,10])
			df = grouped.head(1)
			for name, group in grouped:
			    groupens = list(group[6])
			    for elem in groupens :
			        df.loc[(df[1] == name[0]) & (df[2] == name[1]) & (df[3] == name[2]) & (df[4] == name[3]) & (df[7] == name[4]) & (df[8] == name[5]) & (df[9] == name[6]) & (df[10] == name[7]), str(elem)] = 1
			
			df.drop([6,7,8,10], axis = 1, inplace = True)
			df.rename(columns = {1:'c',9:'m'}, inplace = True)
			df = df.merge(cats, how = 'left')
			df = df.merge(brands, how = 'left')
			df.drop(df.loc[np.isnan(df['m6'])].index, inplace=True)
			df[2] = (df[2] - df[2].mean())/df[2].std(ddof=0)
			df[3] = (df[3] - df[3].mean())/df[3].std(ddof=0)
			df[4] = (df[4] - df[4].mean())/df[4].std(ddof=0)
			df.drop(['c','m'], axis=1, inplace=True)
			print('Creating file to_recommend_' + str(id) + '. ')
			df.to_csv('to_recommend_' + str(id) + '.csv', index=False)
		
		except :
			print('No file with id ' + str(id) + '. ')

if __name__ == "__main__":
   process_weekly_products(sys.argv[1])