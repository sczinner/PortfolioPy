import portfoliopy as pp
import numpy as np
import pandas as pd

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
pp.sreturns2wealth(r,1.0)
np.all(np.isclose(pp.sreturns2wealth(pp.prices2sreturns(r),r[0]),r))
rs=pp.prices2sreturns(x)
pp.equal_weights_portfolio(rs)
pp.equal_weights_portfolio(rs,port_type="bah")
pp.equal_weights_portfolio(rs,port_type="scr")
pp.random_strategy(rs,2)
pp.backtest_strategy(strategy = pp.random_strategy, sreturns = rs,args=2)


