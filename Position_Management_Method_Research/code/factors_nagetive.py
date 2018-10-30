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
rate=0.0005
money=10000
propertyrecord=[]
f1predict=[]
f2predict=[]

for k in range(10):
    num=0
    status=0
    price=[]
    factor1=[]#5分钟平均交易量/20分钟平均交易量
    factor2=[]
    f1=[]
    f2=[]
    g=[]
    clf1 = linear_model.LinearRegression()
    clf2 = linear_model.LinearRegression()
    for i in range(10000*k,10000*(k+1)):
        if fivemindata[i][0]>N:
            if fivemindata[i][5]>daydata[fivemindata[i][0]][6]:
                #价格突破上轨，做多
                if status<1:
                    if fivemindata[i][0]==fivemindata[i+1][0]:
                        #收盘时刻无法交易，需要剔除
                        price.append(fivemindata[i][5])
                        status=1
                        if num==1:
                            g.append(-(price[len(price)-1]-price[len(price)-2])/price[len(price)-2])
            if fivemindata[i][5]<daydata[fivemindata[i][0]][7]:
                #价格跌破下轨，做空
                if status>-1:
                    if fivemindata[i][0]==fivemindata[i+1][0]:
                        #收盘时刻无法交易，需要剔除
                        price.append(fivemindata[i][5])
                        status=-1
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
                        if len(g)>5:
                            clf1.fit(factor1,g)
                            clf2.fit(factor2,g)
                            f1.append(clf1.predict(vratio)[0])
                            f2.append(clf2.predict(sd5/sd20)[0])
                        factor1.append([vratio])
                        factor2.append([sd5/sd20])
                        num=1
    result=np.corrcoef(np.array([f1[0:len(g)-6],f2[0:len(g)-6],g[6:len(g)]]))
    f1predict.append(result[2,0])
    f2predict.append(result[2,1])
x=range(len(f1predict))
plt.figure() 
plt.plot(x,f1predict,'ro')
plt.plot(x,f2predict,'ro')