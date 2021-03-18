# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 13:30:42 2021

@author: guoqi
"""
import os
import pandas as pd
import numpy as np
import pickle

path = "C:/Users/guoqi/Desktop/nlp_project/April" # path to data 


data = pd.DataFrame()
for root, dirs, files in os.walk(path):
    try:
        for word in files:
            label = word.split(' ')[0]
            t_path = root + '/' + word
            f = pd.read_csv(t_path)
            d = pd.DataFrame({'user_id':f.user_id, 'text':f.text,
                             'country':f.country_code, 'language':f.lang,
                             'date':np.repeat(label,len(f))})
            data = data.append(d)            
    except Exception as e:
        print (e)

pickle.dump(data, open(path+"tweets.pkl", "wb"))

my_data = pickle.load(open(path+"tweets.pkl", "rb"))
        


