# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 15:50:19 2021

@author: zxz58
"""
from distributed_network import b
import numpy as np
from node import Node
from link import Link
import matplotlib
import matplotlib.pyplot as plt
#matplotlib.use('WebAgg')

class Network():
    def __init__(self, decay, length):
        self.nodes = []
        self.decay = decay
        self.length = length
        self.links = []
        
    def add_node(self, rate, pos):
        self.nodes.append(Node(rate, pos))
        
    def init_nodes(self, method, para):
        if method == 'uniform': self.init_nodes_uniform(para[0], para[1])
    
    def init_nodes_uniform(self, num_nodes, rate):
        '''create num_nodes nodes randomly with fixed rate'''
        for _ in range(num_nodes):
            self.add_node(rate, self.length*np.random.rand(2)/1.0000000001)
    
    def init_commnuication_process(self, method, para):
        '''find target nodes and set fidelity'''
        if method == 'uniform':
            self.init_commnuication_process_uniform(para[0])
    
    def init_commnuication_process_uniform(self, target_f):
        '''set target nodes uniformly and randomly'''
        num_nodes = len(self.nodes)
        target_list = list(range(num_nodes))
        np.random.shuffle(target_list)
        for i in range(num_nodes):
            source_node = self.nodes[i]
            target_node_index = target_list[0]
            # check target == current node?
            if target_node_index == i: target_node_index = target_list[1]
            target_list.remove(target_node_index)
            target_node = self.nodes[target_node_index]
            if source_node == target_node: raise()
            source_node.set_target(target_node, target_f)
            
    def init_links(self):
        self.links = []
        for node in self.nodes: node.init_links()
            
    def route(self, method, para):
        if method == 'straight': self.route_straight(para[0])
        if method == 'right_angle': self.route_corner(para[0])
    
    def route_straight(self, k):
        '''straight line routing and resource allocation with k dividing'''
        # classify nodes according to k*k subsquares
        ## init nodes classification dictionary
        node_classify = {}
        for i in range(k):
            node_classify[i] = {}
            for j in range(k):
                node_classify[i][j] = []
        ## classify each node
        l = self.length / k # lenght of each subsquare
        ### function from node coordinates to subsquare position
        index_convert = lambda node_pos: (int(np.floor(node_pos[0]/l)),
                                          int(np.floor(node_pos[1]/l)))
        for node in self.nodes:
            indices = index_convert(node.pos)
            node_classify[indices[0]][indices[1]].append(node)
        # find route for each node
        for sour in self.nodes:
            link = Link(target_f=sour.target_f)
            self.links.append(link)
            dest = sour.target_node
            link.add_node(sour) # add source node to link
            i_sour = index_convert(sour.pos)
            i_dest = index_convert(dest.pos)
            i_current = list(i_sour)
            # routing subsquare by subsquare
            while True:
                delta = np.array([i_dest[0] - i_current[0],
                                  i_dest[1] - i_current[1]])
                if np.sum(np.abs(delta)) <= 1:
                    break
                # go to next subsquare
                if np.abs(delta[0]) >= np.abs(delta[1]):
                  i_current[0] = int(i_current[0] + delta[0]/np.abs(delta[0]))
                else:
                  i_current[1] = int(i_current[1] + delta[1]/np.abs(delta[1]))
                # find a node in the next square and add it to the link
                best_value = -1
                for node in node_classify[i_current[0]][i_current[1]]:
                    current_value = len(node.served_links)
                    if current_value < best_value or best_value == -1:
                        best_value = current_value
                        best_node = node
                if best_value == -1: raise()
                link.add_node(best_node)
            link.add_node(dest) # add destination node to link
            
    def route_corner(self, k):
        '''right angle routing and resource allocation with k dividing'''
        # classify nodes according to k*k subsquares
        ## init nodes classification dictionary
        node_classify = {}
        for i in range(k):
            node_classify[i] = {}
            for j in range(k):
                node_classify[i][j] = []
        ## classify each node
        l = self.length / k # lenght of each subsquare
        ### function from node coordinates to subsquare position
        index_convert = lambda node_pos: (int(np.floor(node_pos[0]/l)),
                                          int(np.floor(node_pos[1]/l)))
        for node in self.nodes:
            indices = index_convert(node.pos)
            node_classify[indices[0]][indices[1]].append(node)
        # find route for each node
        flag_x_first = True
        for sour in self.nodes:
            flag_x_first = not flag_x_first
            link = Link(target_f=sour.target_f)
            self.links.append(link)
            dest = sour.target_node
            link.add_node(sour) # add source node to link
            i_sour = index_convert(sour.pos)
            i_dest = index_convert(dest.pos)
            i_current = list(i_sour)
            # routing subsquare by subsquare
            while True:
                delta = np.array([i_dest[0] - i_current[0],
                                  i_dest[1] - i_current[1]])
                if np.sum(np.abs(delta)) <= 1:
                    break
                # go to next subsquare
                if flag_x_first:
                    if np.abs(delta[0]) > 0:
                        i_current[0] = int(i_current[0] + delta[0]/np.abs(delta[0]))
                    else:
                        i_current[1] = int(i_current[1] + delta[1]/np.abs(delta[1]))
                else:
                    if np.abs(delta[1]) > 0:
                        i_current[1] = int(i_current[1] + delta[1]/np.abs(delta[1]))
                    else:
                        i_current[0] = int(i_current[0] + delta[0]/np.abs(delta[0]))
                # find a node in the next square and add it to the link
                best_value = -1
                for node in node_classify[i_current[0]][i_current[1]]:
                    current_value = len(node.served_links)
                    if current_value < best_value or best_value == -1:
                        best_value = current_value
                        best_node = node
                if best_value == -1: raise()
                link.add_node(best_node)
            link.add_node(dest) # add destination node to link
            
    def reset_fidelity(self, fidelity):
        num_link = len(self.links)
        if isinstance(fidelity, float): fidelity = [fidelity] * num_link
        for i in range(num_link):
            link = self.links[i]
            f = fidelity[i]
            link.target_f = f
        
    def nodes_dist(self, node1, node2):
        '''calculate distance between two input nodes'''
        return np.sqrt(np.sum((node1.pos - node2.pos) ** 2))
    
    def resource_allo(self, method, para):
        if method == 'equal': self.resource_allo_equal()
        if method == 'weight': self.resource_allo_weight()
    
    def resource_allo_equal(self):
        for link in self.links:
            i = -1
            for node in link.nodes:
                i += 1
                if i == 0:
                    # source node doesn't contribute resources
                    rate = 0
                else:
                    rate = int(node.rate / (len(node.served_links) - 1))
                link.add_rate(i, rate)
                
    def resource_allo_weight(self):
        a = 1
        for node in self.nodes:
            num_link = len(node.served_links)
            # get length for each link
            link_len = np.empty(num_link)
            for i in range(num_link):
                if node == node.served_links[i].nodes[0]:
                    # source node doesn't contribute resources
                    link_len[i] = 0
                else:
                    link_len[i] = len(node.served_links[i].nodes) - 1
            # get weight for each link
            link_w = np.power(link_len, a)
            link_w = link_w / np.sum(link_w)
            # allocate resources according to weights
            link_resc = np.floor(node.rate * link_w)
            for i in range(num_link):
                link = node.served_links[i]
                rate = link_resc[i]
                link.add_rate(node, rate)
                
    def link_rate(self, method, para):
        from protocol.communication import get_prob_elem, get_rate
        prob_swap = para[0]
        if method == 'nested':
            from protocol.swapping import nested_power
            get_power = nested_power
        if method == 'hop_by_hop':
            from protocol.swapping import hop_by_hop_power
            get_power = hop_by_hop_power
        num_link = len(self.links)
        link_rates = np.empty(num_link)
        for index in range(num_link):
            link = self.links[index]
            num_elem = len(link.nodes) - 1 # number of elementary links
            # get rescoures allocated for each elementary link
            if link.rates[0] == 0:
                rates_resc = np.array(link.rates[1:])
            else:
                if link.rates[-1] == 0:
                    rates_resc = np.array(link.rates[:-1])
                else:
                    raise()
            # get links distances
            dist = np.empty(num_elem)
            for i in range(num_elem):
                dist[i] = self.nodes_dist(link.nodes[i], link.nodes[i+1])
            if np.min(dist) == 0:
                print('link index is', index)
                print(link.nodes)
                raise() 
            # get rates for elementary links
            prob_elem = get_prob_elem(dist, link.target_f, self.decay)
            rates_elem = rates_resc * prob_elem
            # get power of each elementary via swapping protocol
            powers = get_power(num_elem)
            # calculate rate of the link
            rate_link = get_rate(rates_elem, powers, prob_swap)
            link.rate = rate_link
            link_rates[index] = rate_link
        return link_rates
    
    def draw_node_distribution(self):
        # get coordinates info
        num_node = len(self.nodes)
        x, y = np.empty(num_node), np.empty(num_node)
        i = -1
        for node in self.nodes:
            i += 1
            x[i], y[i] = node.pos[0], node.pos[1]
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.scatter(x, y)
        return fig, ax
    
    def draw_subarea_links(self, k, ax=None):
        '''draw graph on served links in each subsquare'''
        from matplotlib import cm
        subarea_links = np.zeros((k, k))
        # classify nodes according to k*k subsquares
        ## classify each node
        l = self.length / k # lenght of each subsquare
        ### function from node coordinates to subsquare position
        index_convert = lambda node_pos: (int(np.floor(node_pos[0]/l)),
                                          int(np.floor(node_pos[1]/l)))
        for node in self.nodes:
            indices = index_convert(node.pos)
            num_links = len(node.served_links)
            subarea_links[indices[0]][indices[1]] += num_links
        # draw
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1, projection='3d')
        # plot a 3D surface like in the example mplot3d/surface3d_demo
        X = np.arange(0, k, 1)
        Y = np.arange(0, k, 1)
        X, Y = np.meshgrid(X, Y)
        Z = subarea_links
        surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
                               linewidth=0, antialiased=False)
        #ax.set_zlim(-1.01, 1.01)
        fig.colorbar(surf, shrink=0.5, aspect=10)
        return fig
    
    def draw_route(self, link_index, colour='g'):
        fig, ax = self.draw_node_distribution()
        if isinstance(link_index, int): link_index = [link_index]
        for link_i in link_index:
            link = self.links[link_i]
            num_node = len(link.nodes)
            for i in range(num_node):
                if i == 0 or i == num_node - 1:
                    # draw source and destination nodes
                    x, y = link.nodes[i].pos
                    ax.scatter(x, y, c='r', s=100)
                    if i == num_node - 1: continue
                # draw a line
                pos1, pos2 = link.nodes[i].pos, link.nodes[i+1].pos
                x, y = (pos1[0], pos2[0]), (pos1[1], pos2[1])
                ax.plot(x, y, c=colour, lw='3')
        return fig, ax
    
    def draw_rates_histogram(self, rates):
        plt.hist(rates)
        
    def alert_link_rate(self, rate_threshold, link_rates):
        link_i = []
        for i in range(len(link_rates)):
            if link_rates[i] < rate_threshold: link_i.append(i)
        #print(link_i)
        # draw
        self.draw_route(link_i, 'r')
        
if __name__ == '__main__':
    decay = 0.01 #0.01
    num_node = 10000 #10000
    node_frequency = 10000
    area_length = 100
    prob_swap = 0.9
    target_fidelity = 0.7
    k = 10 #10
    #methods_route = ['straight', 'right_angle']
    methods_route = ['straight']
    #methods_swap = ['nested', 'hop_by_hop']
    methods_swap = ['nested']
    #'equal', 'weight'
    method_allo = 'equal'
    
    res_rate_ave = []
    import time
    for num_node in np.arange(1000,100000,2000):
        t = time.time()
        network = Network(decay=decay, length=area_length)
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
                #subarea_links.append(network.draw_subarea_links(k))
                #network.draw_route(1)
                #network.draw_rates_histogram(link_rates)
                #network.alert_link_rate(180, link_rates)
            network.init_links()
 


        