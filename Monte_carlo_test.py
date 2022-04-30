#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Main (v)AMM simulator 

This simulates the price discovery position of an AMM. 


Created on Wed Apr  6 14:16:58 2022

@author: juan
"""
import numpy as np
import matplotlib.pyplot as plt
from gbm import genPsi as generate_oracle
import amm as amm
import trading_logics 
import inner_simmulator as mc
import distributions as dists

#defines some initial parameters
SECONDS_IN_A_YEAR=3600*24*356
#defines rate in seconds
RATE_COSTUMERS_IN_SECONDS=140

# rate in $$ for each transaction
RATE_AMOUNT=2000
#defines rate in years. this is the one we will need
RATE_COSTUMERS=RATE_COSTUMERS_IN_SECONDS/(SECONDS_IN_A_YEAR) 
# number of native coins in the initial reserve
INITIAL_RESERVE=1000
# time in years for which we run the simulation
FINAL_TIME=0.5
# defines how often we look at the oracle. 
HOURS_IN_A_YEAR=24*365
# by default, we check the oracle every hour 
dt=FINAL_TIME/HOURS_IN_A_YEAR
# Here we define some hyper-parameters for the GBM model of for the price
R=0.3 #risk-free interest rate
SIGMA=0.6 #volatility
#price at time 0. 
INITIAL_PRICE=3200
# nominal fee for the AMM
AMM_FEE=0.3/100 #

gamma=1-AMM_FEE
market_logic=trading_logics.simple_logic


N_samps=100
results=[]
qoi=np.zeros(N_samps)
#runs the Monte Carlo part

for i in range(N_samps):
    
    print('Iteration '+str(i))
    #generates a list of prices that we will look at 
    oracle_price=generate_oracle(T=FINAL_TIME,
                                 N=HOURS_IN_A_YEAR,
                                 r=R,
                                 sigma=SIGMA,
                                 S0=INITIAL_PRICE)
    
    time_in_hours=np.linspace(0,1,HOURS_IN_A_YEAR)
    #instantiates AMM
    #the initial reserve
    LAMBDA=0.5#np.random.random()
    W_BASE=0.5#np.random.random()
    W_QUOTE=0.5#1-W_BASE
    initial_quote_reserve=INITIAL_PRICE**(1/LAMBDA)*INITIAL_RESERVE*W_QUOTE/W_BASE
    # initializes the AMM object
    AMM=amm.lambdaAMM(fee=AMM_FEE,
                 reserves_base=INITIAL_RESERVE,
                 reserves_quote=initial_quote_reserve,
                 w_quote=W_QUOTE,w_base=W_BASE,l=LAMBDA) # trading function=None uses a CFMM, just like UNIV2
    
    dx_dist=dists.exponential(rate=RATE_AMOUNT)
    dt_dist=dists.exponential(rate=RATE_COSTUMERS)
    
    params={
            'amm':AMM,
            'final_time':FINAL_TIME,
            'dt_dist':dt_dist,
            'dx_dist':dx_dist,
            'initial_price':INITIAL_PRICE,
            'oracle_price':oracle_price,
            'market_logic':market_logic,
            'amm_fee':AMM_FEE
            }
    
    
        
    
    results.append(mc.inner_loop(params))
    # let's look average wealth at time T

    qoi[i]=100*(results[i]['wealth'].iloc[-1]-results[i]['wealth'].iloc[0])/results[i]['wealth'].iloc[0]

print('results')
print('E[W] ± 95%% CI')
print(str(qoi.mean())+' ± '+str(1.98*qoi.std()/N_samps**0.5))





