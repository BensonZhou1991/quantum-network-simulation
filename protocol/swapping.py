# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 22:26:08 2021

@author: zxz58
"""

def nested_power(num_ele_link):
    '''
    calculate # times that each elementary link is involved in a nested 
    swapping protocol
    '''
    power = [0] * num_ele_link
    # init current link
    current_link = []
    for i in range(num_ele_link):
        current_link.append([i])
    # try to get an end-to-end link via swapping
    #flag_forward = True
    pop_i = -1
    while len(current_link) > 1:
        #pop_i = 0 if flag_forward == True else -1
        #flag_forward = not flag_forward
        # gen new link via swapping
        next_link = []
        while len(current_link) > 1:
            new_link = current_link.pop(pop_i)
            new_link.extend(current_link.pop(pop_i))
            # update power number
            #print(new_link)
            for i in new_link:
                power[i] += 1
            next_link.append(new_link)
        if len(current_link) > 0: next_link.append(current_link.pop(pop_i))
        current_link = next_link
    return power

def hop_by_hop_power(num_ele_link):
    '''
    calculate # times that each elementary link is involved in a hop-by-hop 
    swapping protocol
    '''
    power = [0] * num_ele_link
    # init current link
    current_link = []
    for i in range(num_ele_link):
        current_link.append([i])
    next_link = current_link.pop(0)
    # try to get an end-to-end link via swapping
    while len(current_link) > 0:
        # gen new link via swapping
        next_link.extend(current_link.pop(0))
        # update power number
        for i in next_link:
            power[i] += 1
    return power

if __name__ == '__main__':
    #print(nested_power(10))
    print(hop_by_hop_power(9))