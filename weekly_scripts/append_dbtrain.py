import pandas as pd
import numpy as np
import os
import json
import re
import sys
import warnings
warnings.filterwarnings('ignore')

def split_weekly_products(argv) :
	# Prepare list of markets
	ensdf = pd.read_json(argv + '/enseigne.json')
	ensdf.sort_values(by = ['ei'], inplace = True)
	enslist = []
	for elem in ensdf.index :
	    enslist.append(str(ensdf.at[elem,'ei']))

	del ensdf # Delete market dataframes after makinf list to free memory

	province_id_list = list(range(1,21))
	for id in province_id_list :
		try :
			df = pd.read_json(argv + '/weekly_products_' + str(id) + '.json', dtype = {0 : 'str', 1 : 'int'})
			path = argv + '/db_train/' + str(id) + '/data/' 
			timstp = []
			time_grouped = df.groupby(5).head(1)
			for i in time_grouped.index :
			    timstp.append(time_grouped.at[i, 5])
			for j in range(len(timstp)) :
			    tmp = df.loc[df[5] == timstp[j]]
			    tmp.rename(columns = {0:'i',1:'c',2:'p',3:'s',4:'r',6:'e',7:'n',8:'d',9:'m',10:'q'}, inplace = True)
			    complete = tmp[['i', 'c', 'p', 's', 'r', 'e', 'n', 'd', 'm', 'q']]
			    complete['c'] = complete['c'].astype(int)
			    for ens in enslist :
			        complete[ens] = 0

			    complete.fillna('', inplace = True)
			    grouped = complete.groupby(['c', 'p', 's', 'r', 'n', 'd', 'm', 'q'])
			    final_df = grouped.head(1)

			    for name, group in grouped:
			        groupens = list(group['e'])
			        final_df.loc[(final_df['c'] == name[0]) & (final_df['p'] == name[1]) & (final_df['s'] == name[2]) & (final_df['r'] == name[3]) & (final_df['n'] == name[4]) & (final_df['d'] == name[5]) & (final_df['m'] == name[6]) & (final_df['q'] == name[7]), 'z'] = str(list(group['i']))
			        for elem in groupens :
			            final_df.loc[(final_df['c'] == name[0]) & (final_df['p'] == name[1]) & (final_df['s'] == name[2]) & (final_df['r'] == name[3]) & (final_df['n'] == name[4]) & (final_df['d'] == name[5]) & (final_df['m'] == name[6]) & (final_df['q'] == name[7]), str(elem)] = 1

			    final_df.drop(['e', 'i'], axis = 1, inplace = True)
			    sys.stdout.write('creating ' + str(timstp[j]) + ' for province '+ str(id) +'. \n')
			    final_df.to_csv(path + str(timstp[j])+'.csv', index = False)

			del timstp
			
		except Exception as e: 
			sys.stdout.write('No file for province id ' + str(id) +'. ')
			print(e)

if __name__ == "__main__":
   split_weekly_products(sys.argv[1])