# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 22:55:36 2021

@author: Arsalan Khan
"""

import pandas as pd

from sklearn.linear_model import LinearRegression, LogisticRegression

#import complete_data.csv

complete_data = pd.read_csv("complete_data.csv")

#independent variables
X = complete_data[['vader_score', 'simple_score']]

#dependent variables
y = complete_data['change']

#Multiple Linear Regression
MLreg = LinearRegression().fit(X, y)

#Simple Linear Regression on simple_score
X = complete_data['simple_score'].values.reshape(-1, 1)
reg_simple = LinearRegression().fit(X, y)

#Simple Linear Regression on vader_score
X = complete_data['vader_score'].values.reshape(-1, 1)
reg_vader = LinearRegression().fit(X, y)

#Logistic regression

X = complete_data[['vader_score', 'simple_score']]
y = complete_data['Gain (Binary)']
MLlogreg = LogisticRegression().fit(X, y)
