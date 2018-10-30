# -*- coding: utf-8 -*-
"""
Created on Mon May 28 16:54:17 2018

@author: Li Boyang
"""
def max_drawdown(timeseries):
    # 回撤结束时间点
    i = np.argmax(np.maximum.accumulate(timeseries) - timeseries)
    # 回撤开始的时间点
    j = np.argmax(timeseries[:i])
    return (float(timeseries[i]) / timeseries[j]) - 1

#trading signal
n = 100
k = 5
sigma = [0 for i in range(2*n-2)]
Gama = [0 for i in range(n-1)]
PriceGap = [0 for i in range(n-1)]
Miu = [0 for i in range(2*n-2)]
up_line = [0 for i in range(3*n-3)]
down_line = [0 for i in range(3*n-3)]
weight = [i+1 for i in range(n)]
X = test_J
Y = test_Jm
for i in range(n-1,len(X)):
    if sum((X[i-n+1:i+1]-X[i-n+1:i+1].mean())**2)>0:
        Gama_now = sum((X[i-n+1:i+1]-X[i-n+1:i+1].mean())*(Y[i-n+1:i+1]-Y[i-n+1:i+1].mean()))/(sum((X[i-n+1:i+1]-X[i-n+1:i+1].mean())**2))
    else:
        Gama_now=0
    Gama.append(Gama_now)
    PriceGap_now = Y[i]-Gama_now*X[i]
    PriceGap.append(PriceGap_now)
    if i>=2*n-2:
        Miu_now = sum([a*b for a,b in zip(PriceGap[i-n+1:i+1],weight)])/(n*(n+1)/2)
        #Miu_now = sum(PriceGap[i-n+1:i+1])/n
        sigma_now = PriceGap_now-Miu_now
        Miu.append(Miu_now)
        sigma.append(sigma_now)
        if i>=3*n-3:
            up_line.append(np.mean(sigma[i-n+1:i+1])+k*np.std(sigma[i-n+1:i+1]))
            down_line.append(np.mean(sigma[i-n+1:i+1])-k*np.std(sigma[i-n+1:i+1]))
#performance
asset = 0
position = []
tradepoint = []
netasset = []
Gama_used = []
for i in range(len(X)):
    if i <3*n-3:
        position.append(0)
        netasset.append(asset)
        Gama_used.append(0)
    else:
        if position[i-1]==0:
            if sigma[i]>up_line[i]:
                position.append(1)
                Gama_used.append(Gama[i])
                tradepoint.append(i)
            elif sigma[i]<down_line[i]:
                position.append(-1)
                Gama_used.append(Gama[i])
                tradepoint.append(i)
            else:
                position.append(0)
                Gama_used.append(0)
            netasset.append(netasset[i-1])
        elif position[i-1]>0:
            netasset.append(netasset[i-1]+(Jm_price[len(train_J)+i-1]-Jm_price[len(train_J)+i])+Gama_used[-1]*(J_price[len(train_J)+i]-J_price[len(train_J)+i-1]))
            if Y[i]-Gama_used[-1]*X[i]<=0:
                position.append(0)
                Gama_used.append(0)
                tradepoint.append(i)
            else:
                position.append(1)
                Gama_used.append(Gama_used[-1])
        else:
            netasset.append(netasset[i-1]-(Jm_price[len(train_J)+i-1]-Jm_price[len(train_J)+i])-Gama_used[-1]*(J_price[len(train_J)+i]-J_price[len(train_J)+i-1]))
            if Y[i]-Gama_used[-1]*X[i]>=0:
                position.append(0)
                Gama_used.append(0)
                tradepoint.append(i)
            else:
                position.append(-1)
                Gama_used.append(Gama_used[-1])
netasset_s = pd.Series(netasset)
netasset_s.index = X.index
plt.plot(netasset_s)
plt.axhline(0, color="red", linestyle="--")
plt.xlabel("Time"); plt.ylabel("asset")
plt.title('fre=5min,k=5')

AR = ((netasset[-1]+J_price[0])/(J_price[0]))**(12/16)-1
AR_B = ((netasset[-1]+0.15*J_price[0])/(0.15*J_price[0]))**(12/16)-1
sharp = AR/(np.std(np.diff(netasset)/(J_price[0]+netasset)[ :-1])*np.sqrt(250*24*12))
sharp_B = AR_B/(np.std(np.diff(netasset)/(0.15*J_price[0]+netasset)[ :-1])*np.sqrt(250*24*12))
MD_B = max_drawdown(netasset+0.15*J_price[0])
MD = max_drawdown(netasset+J_price[0])
print(AR,AR_B,sharp,sharp_B,MD,MD_B)
