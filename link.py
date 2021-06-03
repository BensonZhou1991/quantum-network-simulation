# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 16:23:48 2021

@author: zxz58
"""

class Link():
    def __init__(self, target_f, rate=None):
        self.nodes = []
        self.rate = rate # communication rate
        self.target_f = target_f
        self.rates = [] # 
        
    def add_node(self, node, node_rate=None):
        # update nodes info
        node.add_to_link(self, node_rate)
        self.nodes.append(node)
        self.rates.append(node_rate)
        
    def add_rate(self, arg, rate):
        from node import Node
        if rate < 0: raise()
        if isinstance(arg, Node):
            node = arg
            i = self.nodes.index(node)
        else:
            i = arg
            node = self.nodes[i]
        if self.rates[i] != None: raise()
        self.rates[i] = rate