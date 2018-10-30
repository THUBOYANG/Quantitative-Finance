library(forecast)
library(tseries)
#get 5min data
data=read.csv('F:\\Tsinghua\\Seventh semester\\FinancialMathematics\\5min.txt');
#get close price
close=data$V6
#stationary test
plot(close,xlab='time')
acf(close)
adf.test(close)
acf(diff(close))
adf.test(diff(close))
pacf(diff(close))
a1=arima(close,order=c(0,1,1))
Box.test(a1$residuals,type='Ljung')

