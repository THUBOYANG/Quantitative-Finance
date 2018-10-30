# -*- coding: utf-8 -*-
"""
Created on Sun May 27 23:10:18 2018

@author: Li Boyang
"""

import numpy as np
import pandas as pd
import math
import statsmodels.api as sm
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
#import data
f3=open('D:/Tsinghua/大四下/毕业设计/data/jm000_30s.csv')
Jm = pd.read_csv(f3)
Jm.columns = ['time','open','high','low','close','volume','hold']
Jm['time'] = pd.to_datetime(Jm['time'])

f4=open('D:/Tsinghua/大四下/毕业设计/data/j9000_30s.csv')
J = pd.read_csv(f4)
J.columns = ['time','open','high','low','close','volume','hold']
J['time'] = pd.to_datetime(J['time'])

#washing data
J_price_30s=J[['time','close']]
Jm_price_30s=Jm[['time','close']]
price_frame_30s = pd.merge(J_price_30s, Jm_price_30s, on=['time'])
J_price_30s=price_frame_30s.close_x
Jm_price_30s=price_frame_30s.close_y
J_logprice_30s = np.log(J_price_30s)
Jm_logprice_30s = np.log(Jm_price_30s)
J_logprice_30s.index = price_frame_30s.time
Jm_logprice_30s.index = price_frame_30s.time
train_J_30s = J_logprice_30s['2013-03-22 09:00:00':'2016-12-30 14:59:30']
train_Jm_30s = Jm_logprice_30s['2013-03-22 09:00:00':'2016-12-30 14:59:30']
test_J_30s = J_logprice_30s[len(train_J_30s): ]
test_Jm_30s = Jm_logprice_30s[len(train_Jm_30s): ]