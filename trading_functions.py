#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 12:56:26 2022

@author: juan
"""

class UNIV2:
    
    """
    
    Here the pricing function should be of the form 
    
    
    RQ=(R+gamma r)(Q-q)=k
    
    """
    
    
    def __init__(self,fee,reserves_quote,reserves_base):
        self.fee=fee
        self.reserves_quote=reserves_quote
        self.reserves_base=reserves_base
        self.gamma=1-fee
        
    def get_reference_price(self):
        return self.reserves_quote/self.reserves_base
    
    def get_slippage(self,amount,side):
        return self.get_reference_price()-self.quote_trade(amount, side)
    def get_k(self):
        return self.reserves_base*self.reserves_quote
    
    
    def quote_trade(self,amount,side):
        
        if side=='buy': # removes Db liquidity of base amount, with resere Rb
            # this means that one has (Rb-Db)(Rq+gammaDq)=k
            Db=self.reserves_base-(self.k)/(self.gamma*amount+self.reserves_quote)
        elif side=='sell':
            #adds liquidity of base amount
            Db=(self.k/(self.reserves_quote-amount+self.amount)-self.reserves_base)/self.gamma
        else:
            assert('side has to be sell or buy!')
        return Db
    
    def execute_trade(self,amount,side):
        Db=self.quote_trade(self,amount,side)
        #executes and updates
        if side=='buy':
            self.reserves_base=self.reserves_base-Db
            # implicitly, these steps already include the new fee
            self.reserves_quote=self.reserves_quote+amount
        elif side=='sell':
            self.reserves_base=self.reserves_base+Db
            self.reserves_quote=self.reserves_quote-amount
        #updates K
        self.k=self.re
        
        
        
            
        
        
        
        
        
        
        
    
        
        
        