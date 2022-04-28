#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 12:56:26 2022

@author: juan

This is the main class for the definition of trading functions.
Any new class should include AT LEAST all the classes in the UNIV2




"""

class UNIV2:
    
    """
    
    Here the pricing function should be of the form 
    
    
    RQ=(R+gamma r)(Q-q)=k
    
    """
    
    
    def __init__(self,fee,reserves_quote,reserves_base):
        '''
        

        Parameters
        ----------
        fee : float, in (0,1)
            Fee for the AMM.
        reserves_quote : float
            reserves from quote currency (USDC).
        reserves_base : float
            reserves from the base currency (ETH) .

        Returns
        -------
        None.

        '''
        
        self.fee=fee
        self.reserves_quote=reserves_quote
        self.reserves_base=reserves_base
        self.gamma=1-fee
        self.k=reserves_quote*reserves_base
        
    def get_reference_price(self):
        '''
        

        Returns
        -------
        float
            returns the reference price from this AMM; R_quote/R_base.

        '''
    
        
        return self.reserves_quote/self.reserves_base
    
    def get_slippage(self,amount,side):
        '''
        determines the slippage given by the UNI curve

        Parameters
        ----------
        amount : float
            transaction amount in quote currency.
        side : str: 'buy' or 'sell'
            buy removes liquidity of BASE amount and adds quote. sell does the opposite

        Returns
        -------
        float
            slippage: "quoted" price vs "filled" price.

        '''
        return self.get_reference_price()-self.quote_trade(amount, side)
    

    
    def get_k(self):
        '''
        

        Returns
        -------
        str
            returns the constant in the AMM.

        '''
        return self.reserves_base*self.reserves_quote
    
    
    def quote_trade(self,amount,side):
        '''
        determines the base amount to be traded given a quote amount and a side (buy or sell)

        Parameters
        ----------
        amount : float
            transaction amount in quote currency.
        side : str: 'buy' or 'sell'
            buy removes liquidity of BASE amount and adds quote. sell does the opposite

        Returns
        -------
        Db : float
            amount of base to be added/removed given some quote amunt and a side.

        '''
        
        if side=='buy': # removes Db liquidity of base amount, with resere Rb
            # this means that one has (Rb-Db)(Rq+gammaDq)=k
            Db=self.reserves_base-(self.k)/(self.gamma*amount+self.reserves_quote)
        elif side=='sell':
            #adds liquidity of base amount
            Db=(self.k/(self.reserves_quote-amount)-self.reserves_base)/self.gamma
        else:
            raise('side has to be sell or buy!')
        return Db
    
    def execute_trade(self,amount,side):
        '''
        Executes trade and updates reserves and K. 
        For simplicity a trader buys or sells an amount `amount` of quote worth of base.
        This amount gets computed by calling quote trade and then reserves get updated. 

        Parameters
        ----------
        amount : float
            transaction amount in quote currency.
        side : str: 'buy' or 'sell'
            buy removes liquidity of BASE amount and adds quote. sell does the opposite

        Returns
        -------
        None.

        '''
        Db=self.quote_trade(amount,side)
        #executes and updates
        if side=='buy':
            self.reserves_base=self.reserves_base-Db
            # implicitly, these steps already include the new fee
            self.reserves_quote=self.reserves_quote+amount
        elif side=='sell':
            self.reserves_base=self.reserves_base+Db
            self.reserves_quote=self.reserves_quote-amount
        else:
            raise('side has to be sell or buy!')
        #updates K
        self.k=self.reserves_base*self.reserves_quote
        
        
        
            
        
        
        
        
        
        
        
    
        
        
        