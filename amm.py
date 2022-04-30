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
        self.collected=0
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
        return self.get_reference_price()*self.quote_trade(amount, side)-amount
    

    
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
        side : str: 'buy' or 'sell', 'none'
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
        else: # keeps this for compatibility with other market logics
            Db=amount/self.get_reference_price()
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
        #updates K
        self.k=self.reserves_base*self.reserves_quote
        
#
#
#
#
#
#
#
#
#
#
#        
#

class lambdaAMM:

    def __init__(self, fee,  reserves_base,reserves_quote ,w_quote=0.5, w_base=0.5, l=0.5):
        '''


        Parameters
        ----------
        fee : float, in (0,1)
            Fee for the AMM.
        reserves_quote : float
            reserves from quote currency (USDC).
        reserves_base : float
            reserves from the base currency (ETH).
        w_quote : float
            weight for the quote currency
        w_base : float
            weight for the base currency
        l : float
            the mixture coefficient lambda (defines the mixture degree of CSMM and CMMM functions)


        Returns
        -------
        None.

        '''

        self.l = l
        self.fee = fee
        self.reserves_quote = reserves_quote
        self.reserves_base = reserves_base
        self.gamma = 1 - fee
        self.w_quote = w_quote
        self.w_base = w_base
        self.k = (w_base ** l) * (reserves_base ** (1 - l)) + (w_quote ** l) * (reserves_quote ** (1 - l))
        self.collected=0
    def get_reference_price(self):
        '''


        Returns
        -------
        float
            returns the reference price from this AMM; (w_base*R_quote/w_quote*R_base)**l.

        '''

        return ((self.w_base * self.reserves_quote)/(self.w_quote * self.reserves_base)) ** self.l

    def get_slippage(self, amount, side):
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
        return self.get_reference_price() * self.quote_trade(amount, side) - amount

    def get_k(self):
        '''


        Returns
        -------
        str
            returns the constant in the AMM.

        '''
        return (self.w_base ** self.l) * (self.reserves_base ** (1 - self.l)) + (self.w_quote ** self.l) * (
                    self.reserves_quote ** (1 - self.l))

    def quote_trade(self, amount, side):
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
            amount of base to be added/removed given some quote amount and a side.

        '''
        k=self.k
        l=self.l
        w_base=self.w_base
        w_quote=self.w_quote
        
        
        
        if side == 'buy':  # remove/buy base or equivalently add/sell quote
            reserves_quote_new = self.reserves_quote + self.gamma * amount
            rhs=(k-w_quote**l*reserves_quote_new**(1-l))/(w_base**l)
            rhs=rhs**(1/(1-l))
            Db=self.reserves_base-rhs
            
            
            # p1 = self.w_base ** (-self.l / (1 - self.l))
            # p2 = (self.k - (self.w_quote ** self.l) * (reserves_quote_new ** (1 - self.l))) ** (1 / (1 - self.l))
            # Db = self.reserves_base - p1 * p2

        elif side == 'sell':  # add/sell base or equivalently remove/buy quote
            reserves_quote_new = self.reserves_quote - amount
            rhs=(k-w_quote**l*reserves_quote_new**(1-l))/(w_base**l)
            rhs=rhs**(1/(1-l))
            Db=(rhs-self.reserves_base)/self.gamma
            
        else:
            Db=amount/self.get_reference_price()

        return Db

    def execute_trade(self, amount, side):
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
        Db = self.quote_trade(amount, side)
        # executes and updates
        if side == 'buy':
            self.reserves_base = self.reserves_base - Db
            # implicitly, these steps already include the new fee
            self.reserves_quote = self.reserves_quote + amount
            self.collected=self.fee*amount
        elif side == 'sell':
            self.reserves_base = self.reserves_base + Db
            self.reserves_quote = self.reserves_quote - amount
            self.collected=self.fee*Db*self.get_reference_price()
        else:
            self.collected=0
        # updates K
        self.k = self.get_k()














            
        
        
        
        
        
        
        
    
        
        
        