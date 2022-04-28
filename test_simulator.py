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

#defines some initial parameters
SECONDS_IN_A_YEAR=3600*24*356
#defines rate in seconds
RATE_COSTUMERS_IN_SECONDS=14

# rate in $$ for each transaction
RATE_AMOUNT=1000
#defines rate in years. this is the one we will need
RATE_COSTUMERS=RATE_COSTUMERS_IN_SECONDS/(SECONDS_IN_A_YEAR) 
# number of native coins in the initial reserve
INITIAL_RESERVE=10000
# time in years for which we run the simulation
FINAL_TIME=1
# defines how often we look at the oracle. 
HOURS_IN_A_YEAR=24*365
# by default, we check the oracle every hour 
dt=FINAL_TIME/HOURS_IN_A_YEAR
# Here we define some hyper-parameters for the GBM model of for the price
R=0.5 #risk-free interest rate
SIGMA=0.6 #volatility
#price at time 0. 
INITIAL_PRICE=3200
# nominal fee for the AMM
AMM_FEE=0.3/100 #

gamma=1-AMM_FEE
market_logic=trading_logics.simple_logic
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
initial_base_reserve=INITIAL_PRICE*INITIAL_RESERVE
# initializes the AMM object
AMM=amm.UNIV2(fee=AMM_FEE,
             reserves_base=INITIAL_RESERVE,
             reserves_quote=initial_base_reserve) # trading function=None uses a CFMM, just like UNIV2

#preallocates total time
total_time=0
price_evolution_AMM=[]
price_evolution_oracle=[]
reserves_quote_evolution=[]
reserves_base_evolution=[]
slippage_evolution=[]

time_list=[0]
price_evolution_AMM.append(AMM.get_reference_price())
price_evolution_oracle.append(INITIAL_PRICE)
reserves_base_evolution.append(AMM.reserves_base)
reserves_quote_evolution.append(AMM.reserves_quote)
trx_evolution=[]
track_arb_opportunities=[]
#%%
while total_time< FINAL_TIME:
    
    #samples a random time increment from an exponential with rate RATE_CUSTOMERS
    dt=np.random.exponential(scale=RATE_COSTUMERS)
    #updates time
    total_time+=dt
    time_list.append(total_time)


    
    #checks for arbitrage opportunities.
    current_amm_price=AMM.get_reference_price()
    #appends oracle price to list for comparisson
    current_oracle_price=oracle_price[np.argmin(time_in_hours<total_time)-1]
    # decices whether a buy or a sell happens. The arbitrage is encoded here
    side,arb_zone=market_logic(current_amm_price,current_oracle_price,AMM_FEE)

    price_evolution_AMM.append(current_amm_price)
    price_evolution_oracle.append(current_oracle_price)    
        
    # samples random amount    
    random_amount=np.random.exponential(RATE_AMOUNT)
    #gets slippage
    slippage_evolution.append(AMM.get_slippage(random_amount,side))

    #updates AMM
    AMM.execute_trade(amount=random_amount,
                 side=side)
    
    #updates reserves
    reserves_base_evolution.append(AMM.reserves_base)
    reserves_quote_evolution.append(AMM.reserves_quote)
    trx_evolution.append(random_amount)
    track_arb_opportunities.append(arb_zone)

    


#%%


##% OUTPUTS RESULTS
skip=1
plt.title('Price evolution')
plt.plot(time_list[::skip],price_evolution_AMM[::skip],label='AMM price')
plt.plot(time_list[::skip],price_evolution_oracle[::skip],label='Oracle price')
plt.plot(time_list[::skip],0.95*np.array(price_evolution_oracle)[::skip],'--',color='white',label='LB Oracle price')
plt.plot(time_list[::skip],1.05*np.array(price_evolution_oracle )[::skip],'--',color='white',label=' UBOracle price')


plt.xlabel('Time (years)')
plt.ylabel('Price, USD')
plt.legend()
# import tikzplotlib
# tikzplotlib.save('sim.tex')
plt.show()

#
plt.title('K evolution')
plt.plot(time_list,np.log(np.array(reserves_quote_evolution)*np.array(reserves_base_evolution)),label='K')
plt.xlabel('Time (years)')
plt.ylabel('Units')
plt.legend()
plt.show()
#
plt.title('Lag  evolution')

plt.plot(time_list,100*(np.array(price_evolution_AMM)-np.array(price_evolution_oracle))/np.array(price_evolution_oracle ),label='AMM price - oracle')
plt.plot(time_list,0*np.array(price_evolution_AMM),'--')

plt.xlabel('Time (years)')
plt.ylabel('AMM price - Oracle')
plt.legend()
plt.show()
arb_zone=np.array(track_arb_opportunities)
labels=[-1,0,1]
arb=np.zeros(3)
ii=0
for i in labels:
    arb[ii]=np.sum([arb_zone==i])/len(arb_zone);
    ii+=1
#%%    
label=['yes, sell','None','yes, buy']
plt.pie(arb,  labels=label, autopct='%1.1f%%',
        shadow=True, startangle=90)
plt.axis('equal')
  

