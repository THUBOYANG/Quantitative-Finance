# -*- coding: utf-8 -*-
"""
Created on Sun May 27 23:19:39 2018

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
f5=open('D:/Tsinghua/大四下/毕业设计/data/jm000_1h.csv')
Jm = pd.read_csv(f5)
Jm.columns = ['time','open','high','low','close','volume','hold']
Jm['time'] = pd.to_datetime(Jm['time'])

f6=open('D:/Tsinghua/大四下/毕业设计/data/j9000_1h.csv')
J = pd.read_csv(f6)
J.columns = ['time','open','high','low','close','volume','hold']
J['time'] = pd.to_datetime(J['time'])

#washing data
J_price_1h=J[['time','close']]
Jm_price_1h=Jm[['time','close']]
price_frame_1h = pd.merge(J_price_1h, Jm_price_1h, on=['time'])
J_price_1h=price_frame_1h.close_x
Jm_price_1h=price_frame_1h.close_y
J_logprice_1h = np.log(J_price_1h)
Jm_logprice_1h = np.log(Jm_price_1h)
J_logprice_1h.index = price_frame_1h.time
Jm_logprice_1h.index = price_frame_1h.time
train_Jm_1h = Jm_logprice_1h['2013-03-22 09:00:00':'2016-12-30 14:59:30']
train_J_1h = J_logprice_1h['2013-03-22 09:00:00':'2016-12-30 14:59:30']
test_J_1h = J_logprice_1h[len(train_J_1h): ]
test_J_1h = J_logprice_1h[len(train_Jm_1h): ]