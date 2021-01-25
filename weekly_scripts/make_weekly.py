import pandas as pd
import numpy as np
import os
import json
import re
import sys

def make_weekly_products(argv):

	root_dir = argv
	province_id_list = list(range(1,21))
	for id in province_id_list :
		try :
			f = open(root_dir + '/product' + str(id) + '_fr.json', 'r+')
			newfile = f.readline()
			f.close()
			pattern = re.compile('{"version":"[0-9]+"},')
			match = re.search(pattern, newfile)
			if match :
			    newfile = newfile.replace(str(match.group()), '')

			f = open(root_dir + '/weekly_products_' + str(id) + '.json', 'w')
			f.write(newfile)
			f.close()

		except : 
			print('No file for province id ' + str(id) + '. ')

if __name__ == "__main__":
   make_weekly_products(sys.argv[1])