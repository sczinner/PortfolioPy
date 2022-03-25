An example of using portfoliopy.py to backtest portfolio strategies
================

## Set up and data

tl;dr made functions which calculate portfolio returns and backtests
portfolio strategies.

I tested the Python functions in R using the reticulate library. First I
load the necessary libraries and sources, and then the data I will be
using

``` r
library(reticulate)
source_python("portfoliopy.py")
prices=as.data.frame(EuStockMarkets)
dates=as.vector(time(EuStockMarkets))
matplot(x=dates,y=apply(prices,2,function(x)x/x[1]),col=1:ncol(prices),type="l",
        xlab="index",ylab="value")
legend("top", colnames(prices),col=seq_len(ncol(prices)),cex=0.8,fill=seq_len(ncol(prices)))
```

![](README_files/figure-gfm/unnamed-chunk-1-1.png)<!-- -->

## Testing the portfolio functions with the included portfolio functions

Note that when using reticulate, to pass integers to Python functions,
we have to specify “as.integer(x)”. For these backtests, the strategies
are formed by looking backwards over 100 days and then holding for 100
days before recomputing.

``` r
sr<-prices2sreturns(prices)
ew.sr<-equal_weights_portfolio(sr)
ew.w<-sreturns2wealth(ew.sr)

rand.sr<-backtest_strategy(random_strategy,sr,back=as.integer(100),forward=as.integer(100),args=as.integer(2))
rand.w<-sreturns2wealth(rand.sr)

inv.var.sr<-backtest_strategy(inv_V_strategy,sr,back=as.integer(100),forward=as.integer(100),args=NULL)
inv.var.w<-sreturns2wealth(inv.var.sr)

inv.beta.sr<-backtest_strategy(inv_B_strategy,sr,back=as.integer(100),forward=as.integer(100),args=NULL)
inv.beta.w<-sreturns2wealth(inv.beta.sr)

ports<-cbind(random=rand.w,inv.var=inv.var.w,inv.beta=inv.beta.w,
             ew=tail(ew.w,length(rand.w))/tail(ew.w,length(rand.w))[1])
matplot(x=tail(dates,length(rand.w)),y=ports,col=1:ncol(ports),type="l",xlab="date",ylab="value")

legend("top", colnames(ports),col=seq_len(ncol(ports)),cex=0.8,fill=seq_len(ncol(ports)))
```

![](README_files/figure-gfm/pressure-1.png)<!-- -->

They all perform pretty much identically (although the random portfolios
obviously sometimes do better or worse). There is lots of room for more
tests with more assets, over longer time periods, and more sophisticated
strategies using these backtesting functions.
