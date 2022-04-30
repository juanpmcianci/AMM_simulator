#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 21:46:40 2022

@author: juan


In this file we write several logics for how the market (i.e., traders and arbitragers)
behave. 


"""
import numpy as np
def simple_logic(current,oracle,fee):
    '''
    here we define a set of very simple rules. 
 
     * If we are on an arbitrage region, perform arbitrage with probability 1
       here, given a market price m, an oracle price p, and a fee f in (0,1),
       the arbitrage region is 
       
       m such that m<(1-f)p  OR m>p/(1-f)
     
     
     
     * If we are on the no-arb region, do 50-50 chance of having a buy or a sell

    Parameters
    ----------
    current : float
        current AMM price.
    oracle : float
        current oracle price.
    fee : float in (0,1)
        DESCRIPTION.

    Returns
    -------
    side : str, 'buy', 'sell'
        whether there's a buy or a sell.
    arb_zone : int: -1, 0, 1
        -1: arbitrage, sell
        0: not in arb zone
        1: arbitrage, buy.

    '''

    '''
    
   
    
    '''
    gamma=1-fee
    arb_sell=current>oracle/gamma
    arb_buy=current<gamma*oracle
    
    if arb_sell:
        prob_buy=0
        side='sell'
        arb_zone=-1
    elif arb_buy:
        prob_buy=1
        side='buy'
        arb_zone=1
    else:
        prob_buy=0.5
        arb_zone=0
        
        if np.random.random()<prob_buy:
            side='buy'
        else:
            side='sell'
    
  
        
        
    return side, arb_zone

def only_arb_zone(current,oracle,fee):
    '''
    here we define a set of very simple rules. 
 
     * If we are on an arbitrage region, perform arbitrage with probability 1
       here, given a market price m, an oracle price p, and a fee f in (0,1),
       the arbitrage region is 
       
       m such that m<(1-f)p  OR m>p/(1-f)
     
     
     
     * No trade otherwise

    Parameters
    ----------
    current : float
        current AMM price.
    oracle : float
        current oracle price.
    fee : float in (0,1)
        DESCRIPTION.

    Returns
    -------
    side : str, 'buy', 'sell'
        whether there's a buy or a sell.
    arb_zone : int: -1, 0, 1
        -1: arbitrage, sell
        0: not in arb zone
        1: arbitrage, buy.

    '''

    '''
    
   
    
    '''
    gamma=1-fee
    arb_sell=current>oracle/gamma
    arb_buy=current<gamma*oracle
    
    if arb_sell:
        prob_buy=0
        side='sell'
        arb_zone=-1
    elif arb_buy:
        prob_buy=1
        side='buy'
        arb_zone=1
    else:
        side=None
        arb_zone=0
    
  
        
        
    return side, arb_zone
