# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 12:46:07 2018

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

f2=open('F:/Tsinghua/大四下/毕业设计/data/j9000_5min.csv')
J = pd.read_csv(f2)
J.columns = ['nouse','date','time','open','high','low','close','volume','hold']
del J['nouse']

f3=open('F:/Tsinghua/大四下/毕业设计/data/jm000_5min.csv')
Jm = pd.read_csv(f3)
Jm.columns = ['nouse','date','time','open','high','low','close','volume','hold']
del Jm['nouse']

#washing data
J_price=J[['date','time','close']]
Jm_price=Jm[['date','time','close']]
result_frame = pd.merge(J_price, Jm_price, on=['date', 'time'])
J_price=result_frame.close_x
Jm_price=result_frame.close_y

#ADF test & coint test
Jm_logprice = np.log(Jm_price)
sm.tsa.stattools.adfuller(Jm_logprice)
J_logprice = np.log(J_price)
sm.tsa.stattools.adfuller(J_logprice)
diff_Jm = Jm_logprice.diff()
sm.tsa.stattools.adfuller(diff_Jm.drop(0))
diff_J = J_logprice.diff()
sm.tsa.stattools.adfuller(diff_J.drop(0))
sm.tsa.stattools.coint(Jm_logprice, J_logprice)

# plot data
J_logprice.plot(); Jm_logprice.plot()
plt.xlabel("Time"); plt.ylabel("logPrice")
plt.legend(["J", "JM"],loc='best')

# OLS to determine coefs of coint
x = J_logprice
y = Jm_logprice
X = sm.add_constant(x)
result = (sm.OLS(y,X)).fit()
print(result.summary())

# plot OLS
fig, ax = plt.subplots(figsize=(8,6))
ax.plot(x, y, 'o', label="data")
ax.plot(x, result.fittedvalues, 'r', label="OLS")
ax.legend(loc='best')

# plot coint
(Jm_logprice-0.8215*J_logprice).plot()
plt.axhline((Jm_logprice-0.8215*J_logprice).mean(), color="red", linestyle="--")
plt.xlabel("Time"); plt.ylabel("epsilon")
plt.legend(["epsilon", "Mean"])

# trading strategy
mean = (Jm_logprice-0.8215*J_logprice).mean()
position = [0]
asset = [Jm_price[0]+0.8215*J_price[0]]
tradepoint = []
for i in range(80436):
    if (Jm_logprice[i]-0.8215*J_logprice[i] < mean) & (position[i]==0):
        position.append(1)
        tradepoint.append(i)
        asset.append(asset[i])
    elif (Jm_logprice[i]-0.8215*J_logprice[i] > mean) & (position[i] ==0):
        position.append(-1)
        tradepoint.append(i)
        asset.append(asset[i])
    elif (Jm_logprice[i]-0.8215*J_logprice[i] > mean) & (position[i] ==1):
        position.append(-1)
        tradepoint.append(i)
        asset.append(asset[i] - 0.8215*(J_price.iloc[i]-J_price.iloc[(i-1)]) + (Jm_price.iloc[i]-Jm_price.iloc[(i-1)]))
        #asset.append(asset[i] + 2*(0.8215*J_price.iloc[i]-Jm_price.iloc[i]))
    elif (Jm_logprice[i]-0.8215*J_logprice[i] < mean) & (position[i] ==-1):
        position.append(1)
        tradepoint.append(i)
        asset.append(asset[i] + 0.8215*(J_price.iloc[i]-J_price.iloc[(i-1)]) - (Jm_price.iloc[i]-Jm_price.iloc[(i-1)]))
        #asset.append(asset[i] - 2*(0.8215*J_price.iloc[i]-Jm_price.iloc[i]))
    elif (Jm_logprice[i]-0.8215*J_logprice[i] > mean) & (position[i] ==-1):
        position.append(-1)
        asset.append(asset[i] + 0.8215*(J_price.iloc[i]-J_price.iloc[(i-1)]) - (Jm_price.iloc[i]-Jm_price.iloc[(i-1)]))
    elif (Jm_logprice[i]-0.8215*J_logprice[i] <= mean) & (position[i] ==1):
        position.append(1)
        asset.append(asset[i] - 0.8215*(J_price.iloc[i]-J_price.iloc[(i-1)]) + (Jm_price.iloc[i]-Jm_price.iloc[(i-1)]))

#performance
asset=pd.DataFrame(asset)
asset.columns=['asset']
return_year=pow(1+(asset.asset[80436]-asset.asset[0])/(asset.asset[0]),1/5)-1
std_year=np.std(dailyreturn)*np.sqrt(80436)/np.sqrt(5)
sharp=return_year/std_year        

max_drawback=(asset.asset[0]-asset.asset[1])/asset.asset[0]
for j in range(1,80436):
    if (asset.asset[j]>asset.asset[j-1])&(asset.asset[j]>asset.asset[j+1]):
        for k in range(j+1,80437):
            if (asset.asset[j]-asset.asset[k])/asset.asset[j]>max_drawback:
                max_drawback=(asset.asset[j]-asset.asset[k])/asset.asset[j]

            
            





((train_Jm-0.8696*train_J)-(train_Jm-0.8696*train_J).mean()).plot()
plt.axhline(0, color="red", linestyle="--")
plt.xlabel("Time"); plt.ylabel("epsilon")
plt.legend(["epsilon", "Mean"])
















