fivemin=read.csv("5min.txt")
daydata=read.csv("1day.txt")
n=nrow(fivemin)
m=nrow(daydata)
start=1:2000
j=2
for (i in 2:n){
  if (fivemin[i,1]!=fivemin[i-1,1]){
    start[j]=i
    j=j+1
  }
}
start[j]=i+1

fivemin=fivemin[,1:6]
daydata=cbind(daydata,daydata[,1],daydata[,1])
rate=0.0005
present=0
stop=0
sum=0
num=0
win=0
for (k in 2:m){
  for (i in start[k]:(start[k+1]-1)){
    gap=(daydata[k-1,3]-daydata[k-1,4])/2
    if (fivemin[i,6]>daydata[k-1,3]){
      if (stop==0){
        if (present==0){
          sum=sum+(present-1)*fivemin[i,6]*(1+rate)
          present=1
          num=num+1
        }
        if (present==-1){
          sum=sum+(present-1)*fivemin[i,6]*(1+rate)
          present=1
          num=num+1
        }
        if (present==1){
          if ((fivemin[i,6]-daydata[k-1,3])>0.4*gap){
            stop=1
            sum=sum+present*fivemin[i,6]-fivemin[i,6]*rate
            present=0
            num=num+1
            win=win+1
          }
        }
      }
    }else{
      if (fivemin[i,6]<daydata[k-1,4]){
        if (stop==0){
          if (present==1){
            sum=sum+(present+1)*fivemin[i,6]*(1-rate)
            present=-1
            num=num+1
          }
          if (present==0){
            sum=sum+(present+1)*fivemin[i,6]*(1-rate)
            present=-1
            num=num+1
          }
          if (present==-1){
            if (abs(fivemin[i,6]-daydata[k-1,3])>0.4*gap){
              stop=1
              sum=sum+present*fivemin[i,6]-fivemin[i,6]*rate
              present=0
              num=num+1
              win=win+1
            }
          }
        }
      }else{
        if (stop==1){
          stop=0
        }else{
          if (present==1){
            if ((daydata[k-1,3]-fivemin[i,6])>0.1*gap){
              sum=sum+present*fivemin[i,6]-fivemin[i,6]*rate
              present=0
              num=num+1
            }
          }
          if (present==-1){
            if ((fivemin[i,6]-daydata[k-1,4])>0.1*gap){
              sum=sum+present*fivemin[i,6]-fivemin[i,6]*rate
              present=0
              num=num+1
            }
          }
        }
      }
    }
  }
  if (present!=0){
    sum=sum+present*fivemin[i,6]-fivemin[i,6]*rate
    present=0
    num=num+1
  }
  daydata[k,6]=sum
}
