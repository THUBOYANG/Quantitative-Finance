import os
import numpy as np
import pylab
import matplotlib.pyplot as plt
from sklearn import linear_model

"""
k1,k2,N为模型参数
daydata为日数据，daydata[1:7]保存着当日的开盘价、最高价、最低价、收盘价、模型的range、上轨、下轨
fivemindata为五分钟数据，fivemindata[0:7]保存着日期、时间、五分钟内的开盘价、最高价、最低价、收盘价、交易量、持仓量
"""
daydata=[]
fivemindata=[]
k1=0.2
k2=0.2
N=5

os.chdir("E:\\pythonfile\\")
f=open("1day.txt")
g=open("5min.txt")

while True:
    line = f.readline()
    if len(line) == 0:
        break
    daydata.append(list(map(int,line.split('\t'))))

while True:
    line = g.readline()
    if len(line) == 0:
        break
    fivemindata.append(list(map(int,line.split('\t'))))
    
#h为之前N日的最高价，c为之前N日的收盘价，l为之前N日的最低价
h=[]
c=[]
l=[]
for i in range(N):
    h.append(daydata[i][2])
    l.append(daydata[i][3])
    c.append(daydata[i][4])
    
for i in range(N+1,len(daydata)):
    h.pop(0)
    h.append(daydata[i-1][2])
    l.pop(0)
    l.append(daydata[i-1][3])
    c.pop(0)
    c.append(daydata[i-1][4])
    daydata[i][5]=max(max(h)-min(c),max(c)-min(l))
    daydata[i][6]=daydata[i][1]+k1*daydata[i][5]
    daydata[i][7]=daydata[i][1]-k2*daydata[i][5]

#以上为处理数据，以下为实施交易

"""
为简化问题，假设每次只交易一手，且暂不考虑加杠杆
status:状态记录，0为不持仓，1为多仓，-1为空仓
money:资金，初始为10000
rate:手续费率
"""
status=0
next=0
num=0
money=10000
propertyrecord=[]
rate=0.0005
factorp=[]#多仓
gp=[]#多仓实际收益
fp=[]
pricep=0#触发多仓时的价格
factorn=[]
gn=[]
pricen=0

clf = linear_model.LinearRegression()

for i in range(len(fivemindata)):
    if fivemindata[i][0]>N:
        if fivemindata[i][5]>daydata[fivemindata[i][0]][6]:
            #价格突破上轨，做多
            if status<0.5:
                if fivemindata[i][0]==fivemindata[i+1][0]:
                    #收盘时刻无法交易，需要剔除
                    if status<-0.5:
                        #空仓：算上次交易的收益
                        gn.append(-(fivemindata[i][5]-pricen)/pricen)
                    #计算因子
                    ave20=0
                    for j in range(4):
                        ave20=ave20+fivemindata[i-j][6]
                    vratio=4*fivemindata[i][6]/ave20               
                    temp=[]
                    for j in range(5):
                        temp.append(fivemindata[i-j][5])
                    sd5=np.var(temp)
                    for j in range(5,20):
                        temp.append(fivemindata[i-j][5])
                    sd20=np.var(temp)
                    #计算应变为的仓位，其中，数据量不够时按照1手
                    if len(gp)>10:
                        clf.fit(factorp,gp)
                        predictall=clf.predict(factorp)
                        lm=clf.predict([[vratio,sd5/sd20]])[0]
                        predictp=(lm-np.mean(predictall))/np.var(predictall)
                        if predictp>0.5:
                            next=2
                        else:
                            if predictp<-0.5:
                                next=0
                                if status==0:
                                    #平仓+弱信号时，其实没交易
                                    num=num-1
                            else:
                                next=1
                    else:
                        next=1
                    num=num+1
                    if next!=0:
                        pricep=fivemindata[i][5]
                        factorp.append([vratio,sd5/sd20])
                    money=money-fivemindata[i][5]*(next-status)*(1+rate)
                    status=next
        if fivemindata[i][5]<daydata[fivemindata[i][0]][7]:
            #价格跌破下轨，做空
            if status>-0.5:
                    if status>0.5:
                        #之前多仓：算上次交易的收益
                        gp.append((fivemindata[i][5]-pricep)/pricep)
                    #计算因子
                    ave20=0
                    for j in range(4):
                        ave20=ave20+fivemindata[i-j][6]
                    vratio=4*fivemindata[i][6]/ave20               
                    temp=[]
                    for j in range(5):
                        temp.append(fivemindata[i-j][5])
                    sd5=np.var(temp)
                    for j in range(5,20):
                        temp.append(fivemindata[i-j][5])
                    sd20=np.var(temp)
                    #计算应变为的仓位，其中，数据量不够时按照1手
                    if len(gn)>10:
                        clf.fit(factorn,gn)
                        predictall=clf.predict(factorn)
                        lm=clf.predict([[vratio,sd5/sd20]])[0]
                        predictn=(lm-np.mean(predictall))/np.var(predictall)
                        if predictn>0.5:
                            next=-2
                        else:
                            if predictn<-0.5:
                                next=0
                                if status==0:
                                    #平仓弱信号时，其实没交易
                                    num=num-1
                            else:
                                next=-1
                    else:
                        next=-1
                    num=num+1
                    if next!=0:
                        pricen=fivemindata[i][5]
                        factorn.append([vratio,sd5/sd20])
                    money=money-fivemindata[i][5]*(next-status)*(1-rate)
                    status=next
        propertyrecord.append(money+status*fivemindata[i][5])
x=range(len(propertyrecord))
plt.figure()  
plt.plot(x,propertyrecord)