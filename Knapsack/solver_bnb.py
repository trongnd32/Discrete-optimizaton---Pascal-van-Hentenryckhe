#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
from recordclass import recordclass
from collections import deque
Item = namedtuple("Item", ['index', 'value', 'weight'])
Node = recordclass('Node', 'level value weight items')

items = []
item_count = 0
capacity = 0
sum_items_value = []
sum_items_weight = []

def read_input(input_data):
    global item_count
    global capacity
    global items
    global sum_items_value
    global sum_items_weight
    
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []
    
    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))
    
    items.sort(key=lambda item: item.value/item.weight, reverse=True)
    
    for i in range(item_count):
        if i > 0:
            sum_items_value.append(sum_items_value[i - 1] + items[i].value)
            sum_items_weight.append(sum_items_weight[i - 1] + items[i].weight)
        else:
            sum_items_value.append(items[0].value)
            sum_items_weight.append(items[0].weight)
    
    
    #for i in range(item_count):
    #    print(items[i].weight, end=" ")
    #print()
    #for i in range(item_count):
    #    print(items[i].value, end=" ")
    #print()
    #print(capacity)
    #print(' '.join(map(str, sum_items_value)))

###################################
    
def estimate(u):
    
    if(u.weight >= capacity):
        return 0
    
    es = u.value
    
    low = u.level
    high = item_count
    while high-low > 1:
        mid = int((low+high)/2)
        if mid >= item_count:
            break
        #print("debug: ",low, mid, high," | ", sum_items_weight[mid], sum_items_weight[u.level], sum_items_weight[mid] - sum_items_weight[u.level] + u.weight, capacity)
        if sum_items_weight[mid] - sum_items_weight[u.level] + u.weight <= capacity:
            low = mid
        else:
            high = mid
    
    tmp = 0
    
    
    if low + 1 < item_count:
        tmp = (capacity-(sum_items_weight[low] - sum_items_weight[u.level] + u.weight))/items[low+1].weight*items[low+1].value
    if low < item_count:
        es += sum_items_value[low]-sum_items_value[u.level] + tmp
        
        
    #print("es: ", low + 1, es)
    return es

####################################
    
def bound(u):
    if (u.weight >= capacity):
        return 0
    else:
        result = u.value
        j = u.level + 1
        totweight = u.weight
        
        while (j < item_count and totweight + items[j].weight <= capacity):
            totweight = totweight + items[j].weight
            result = result + items[j].value
            j = j + 1
            #print("debug2: ", j, items[j].weight, totweight)
        
        k = j
        if (k <= item_count - 1):
            result = result + (capacity - totweight)*items[k].value/items[k].weight
        
        #print("bo: ", k, result)
        
        return result


    
def solve_by_bb(input_data):  
    
    ep = 0.0001
    
    read_input(input_data)

    # items.sort(key=lambda item:item.value, reverse=True)
    
    x = []
    cur_max_val = 0
    
    v = Node(level=-1, value=0, weight=0,items=[])
    Q = deque([])
    Q.append(v)
    
    it=0
    
    while len(Q) != 0:
        v = Q[0]
        Q.popleft()
        
        if v.level == item_count - 1:
            continue
        
        u = Node(level = None, value = None, weight = None, items = [])
        
        u.level = v.level + 1
        u.value = v.value + items[u.level].value
        u.weight = v.weight + items[u.level].weight
        u.items = list(v.items)
        u.items.append(items[u.level].index)
        
        if u.weight <= capacity and u.value > cur_max_val:
            cur_max_val = u.value
            x = (u.items).copy()
        
        es = estimate(u)
        #es1 = bound(u)
        #if abs(es-es1) > ep:
         #   print(es,es1)
        
        if es > cur_max_val:
            Q.append(u)       
            
        u = Node(level = None, value = None, weight = None, items = [])
        u.level = v.level + 1
        u.value = v.value
        u.weight = v.weight
        u.items = list(v.items)
        
        if u.weight <= capacity and u.value > cur_max_val:
            cur_max_val = u.value
            x = (u.items).copy()
        
        es = estimate(u)
        #es1 = bound(u)
        #if abs(es-es1) > ep:
         #   print(es,es1)
        
        if es > cur_max_val:
            Q.append(u)
        
    taken = [0]*item_count
    for i in x:
        taken[i] = 1
    
    # print result
    #print("--- %s seconds by bb ---" % (time.time() - start_time))
    output_data = str(cur_max_val) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    
    return output_data

def solve_it(input_data):
    return solve_by_bb(input_data)


import time

if __name__ == '__main__':
    import sys
    start_time = time.time()
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')
    #print("--- %s seconds ---" % (time.time() - start_time))
