alldata=read.csv("washed1min.txt")
alldata[,2]=ceiling(alldata[,2]-0.1)
n=nrow(alldata)

i=1
while (i<n){
  if ((alldata[i,2]%%100)%%5==0){
    if (alldata[i+4,2]==(alldata[i,2]+4)){
      i=i+5
    }else{
      alldata[i,1]=NA
      i=i+1
    }
  }else{
    alldata[i,1]=NA
    i=i+1
  }
}
alldata=na.omit(alldata)
n=nrow(alldata)

n5=n/5
temp5=matrix(NA,nrow = n5,ncol = 8)
for (i in 1:n5){
  temp5[i,1]=alldata[5*i-4,1]
  temp5[i,2]=alldata[5*i-4,2]
  temp5[i,3]=alldata[5*i-4,3]
  temp5[i,6]=alldata[5*i,6]
  temp5[i,8]=alldata[5*i,8]
  temp5[i,7]=sum(alldata[(5*i-4):(5*i),7])
  max=0
  min=9999
  for (j in (5*i-4):(5*i)){
    if (alldata[j,4]>max){
      max=alldata[j,4]
    }
    if (alldata[j,5]<min){
      min=alldata[j,5]
    }
  }
  temp5[i,4]=max
  temp5[i,5]=min
}
write.csv(temp5,file = "5min.txt",quote = FALSE,row.names = FALSE)

i=1
while (i<n){
  if ((alldata[i,2]%%100)%%15==0){
    if (alldata[i+14,2]==(alldata[i,2]+14)){
      i=i+15
    }else{
      alldata[i,1]=NA
      i=i+1
    }
  }else{
    alldata[i,1]=NA
    i=i+1
  }
}
alldata=na.omit(alldata)
n=nrow(alldata)

n15=n/15
temp15=matrix(NA,nrow = n15,ncol = 8)

for (i in 1:n15){
  temp15[i,1]=alldata[15*i-14,1]
  temp15[i,2]=alldata[15*i-14,2]
  temp15[i,3]=alldata[15*i-14,3]
  temp15[i,6]=alldata[15*i,6]
  temp15[i,8]=alldata[15*i,8]
  temp15[i,7]=sum(alldata[(15*i-14):(15*i),7])
  max=0
  min=9999
  for (j in (15*i-14):(15*i)){
    if (alldata[j,4]>max){
      max=alldata[j,4]
    }
    if (alldata[j,5]<min){
      min=alldata[j,5]
    }
  }
  temp15[i,4]=max
  temp15[i,5]=min
}
write.csv(temp15,file = "15min.txt",quote = FALSE,row.names = FALSE)