# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 22:55:36 2021

@author: Arsalan Khan
"""

import pandas as pd

from sklearn.linear_model import LinearRegression, LogisticRegression

#dow30 index

dow = pd.read_csv("dow.csv")

X = dow[['Simple', 'Vader']]
y = dow['Change']

MLreg_dow = LinearRegression().fit(X, y)

y = dow['Binary']

MLlog_dow = LogisticRegression().fit(X, y)

#nasdaq index

nasdaq = pd.read_csv("nasdaq.csv")

X = nasdaq[['Simple', 'Vader']]
y = nasdaq['Change']

MLreg_nasdaq = LinearRegression().fit(X, y)

y = nasdaq['Binary']

MLlog_nasdaq = LogisticRegression().fit(X, y)

#russell

russell = pd.read_csv("russell.csv")

X = russell[['Simple', 'Vader']]
y = russell['Change']

MLreg_russell = LinearRegression().fit(X, y)

y = russell['Binary']

MLlog_russell = LogisticRegression().fit(X, y)

#sp_500 index

sp_500 = pd.read_csv("sp_500.csv")

X = sp_500[['Simple', 'Vader']]
y = sp_500['Change']

MLreg_sp_500 = LinearRegression().fit(X, y)

y = sp_500['Binary']

MLlog_sp_500 = LogisticRegression().fit(X, y)