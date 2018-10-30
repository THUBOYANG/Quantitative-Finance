%训练集生成
x1=CLOSE(21:401);
x2=HIGH(21:401);
x3=LOW(21:401);
x4=CLOSE(20:400);
x5=HIGH(20:400);
x6=LOW(20:400);
x7=(CLOSE(21:401)+CLOSE(20:400)+CLOSE(19:399)+CLOSE(18:398)+CLOSE(17:397))./5;
x8=(HIGH(21:401)+HIGH(20:400)+HIGH(19:399)+HIGH(18:398)+HIGH(17:397))./5;
x9=(LOW(21:401)+LOW(20:400)+LOW(19:399)+LOW(18:398)+LOW(17:397))./5;
x10=x1;
x11=x2;
x12=x3;
for i=1:19
    x10=x10+CLOSE((21-i):(401-i));
    x11=x11+HIGH((21-i):(401-i));
    x12=x12+LOW((21-i):(401-i));
end
x10=x10/20;
x11=x11/20;
x12=x12/20;
x13=IVIX(21:401);
x14=VIX(21:401);
x15=SP500(21:401);
x16=DollarCR(21:401);
Y=[CLOSE(22:402) HIGH(22:402) LOW(22:402)];
%PCA
X=[x1 x2 x3 x4 x5 x6 x7 x8 x9 x10 x11 x12 x13 x14 x15 x16];
%sddata=zscore(X);%数据标准化
%[p,princ,egenvalue]=princomp(sddata);%调用主成分
%per=100*egenvalue/sum(egenvalue);%各个主成分所占百分比
%p=p(:,1:4);%输出前4个主成分系数
%sc=princ(:,1:4);%前4主成分量
%测试集生成
tx1=CLOSE(402:485);
tx2=HIGH(402:485);
tx3=LOW(402:485);
tx4=CLOSE(401:484);
tx5=HIGH(401:484);
tx6=LOW(401:484);
tx7=(CLOSE(402:485)+CLOSE(401:484)+CLOSE(400:483)+CLOSE(399:482)+CLOSE(398:481))./5;
tx8=(HIGH(402:485)+HIGH(401:484)+HIGH(400:483)+HIGH(399:482)+HIGH(398:481))./5;
tx9=(LOW(402:485)+LOW(401:484)+LOW(400:483)+LOW(399:482)+LOW(398:481))./5;
tx10=tx1;
tx11=tx2;
tx12=tx3;
for i=1:19
    tx10=tx10+CLOSE((402-i):(485-i));
    tx11=tx11+HIGH((402-i):(485-i));
    tx12=tx12+LOW((402-i):(485-i));
end
tx10=tx10./20;
tx11=tx11./20;
tx12=tx12./20;
tx13=IVIX(402:485);
tx14=VIX(402:485);
tx15=SP500(402:485);
tx16=DollarCR(402:485);
tY=[CLOSE(403:486) HIGH(403:486) LOW(403:486)];
testX=[tx1 tx2 tx3 tx4 tx5 tx6 tx7 tx8 tx9 tx10 tx11 tx12 tx13 tx14 tx15 tx16];
%sddata_test=zscore(testX);
%sc_test=sddata_test*p;
%统一归一化
%Totalsc=[sc;sc_test];
%[Totalsc,PS1]=mapminmax(Totalsc',0,1);
%[Y,PS2]=mapminmax(Y',0,1);
%sc=Totalsc(:,1:381);
%sc_test=Totalsc(:,382:465);
%构建BP网络
scale = [0 1]
for i = 1:15
    scale = [scale ; 0 1]
end
net=newff(scale,[1 3],{'logsig','purelin'},'traingdx','learngdm','mse')
%设置参数
net=init(net)
net.trainParam.goal=1e-5;
net.trainParam.epochs=5000;
net.trainParam.lr=0.55;
net.trainParam.mc=0.9;
%开始训练
[net,tr]=train(net,X',Y');    
%将训练出的网络在测试集上检验
Y_test=sim(net,testX');
%Y_test=mapminmax('reverse',Y_test,PS2);
error=Y_test'-tY;
MSE=sum(error.^2);