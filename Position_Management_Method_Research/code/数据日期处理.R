alldata=read.csv("1mindata.txt",sep = '\t')
alldata[,2]=alldata[,2]*10000
alldata[,2]=ceiling(alldata[,2]-0.1)
subdata=cbind(alldata[,1],alldata[,1],alldata[,2])
n=nrow(alldata)
j=1
subdata[1,2]=1
for (i in 2:n){
  if (subdata[i,1]!=subdata[i-1,1]){
    j=j+1
  }
  subdata[i,2]=j
}
for (i in 1:n){
  if (subdata[i,3]>1800){
    subdata[i,2]=subdata[i,2]+1
  }
}
alldata[,1]=subdata[,2]
write.csv(alldata,file = "washed1min.txt",quote = FALSE,row.names = FALSE)