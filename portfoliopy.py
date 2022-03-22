import numpy as np
import pandas as pd
#import ipdb

#returns a pandas data frame of simple returns
#prices is a pandas data frame with columns being asset prices
def prices2sreturns(prices):
  sreturns = prices.pct_change()
  sreturns = sreturns.drop(sreturns.index[0])
  return sreturns

#returns a pandas series of wealth/prices from simple returns
#sreturns is a pandas series of an asset's returns
def sreturns2wealth(sreturns,s0=1.0):
    sreturns=pd.Series(sreturns)
    wealth = s0*(1+sreturns).cumprod()
    #new_index = [str(wealth.index[0]-1)]
    wealth = pd.Series(s0,index=[str(0)]).append(wealth)
    return wealth
  
#calculates the simple returns on a portfolio given list of weights ww
#sreturns is the pandas data of simple returns of the components,
#if rf (riskfree) is not none then first weight is assumed to be on the risk free asset
#with specified rf rate
#types of portfolios are: 
#"cr" - constantly rebalanced 
#"bah" - buy and hold
#"scr" - semi-constantly rebalanced, aka rebalanced every kk days
def portfoliosreturns(ww, sreturns, rf=None,port_type="bah",kk=2):
  if rf is not None:
    sreturns['rf']=rf
  if(port_type=="bah"):
    prices = sreturns.apply(sreturns2wealth)
    #ipdb.set_trace()
    wealth = prices.dot(list(ww))
    sreturns_p = prices2sreturns(wealth)
  elif(port_type=="cr"):
    sreturns_p = sreturns.dot(list(ww))
  else:
    nn=len(sreturns.index)
    BB = np.arange(0,nn,kk)
    BB = np.append(BB,nn+1)
    sreturns_p_a = pd.Series()
    for ii in range(1,len(BB)):
      sreturns_p_ii=pd.Series(portfoliosreturns(ww,sreturns.iloc[BB[ii-1]:BB[ii],:],rf,"bah"))
      sreturns_p_a=sreturns_p_a.append(sreturns_p_ii)
    sreturns_p = sreturns_p_a
    
  return sreturns_p

#takes a function strategy which takes sreturns as an argument, and args
#the strategy will be formed with length back, and recomputed every forward
#kk is used to semi-constantly rebalance and must be smaller than forward
#window type is either "tumbling" or "expanding"
def backtest_strategy(strategy, sreturns, rf=None,port_type="bah",back=2,
forward=3,kk=2,window_type="tumbling",args=None):
  if rf is not None:
    sreturns['rf']=rf
    
  nn=len(sreturns.index)
  if window_type=="tumbling":
    starts = np.arange(0,nn,forward)
  else:
    starts = np.repeat(0,len(np.arange(0,nn,forward)))

  ends = np.arange(back,nn,forward)
  ends = np.append(ends,nn)
  
  sreturns_p_a = pd.Series()
  for ii in range(0,len(starts)-1):
    sreturns_in=sreturns.iloc[starts[ii]:ends[ii],:]
    ww_ii=strategy(sreturns_in,args)
    sreturns_out=sreturns.iloc[ends[ii]:np.minimum((ends[ii]+forward),nn),:]
    sreturns_p_out=pd.Series(portfoliosreturns(ww_ii,sreturns_out,rf,port_type,kk))
    sreturns_p_a=sreturns_p_a.append(sreturns_p_out)
  
  sreturns_p=sreturns_p_a
  return sreturns_p

#generates random long-only portfolios with weights on size assets
def random_strategy(sreturns,size=2):
  dd=np.shape(sreturns)[1]
  weights = np.random.choice(np.arange(1,100),size=size,replace=True)
  weights = weights/sum(weights)
  assets = list(np.random.choice(np.arange(0,dd),size=size,replace=False))
  ww=pd.Series(np.repeat(0,dd))
  for ii in range(0,size):
    ww.loc[assets[ii]]=weights[ii]
  return ww

#equal weights benchmark portfolio
def equal_weights_portfolio(sreturns,port_type="cr",kk=2):
  dd=np.shape(sreturns)[1]
  return portfoliosreturns(np.repeat(1/dd,dd),sreturns,port_type=port_type,kk=kk)

x = pd.DataFrame([[1, 6,11],
              [2, 7,12],
              [3, 8,13],
               [4, 9,14],
               [5, 10,15],
               [3, 20,7],
               [2, 3,8],
               [2, 7,12],
               [2, 7,13]])
prices2sreturns(x)
r=pd.Series([0.5, 0.5, 0.1,-0.5])
sreturns2wealth(r,1.0)
np.all(np.isclose(sreturns2wealth(prices2sreturns(r),r[0]),r))
rs=prices2sreturns(x)
equal_weights_portfolio(rs)
equal_weights_portfolio(rs,port_type="bah")
equal_weights_portfolio(rs,port_type="scr")
random_strategy(rs,2)
backtest_strategy(strategy = random_strategy, sreturns = rs,forward=4,args=2)




