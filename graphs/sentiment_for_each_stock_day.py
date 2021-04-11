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
dow = pd.read_csv('C:/Users/guoqi/Desktop/nlp_project/NLP-Final-Project/Modeling/Data/Financial Data/dow30.csv')
nasdaq = pd.read_csv('C:/Users/guoqi/Desktop/nlp_project/NLP-Final-Project/Modeling/Data/Financial Data/nasdaq.csv')
russell = pd.read_csv('C:/Users/guoqi/Desktop/nlp_project/NLP-Final-Project/Modeling/Data/Financial Data/russell.csv')


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
def date_convert(date_str):
    from datetime import datetime
    date = datetime.strptime(date_str,'%Y-%m-%d')
    return date
dow['Date'] = dow['Date'].apply(date_convert)
nasdaq['Date'] = nasdaq['Date'].apply(date_convert)
russell['Date'] = russell['Date'].apply(date_convert)


# define a function to only keep numbers in the strings, so that they can be changed to numbers

def fun(x):
    import re
    x_ = re.sub('[^0-9.]+','',x)
    x_ = float(x_)
    return x_
sp['Open'] = sp['Open'].apply(fun)
sp['Close'] = sp['Close'].apply(fun)
dow['dow30'] = dow['dow30'].apply(fun)
nasdaq['nasdaq'] = nasdaq['nasdaq'].apply(fun)
russell['russell'] = russell['russell'].apply(fun)


# getting the magnitude of change on that date
sp['Change'] = sp['Open'] - sp['Close']

# get change amount for dow, nasdaq, russell
def get_change(x):
    for i in np.arange(x.shape[0]):
        if i == 0:
            x['Change'][i] = x.iloc[i,1]
        else:
            x['Change'][i] = x.iloc[i,1] - x.iloc[i-1,1]
    return x

dow['Change'] = 0
dow = get_change(dow)
nasdaq['Change'] = 0
nasdaq = get_change(nasdaq)
russell['Change'] = 0
russell = get_change(russell)



# subset data
sp = sp[(sp['Date'] >= begin_date) & (sp['Date'] <= end_date)]
dow = dow[(dow['Date'] >= begin_date) & (dow['Date'] <= end_date)]
russell = russell[(russell['Date']>= begin_date) & (russell['Date'] <= end_date)]
nasdaq = nasdaq[(nasdaq['Date']>= begin_date) & (nasdaq['Date'] <= end_date)]

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




dow.rename(columns = {'dow30' : 'Close'},inplace = True)
nasdaq.rename(columns = {'nasdaq':'Close'},inplace = True)
russell.rename(columns = {'russell':'Close'},inplace = True)

                      
def data(x):
    x_change = x[['Date','Close','Change']]
    
    x_change['Binary'] = 0
    x_change['Date_Range_of_Senti_Score'] = 0
    x_change['Simple']= 0
    x_change['Vader']= 0
    
    for i in np.arange(x_change.shape[0]):
        beg = x_change.iloc[i,0] - datetime.timedelta(days = 2)
        end = x_change.iloc[i,0]
        sub = avg_senti_each_date[(avg_senti_each_date['Date'] >= beg) & (avg_senti_each_date['Date'] <= end)]
        date_range = str(beg) + ' to ' + str(end)
        x_change['Date_Range_of_Senti_Score'].iloc[i] = re.sub(' 00:00:00','',date_range)
        x_change['Simple'].iloc[i] = sub['simple_avg'].mean()
        x_change['Vader'].iloc[i] = sub['vader_avg'].mean()
        if x_change['Change'].iloc[i] >= 0:
            x_change['Binary'].iloc[i] = 1
        else: 
            x_change['Binary'].iloc[i] = 0
    return x_change
    

sp_change = data(sp)
dow_change = data(dow)
nasdaq_change = data(nasdaq)
russell_change= data(russell)
    

pickle.dump(avg_senti_each_date, open("C:/Users/guoqi/Desktop/nlp_project/NLP-Final-Project/Data_Wrangling_code/Avg_Sentiment_each_date.pkl", "wb"))
pickle.dump(sp_change, open("C:/Users/guoqi/Desktop/nlp_project/NLP-Final-Project/Modeling/sp_500.pkl", "wb"))
sp_change.to_csv(r'C:/Users/guoqi/Desktop/nlp_project/NLP-Final-Project/Modeling/sp_500.csv', index = False)
dow_change.to_csv(r'C:/Users/guoqi/Desktop/nlp_project/NLP-Final-Project/Modeling/dow.csv', index = False)
nasdaq_change.to_csv(r'C:/Users/guoqi/Desktop/nlp_project/NLP-Final-Project/Modeling/nasdaq.csv', index = False)
russell_change.to_csv(r'C:/Users/guoqi/Desktop/nlp_project/NLP-Final-Project/Modeling/russell.csv', index = False)









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
















