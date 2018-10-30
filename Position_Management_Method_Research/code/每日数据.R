alldata=read.csv("1mindata.txt",sep = '\t')
alldata[,2]=alldata[,2]*10000
alldata[,2]=ceiling(alldata[,2]-0.1)
n=nrow(alldata)
j=1
daydata=matrix(NA,ncol = 5,nrow = 2500)
daydata[1,2]=alldata[1,3]
max=alldata[1,4]
min=alldata[1,5]
for(i in 2:n){
  if (alldata[i,1]!=alldata[i-1,1]){
    daydata[j,1]=alldata[i-1,1]
    daydata[j,5]=alldata[i-1,6]
    daydata[j+1,2]=alldata[i,3]
    daydata[j,3]=max
    daydata[j,4]=min
    max=alldata[i,4]
    min=alldata[i,5]
    j=j+1
  }else{
    if (alldata[i,4]>max){
      max=alldata[i,4]
    }
    if (alldata[i,5]<min){
      min=alldata[i,5]
    }
  }
}
daydata=na.omit(daydata)
write.csv(daydata,file = "1day.txt",quote = FALSE,row.names = FALSE)