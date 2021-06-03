# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 00:37:32 2021

@author: zxz58
"""
import numpy as np

def get_prob_elem(dist, target_f, decay):
    '''
    Calculate the success probability for generating an elementary link

    Parameters
    ----------
    dist : np.array
        Distances of links
    target_f : float
        target fidelity
    decay: float
        decay factor
    Returns
    -------
    np.array

    '''
    pro_succ = np.exp(-1 * decay * dist)
    pro_succ = 2 * pro_succ / (1 - pro_succ)
    pro_succ = 0.5 * (1 - np.power((2 * target_f - 1), pro_succ))
    return pro_succ

def get_rate(rates_elem, powers, pro_succ):
    '''
    Get the maximum rate for the end-to-end link

    Parameters
    ----------
    rates_elem : TYPE
        generation rate for each elementary link
    powers : TYPE
        DESCRIPTION.
    pro_succ : TYPE
        success probability for each swapping operation

    Returns
    -------
    maximum generation rate for the end-to-end link

    '''
    if len(rates_elem) != len(powers): raise()
    num_link = len(rates_elem)
    rates = np.zeros(num_link)
    for i in range(num_link):
        rates[i] = rates_elem[i] * np.power(pro_succ, powers[i])
    return np.min(rates)