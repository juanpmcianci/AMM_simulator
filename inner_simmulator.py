#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is in the inner loop function. this function gets called many times on the MC simulator
@author: juan
"""
import numpy as np
import pandas as pd
def inner_loop(parameters):
    
    HOURS_IN_A_YEAR=24*365
    
    # reads simulation parameters
    AMM=parameters['amm']
    final_time=parameters['final_time']
    dt_dist=parameters['dt_dist']
    dx_dist=parameters['dx_dist']
    initial_price=parameters['initial_price']
    oracle_price=parameters['oracle_price']
    market_logic=parameters['market_logic']
    amm_fee=parameters['amm_fee']
    
    time_in_hours=np.linspace(0,1,HOURS_IN_A_YEAR)

    #preallocates total time
    total_time=0
    price_evolution_AMM=[]
    price_evolution_oracle=[]
    reserves_quote_evolution=[]
    reserves_base_evolution=[]
    slippage_evolution=[]; slippage_evolution.append(0)
    track_k=[]
    track_collected_fee=[]
    time_list=[0]
    price_evolution_AMM.append(AMM.get_reference_price())
    price_evolution_oracle.append(initial_price)
    reserves_base_evolution.append(AMM.reserves_base)
    reserves_quote_evolution.append(AMM.reserves_quote)
    track_k.append(AMM.get_k())
    trx_evolution=[];trx_evolution.append(0)
    track_arb_opportunities=[]; track_arb_opportunities.append(0)
    
    track_collected_fee.append(AMM.collected)
    #%%
    while total_time< final_time:
        
        #samples a random time increment from an exponential with rate RATE_CUSTOMERS
        ##TODO: make rates depend on the state of the market
        dt=dt_dist.sample()
        #updates time
        total_time+=dt
        time_list.append(total_time)
    
    
        
        #checks for arbitrage opportunities.
        current_amm_price=AMM.get_reference_price()
        #appends oracle price to list for comparisson
        current_oracle_price=oracle_price[np.argmin(time_in_hours<total_time)-1]
        # decices whether a buy or a sell happens. The arbitrage is encoded here
        side,arb_zone=market_logic(current_amm_price,current_oracle_price,amm_fee)
    
        price_evolution_AMM.append(current_amm_price)
        price_evolution_oracle.append(current_oracle_price)    
            
        # samples random amount    
        random_amount=dx_dist.sample()
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
        track_k.append(AMM.get_k())
        track_collected_fee.append(AMM.collected)
    
    
    V_held=np.array(reserves_quote_evolution[0]+np.array(price_evolution_oracle)*reserves_base_evolution[0])
    wealth=np.array(reserves_quote_evolution)+np.array(price_evolution_oracle)*np.array(reserves_base_evolution)
    #output traced quantities
    tracer={
        'time':np.array(time_list),
        'price_amm':np.array(price_evolution_AMM),
        'price_oracle':np.array(price_evolution_oracle),
        'slippage':np.array(slippage_evolution),
        'reserves_base':np.array(reserves_base_evolution),
        'reserves_quote':np.array(reserves_quote_evolution),
        'k':np.array(track_k),
        'fee':np.array(track_collected_fee),
        'trx':np.array(trx_evolution),
        'wealth':wealth,
        'IL':(wealth-V_held)/V_held,
        'arbs':np.array(track_arb_opportunities)
        }

    return pd.DataFrame(tracer)
    
    
