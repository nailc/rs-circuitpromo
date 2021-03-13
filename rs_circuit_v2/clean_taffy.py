import pandas as pd
import numpy as np
import json
import os

# This script does four things :
# Delete recommended baskets with id 1111111111111
# Delete too old baskets for which we have no data available for training
# Delete useless columns
# Convert taffy to csv

def clean_taffy_liste(root_dir, directory, province) :
	df = pd.read_json(directory + '/taffy.json', dtype = {'i': 'str'}) # Open taffy
	path = root_dir + 'db_train/' + str(province) + '/data/' # Set path to files from user's province
	df.drop(['___id', '___s', 'quantity'], axis = 1, inplace = True) # Drop useless columns
	grouped = df.groupby(["c"]) # Group on timestamp's basket

	# Get earliest file's timestamp we have in database
	for file in os.listdir(path) :
	    timestamp = int(file[:13])
	    break

	# Delete recommended basket and basket with no available data for training
	for name, group in grouped :
	    if name == 1111111111111 :
	        df.drop(group.index, inplace = True)
	    elif name < timestamp :
	        df.drop(group.index, inplace = True)

	df[["i"]] = df[["i"]].astype(str)
	# Save cleaned taffy to csv
	df.to_csv(directory + '/taffy_clean.csv', index = False)
	print('Taffy cleaned and saved.')