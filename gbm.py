#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 14:24:19 2022

This generates a GBM

@author: juan
"""
import numpy as np


def genPsi(T,N,r,sigma,S0):
    t=np.linspace(0,T,N)
    dt=np.diff(t)
    xi=np.random.standard_normal(len(dt))
    W=np.append([0],np.cumsum(sigma*np.sqrt(dt)*xi))
    S=S0*np.exp((r-sigma**2/2)*t+W);
    return S