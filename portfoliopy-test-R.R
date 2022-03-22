library(reticulate)
source_python("portfoliopy.py")
prices=as.data.frame(EuStockMarkets)
matplot(x=1:nrow(prices),y=apply(prices,2,function(x)x/x[1]),col=1:ncol(prices),type="l")
sr<-prices2sreturns(prices)
ew.sr<-equal_weights_portfolio(sr)
ew.w<-sreturns2wealth(ew.sr)
points(1:length(ew.w),ew.w,col=5,type="l")

rand.sr<-backtest_strategy(random_strategy,sr,forward=as.integer(100),args=as.integer(2))
rand.w<-sreturns2wealth(rand.sr)

inv.var.sr<-backtest_strategy(inv_V_strategy,sr,forward=as.integer(100),args=NULL)
inv.var.w<-sreturns2wealth(inv.var.sr)

inv.beta.sr<-backtest_strategy(inv_B_strategy,sr,forward=as.integer(100),args=NULL)
inv.beta.w<-sreturns2wealth(inv.beta.sr)

ports<-cbind(rand.w,inv.var.w,inv.beta.w,tail(ew.w,length(rand.w))/tail(ew.w,length(rand.w))[1])
matplot(x=1:length(rand.w),y=ports,col=1:ncol(ports),type="l")
