import numpy as np
#Calculates simple returns from prices
#prices is a 2d numpy array with columns being asset prices
#or a 1D array of a single asset's prices
def prices2sreturns(prices):
  d=len(prices.shape)
  if d==1:
    return prices[1:] / prices[:-1] - 1
  else:
    return prices[1:,:] / prices[:-1,:] - 1


#Calculates wealth/prices from simple returns
#sreturns is a 1D array of an asset's returns
def sreturns2wealth(sreturns,s0=1):
    return np.insert(s0*np.cumprod(1+sreturns),0,s0)
  
# x = np.array([[1, 4], 
#               [2, 5],
#               [3, 6]])
# prices2sreturns(x)
# x = np.array([1.0, 2, 3,4])
# prices2sreturns(x)
# r=np.array([0.5, 0.5, 0.1,-0.5])
# sreturns2wealth(r,1)
# np.all(sreturns2wealth(prices2sreturns(x),x[0])==x)


