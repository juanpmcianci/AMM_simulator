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
RATE_COSTUMERS_IN_SECONDS=14

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
R=0.2 #risk-free interest rate
SIGMA=0.6 #volatility
#price at time 0. 
INITIAL_PRICE=3200
# nominal fee for the AMM
AMM_FEE=1/100 #

gamma=1-AMM_FEE
market_logic=trading_logics.only_arb_zone
#generates a list of prices that we will look at 
oracle_price=generate_oracle(T=FINAL_TIME,
                             N=HOURS_IN_A_YEAR,
                             r=R,
                             sigma=SIGMA,
                             S0=INITIAL_PRICE)

time_in_hours=np.linspace(0,1,HOURS_IN_A_YEAR)
# Plots to check that everything makes sense
plt.plot(time_in_hours,oracle_price, label='simulated oracle price')
plt.plot(time_in_hours,oracle_price/gamma, label='UB simulated oracle price')
plt.plot(time_in_hours,oracle_price*gamma, label='LB simulated oracle price')

plt.legend()
plt.xlabel('Time (years)')
plt.ylabel('Price, USD')
plt.show()
#%%
#instantiates AMM
#the initial reserve
LAMBDA=np.random.random()
W_BASE=np.random.random()
W_QUOTE=1-W_BASE
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


res=mc.inner_loop(params)


#%%
time=res['time']
plt.plot(time,res['price_amm'])
plt.plot(time,res['price_oracle'])
plt.show()
cols=res.columns

for i in cols:
    if i!='time':
        plt.plot(time,res[i])
        plt.title(i)
        plt.show()


# price_amm=res['price_amm']
# price_oracle=res['price_oracle']
# slippage=res['slippage']
# reserves_base=res['reserves_base']
# reserves_quote=res['reserves_quote']
# k=res['k']




