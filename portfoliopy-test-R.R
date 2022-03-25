library(reticulate)
source_python("portfoliopy.py")
prices=as.data.frame(EuStockMarkets)
dates=as.vector(time(EuStockMarkets))
matplot(x=dates,y=apply(prices,2,function(x)x/x[1]),col=1:ncol(prices),type="l",
        xlab="date",ylab="value")
legend("top", colnames(prices),col=seq_len(ncol(prices)),cex=0.8,fill=seq_len(ncol(prices)))

sr<-prices2sreturns(prices)
ew.sr<-equal_weights_portfolio(sr)
ew.w<-sreturns2wealth(ew.sr)

rand.sr<-backtest_strategy(random_strategy,sr,forward=as.integer(100),args=as.integer(2))
rand.w<-sreturns2wealth(rand.sr)

inv.var.sr<-backtest_strategy(inv_V_strategy,sr,forward=as.integer(100),args=NULL)
inv.var.w<-sreturns2wealth(inv.var.sr)

inv.beta.sr<-backtest_strategy(inv_B_strategy,sr,forward=as.integer(100),args=NULL)
inv.beta.w<-sreturns2wealth(inv.beta.sr)

ports<-cbind(random=rand.w,inv.var=inv.var.w,inv.beta=inv.beta.w,
             ew=tail(ew.w,length(rand.w))/tail(ew.w,length(rand.w))[1])
matplot(x=tail(dates,length(rand.w)),y=ports,col=1:ncol(ports),type="l",xlab="date",ylab="value")

legend("top", colnames(ports),col=seq_len(ncol(ports)),cex=0.8,fill=seq_len(ncol(ports)))

# strategy_R<-function(sreturns,args=NULL){
#   dd=ncol(sreturns)
#   return(rep(1/dd,dd))
# }
# 
# Rstrat.sr<-backtest_strategy(strategy_R,sr,forward=as.integer(100),args=NULL,port_type="cr")
# 
# plot(Rstrat.sr,tail(ew.sr,length(Rstrat.sr)))
# 
# plot(ew.sr,as.matrix(sr)%*%rep(1/4,4))
# plot(Rstrat.sr,tail(as.matrix(sr)%*%rep(1/4,4),length(Rstrat.sr)))