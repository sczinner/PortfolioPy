library(reticulate)
source_python("portfoliopy.py")
prices=as.data.frame(EuStockMarkets)
matplot(x=1:nrow(prices),y=apply(prices,2,function(x)x/x[1]),col=1:ncol(prices),type="l")
sr<-prices2sreturns(prices)
ew.sr<-equal_weights_portfolio(sr)
ew.w<-sreturns2wealth(ew.sr)
points(1:length(ew.w),ew.w,col=5,type="l")


random_strategy(sr,as.integer(3))

rand.sr<-backtest_strategy(random_strategy,sr,forward=as.integer(100),args=as.integer(2))
rand.w<-sreturns2wealth(rand.sr)
plot(1:length(rand.w),rand.w,type="l")

for(ii in 2:10){
  rand.sr<-backtest_strategy(random_strategy,sr,forward=as.integer(100),args=as.integer(2))
  rand.w<-sreturns2wealth(rand.sr)
  points(1:length(rand.w),rand.w,type="l",col=ii)
}
