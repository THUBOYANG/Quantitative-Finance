# -*- coding: utf-8 -*-
"""
Created on Mon May 14 16:07:19 2018

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
f1=open('D:/Tsinghua/大四下/毕业设计/data/jm000_5mins.csv')
Jm = pd.read_csv(f1)
Jm.columns = ['time','open','high','low','close','volume','hold']
Jm['time'] = pd.to_datetime(Jm['time'])

f2=open('D:/Tsinghua/大四下/毕业设计/data/j9000_5mins.csv')
J = pd.read_csv(f2)
J.columns = ['time','open','high','low','close','volume','hold']
J['time'] = pd.to_datetime(J['time'])

#washing data
J_price=J[['time','close']]
Jm_price=Jm[['time','close']]
price_frame = pd.merge(J_price, Jm_price, on=['time'])
J_price=price_frame.close_x
Jm_price=price_frame.close_y
J_logprice = np.log(J_price)
Jm_logprice = np.log(Jm_price)

train_J=J_logprice[0:57956]
train_Jm=Jm_logprice[0:57956]
test_J=J_logprice[57956: ]
test_Jm=Jm_logprice[57956: ]


            
            
















