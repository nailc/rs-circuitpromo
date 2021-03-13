import pandas as pd
import numpy as np
import json
import random
import time
import gc
import glob
import os

def make_pool_data(root_dir, directory, province) :
    path = root_dir + '/db_train/' + str(province) + '/data/'
    taffy = pd.read_csv(directory + '/taffy_clean.csv', dtype = {'i': 'str'})
    grouped = taffy.groupby(["c"])
    totrain = pd.DataFrame()
    replace = False
    faker = 5

    for panid, pan in grouped :
        pool = pd.DataFrame()
        correspondance = pd.DataFrame()
        list_ens = []

        for file in os.listdir(path) : 
            if int(file[:13]) - 604800000 < panid <= int(file[:13]):
                tmp = pd.read_csv(path + file)
                pool = pool.append(tmp, ignore_index = True)

        if len(pool) == 0:
            if int(file[:13]) - (604800000*3) < panid <= int(file[:13]) + (604800000*3):
                tmp = pd.read_csv(path + file)
                pool = pool.append(tmp, ignore_index = True)

        if len(pool) > 0 :
            for idx in pan.index :
                correspondance = correspondance.append(pool[pool['z'].str.contains("'" + pan.at[idx, 'i'] +"'", regex=False)])
                
                if pool[pool['z'].str.contains("'" + pan.at[idx, 'i'] +"'", regex=False)].empty == False :
                    list_ens.append(pan.at[idx, 'e'])

                pool.drop(pool[pool['z'].str.contains(pan.at[idx, 'i'])].index, inplace = True)

            correspondance['pan'] = panid
            pool['pan']= panid
            correspondance['class'] = list_ens
            pool['class'] = 0
            arr_corr = correspondance.to_numpy()
            i = 0
            ratio = len(pool)/len(pan) 

            if ratio > faker :

                while i < faker :
                    arr_sample = pool.loc[np.random.choice(pool.index, len(pan) , replace), :].to_numpy()
                    clone = np.vstack((arr_corr, arr_sample))

                    try :
                        totrain = np.vstack((totrain, clone))

                    except :
                        totrain = clone

                    i = i + 1

            elif ratio < faker :

                while i < ratio :
                    arr_sample = pool.loc[np.random.choice(pool.index, len(pan) , replace), :].to_numpy()
                    clone = np.vstack((arr_corr, arr_sample))

                    try :
                        totrain = np.vstack((totrain, clone))

                    except :
                        totrain = clone

                    i = i + 1

    col_list = correspondance.columns
    training_set = pd.DataFrame(totrain, columns = col_list)
    training_set.drop('z', axis = 1)
    training_set.to_csv(directory + '/training_pool.csv', index = False)
    del(totrain)