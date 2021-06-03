# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 22:38:13 2021

@author: zxz58
"""
from distributed_network import b
import numpy as np
from node import Node
from link import Link
from network import Network
import matplotlib
import matplotlib.pyplot as plt

decay = 0.01 #0.01
num_node = 10000 #10000
node_frequency = 10000
area_length = 100
prob_swap = 0.9
target_fidelity = 0.7
k = 10 #10
# choose routing strategy
#methods_route = ['straight', 'right_angle']
methods_route = ['straight']
# choose entalglement swapping strategy
#methods_swap = ['nested', 'hop_by_hop']
methods_swap = ['nested']
# choose entalglement resources allocation strategy
#'equal', 'weight'
method_allo = 'equal'

res_rate_ave = []
import time
for num_node in np.arange(1000,100000,2000):
    t = time.time()
    network = Network(decay=decay, length=area_length)
    # initialize nodes in network
    network.init_nodes('uniform', [num_node, node_frequency])
    #fig_node, _ = network.draw_node_distribution()
    network.init_commnuication_process('uniform', [target_fidelity])
    subarea_links = []
    for method_route in methods_route:
        network.route(method_route, [k])
        network.resource_allo(method_allo, None)
        for method_swap in methods_swap:
            link_rates = network.link_rate(method_swap, [prob_swap])
            print(method_route, method_swap, 
                  np.average(link_rates), np.var(link_rates))
            res_rate_ave.append(time.time() - t)
            # draw
            #subarea_links.append(network.draw_subarea_links(k))
            #network.draw_route(1)
            #network.draw_rates_histogram(link_rates)
            #network.alert_link_rate(180, link_rates)
        network.init_links()