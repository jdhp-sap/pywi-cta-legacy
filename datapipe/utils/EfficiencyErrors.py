from math import factorial, log, exp, gamma, pi
import numpy as np
from scipy.optimize import minimize

from itertools import count

''' method from the paper
Calculating Efficiencies and Their
Uncertainties
Marc Paterno
FNAL/CD/CEPA/SLD
paterno@fnal.gov
May 5, 2003
'''





__all__ = [
            "get_efficiency_errors",
            #"get_efficiency_errors_minimize",
            #"get_efficiency_errors_scan",
            ]


def log_gamma(end,start=1):
    ''' 
        calculating log(Γ(x)) as the sum of the logarithms 
        of all integers in [1, x)
        a second argument can be used to set an alternative start
        e.g. if you have Γ(N) / Γ(k) -> Γ(N,k) sums all in [k,N)
        
        Parameters:
        -----------
        end : integer
            (not included) end of the sum
        start : integer, default: 1
            start of the sum
        
        Note:
        -----
        Γ(x) = (x-1)! 
        so @end doesn't neet to be included in sum
        
        if @start > @end, return the negative instead
    '''

    return np.sign(end-start) * sum( log(i) for i in np.arange(min(start,end),max(start,end)) )
    
    
def P_e (k, N, e):
    '''
        probability density function for the efficiency @e of passing @k events while observing @N
        
        Parameters:
        ----------
        k: integer
            number of events passing selection
        N : integer
            total number of events
        e : float
            test-efficiency
            0 <= e <= 1
        
        Returns:
        --------
        P : float
            the probability density to have a real efficiency of e
            while observing k out of N events passing a selection
        
    '''
    
    
    ''' has problems with high numbers ( Γ(100) gets HUUUUGE), use log-version instead '''
    #res1 = gamma(N+2) / (gamma(k+1)*gamma(N-k+1)) * e**k * (1-e)**(N-k)
    #return res1
    
    ''' protect from log(0) calls '''
    if e == 0:
        if k == 0: return 6
        else:      return 0
    if e == 1:
        if k == N: return 6
        else:      return 0
    if abs(e-.5) > .5: return 0
    
    ''' log-ed version '''
    #res2 = log_gamma(N+2)     + k*log(e) + (N-k)*log(1-e) - log_gamma(N-k+1) - log_gamma(k+1)
    #return exp(res3)
    
    ''' optimised version (sum_{0..N} - sum_{0..k} = sum_{k..N}) '''
    res3 = log_gamma(N+2,k+1) + k*log(e) + (N-k)*log(1-e) - log_gamma(N-k+1)
    return exp(res3)

    
def get_b_from_a(a,k,N, conf=.68,de=.001, func=P_e):
    '''
        determines b from a so that the intervall between them covers an intervall of conf
    '''
    b = a
    integral=0
    for i in count():
        integral += (func(k,N,b) + func(k,N,b+de))*de /2.
        b = a + i*de
        if integral >= .68: return (b,integral)
        if b+de > 1 :       return (9,integral)


def test_func(arg,k,N, conf=.68,de=.001, func=P_e):
    '''
        test function that calculates the 
        difference between a and b while covering an intervall of conf
    '''
    a = arg[0]
    (b,integral) = get_b_from_a(a, k, N, conf, de)
    if b <= 1: 
        test_func.min_a = a
        test_func.min_b = b
        return b-a
    else: return b


def get_efficiency_errors_minimize(k, N, conf=.68, de=0.0005) :
    if N == 0: return [0,0,0,0,0]
    
    test_func.min_diff=5.

    minimize(test_func, [0], args=(k,N,conf,de), bounds=[(0,1)],
             method='L-BFGS-B', options={'disp' : False, 'eps':1e-3}
            )    
    
    
    mean = k/N 
    if k == 0: test_func.min_b = 0
    if k == N: test_func.min_b = 1
    lerr = mean-test_func.min_a
    herr = test_func.min_b-mean
    
    return [mean, lerr, herr, test_func.min_a, test_func.min_b]

def get_efficiency_errors_scan(k, N, conf=.68, de=0.0005) :
    if N == 0: return [0,0,0,0,0]
    
    min_diff = 20.
    min_a = None
    min_b = None
    for i in count(0):
        a = i * de
        (b,integral) = get_b_from_a(a, k, N, conf, de)
        if b-a < min_diff: 
            min_diff = b-a
            min_a = a
            min_b = b
        if b > 1: break
    
    
    mean = k/N 
    if k == 0: min_a = 0
    if k == N: min_b = 1
    lerr = mean-min_a
    herr = min_b-mean
    
    return [mean, lerr, herr, min_a, min_b]


#get_efficiency_errors = get_efficiency_errors_scan
get_efficiency_errors = get_efficiency_errors_minimize



if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        pars = [2,5]
    else:
        pars = sys.argv[:2]
    
    print("get_efficiency_errors_scan({}, {}):".format(pars[0], pars[1])) 
    print(get_efficiency_errors_scan    (pars[0], pars[1])) 
    print("get_efficiency_errors_minimize({}, {}):".format(pars[0], pars[1])) 
    print(get_efficiency_errors_minimize(pars[0], pars[1])) 

    
    import numpy as np
    import matplotlib.pyplot as plt

    
    print("creating test distributions for N=5 and k = {0,...,5}")
    dt = 0.001
    t = np.arange(0.0, 1.+dt, dt)
    y0 = [P_e(0,5,x) for x in t]
    y1 = [P_e(1,5,x) for x in t]
    y2 = [P_e(2,5,x) for x in t]
    y3 = [P_e(3,5,x) for x in t]
    y4 = [P_e(4,5,x) for x in t]
    y5 = [P_e(5,5,x) for x in t]



    print( "integral of test distributions (should be 1)")
    print( "k=0: ", sum(y0) * dt )
    print( "k=1: ", sum(y1) * dt )
    print( "k=2: ", sum(y2) * dt )
    print( "k=3: ", sum(y3) * dt )
    print( "k=4: ", sum(y4) * dt )
    print( "k=5: ", sum(y5) * dt )




    plt.figure(1)
    plt.plot(y0, 'bo', y1, 'ro', y2, 'yo', y3, 'go', y4, "bo", y5, "ro")
    plt.show()

