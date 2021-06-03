# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 13:19:31 2021

@author: zxz58
"""
from link import Link

class Node():
    def __init__(self, rate, pos):
        '''
        initialize

        Parameters
        ----------
        rate : # entanglement pairs created per unit time
        pos : (x_coordinate, y_coordinate)

        Returns
        -------
        None.

        '''
        # init parameters
        self.pos = pos
        self.rate = rate
        self.rate_left = rate # rate left after being allocated for links
        # served links and rate of entanglement pairs for each link
        self.served_links = []
        self.served_rate = []
        # info for communication
        self.target_node = None
        # target fidelity for transmitting info to the target node
        self.target_f = None
    
    def add_to_link(self, link, rate=None):
        '''
        add node to a Link class

        Returns
        -------
        None.

        '''
        self.served_links.append(link)
        self.served_rate.append(rate)
        if rate != None: self.rate_left -= rate
        
    def set_target(self, target_node, target_f):
        self.target_node, self.target_f = target_node, target_f
        
    def add_rate(self, arg, rate):
        if isinstance(arg, Link):
            link = arg
            i = self.served_links.index(link)
        else:
            i = arg
            link = self.served_links[i]
        if self.served_rate[i] != None: raise()
        self.served_rate[i] = rate
        self.rate_left -= rate
        if self.rate_left < 0: raise()
        
    def init_links(self):
        self.rate_left = self.rate # rate left after being allocated for links
        # served links and rate of entanglement pairs for each link
        self.served_links = []
        self.served_rate = []