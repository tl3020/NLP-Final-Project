# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 14:57:57 2021

@author: qianrun
"""

import pandas as pd
import pickle
import datetime
import numpy as np
import re

# read original S&P 500 data in Dataset folder of the repo
sp = pd.read_csv('C:/Users/guoqi/Desktop/nlp_project/NLP-Final-Project/Dataset/S&P500/Daily_S&P500.csv')
# read pkl file of sentiment score of each tweets from Data wrangling code folder of the repo
senti = pickle.load(open("C:/Users/guoqi/Desktop/nlp_project/NLP-Final-Project/Data_Wrangling_code/US_Eng_tweets_with_senti.pkl", "rb"))

# set up date range to subset S&P 500
begin_date = datetime.datetime(2020, 4, 1)
end_date = datetime.datetime(2020, 4, 30)

# define a function to change sp['Date'] from str to datetime type 
def date_convert_sp(date_str):
    from datetime import datetime
    date = datetime.strptime(date_str,'%m/%d/%Y')
    return date
sp['Date']= sp['Date'].apply(date_convert_sp)

# subset data
sp = sp[(sp['Date'] >= begin_date) & (sp['Date'] <= end_date)]

# getting avegrage sentimen score for eahc date
senti_ = senti.groupby('date')
avg_vader = pd.DataFrame(senti_['vader_senti'] .mean())
avg_simple = pd.DataFrame(senti_['simple_senti'].mean())
avg_senti_each_date = pd.merge(avg_vader,avg_simple, on = 'date')
avg_senti_each_date.reset_index(inplace=True)
avg_senti_each_date.rename(columns = {'date' : 'Date','vader_senti' : 'vader_avg', 'simple_senti' : 'simple_avg'}, inplace = True)

# define a function to change avg_senti_each_date['Date'] from str to datetime type 
# (can't use previous one because the format of the str is different)
def date_convert_senti(date_str):
    from datetime import datetime
    date = datetime.strptime(date_str,'%Y-%m-%d')
    return date
avg_senti_each_date['Date'] = avg_senti_each_date['Date'].apply(date_convert_senti)

# define a function to only keep numbers in the strings, so that they can be changed to numbers
def fun(x):
    import re
    x_ = re.sub('[^0-9.]+','',x)
    x_ = float(x_)
    return x_
sp['Open'] = sp['Open'].apply(fun)
sp['Close'] = sp['Close'].apply(fun)

# getting the magnitude of change on that date
sp['Change'] = sp['Open'] - sp['Close']

# getting columns that we need
sp_change = sp[['Date','Open','Close','Change']]

# creating empty columns to store other info
sp_change['Binary'] = [0] * sp_change.shape[0]
sp_change['Date_Range_of_Senti_Score'] = [0] * sp_change.shape[0]
sp_change['Simple']= [0] * sp_change.shape[0]
sp_change['Vader']= [0] * sp_change.shape[0]

# getting other info
for i in np.arange(sp_change.shape[0]):
    beg = sp_change.iloc[i,0] - datetime.timedelta(days = 2)
    end = sp_change.iloc[i,0]
    sub = avg_senti_each_date[(avg_senti_each_date['Date'] >= beg) & (avg_senti_each_date['Date'] <= end)]
    date_range = str(beg) + ' to ' + str(end)
    sp_change['Date_Range_of_Senti_Score'].iloc[i] = re.sub(' 00:00:00','',date_range)
    sp_change['Simple'].iloc[i] = sub['simple_avg'].mean()
    sp_change['Vader'].iloc[i] = sub['vader_avg'].mean()
    if sp_change['Change'].iloc[i] >= 0:
        sp_change['Binary'].iloc[i] = 1
    else: 
        sp_change['Binary'].iloc[i] = 0
    

pickle.dump(avg_senti_each_date, open("C:/Users/guoqi/Desktop/nlp_project/NLP-Final-Project/Data_Wrangling_code/Avg_Sentiment_each_date.pkl", "wb"))
pickle.dump(sp_change, open("C:/Users/guoqi/Desktop/nlp_project/NLP-Final-Project/Modeling/sp_500.pkl", "wb"))
sp_change.to_csv(r'C:/Users/guoqi/Desktop/nlp_project/NLP-Final-Project/Modeling/sp_500.csv', index = False)










import pandas as pd

from sklearn.linear_model import LinearRegression, LogisticRegression

sp_change = pickle.load(open("C:/Users/guoqi/Desktop/nlp_project/NLP-Final-Project/Modeling/sp_500.pkl", "rb"))

#independent variables
X = sp_change[['Vader', 'Simple']]

#dependent variables
y = sp_change['Change']

#Multiple Linear Regression
MLreg = LinearRegression().fit(X, y)

#Simple Linear Regression on simple_score
X = sp_change['Simple'].values.reshape(-1, 1)
reg_simple = LinearRegression().fit(X, y)

#Simple Linear Regression on vader_score
X = sp_change['Vader'].values.reshape(-1, 1)
reg_vader = LinearRegression().fit(X, y)

#Logistic regression

X = sp_change[['Vader', 'Simple']]
y = y = sp_change['Binary']
MLlogreg = LogisticRegression().fit(X, y)
















