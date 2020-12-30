import os
import random
import math

initial_difficulty = 1000

node_number = 100
first_round_d = initial_difficulty 
second_round_d = initial_difficulty / 10
runner_up_list = []
total_cycle = 1000
node_hash_capability_queue = []
node_hash_tmp = []
history_first_round_difficulty = []
history_second_round_difficulty = []

def random_node_calculate_hash():
    for i in range(0, node_number):
        tmp = random.random()
        while tmp in node_hash_tmp:
            tmp = random.randint(0, 1)
        
        node_hash_tmp.append(tmp)
    
    node_hash_tmp.sort()
    
    for i in range(0, node_number):
        if i == 0:
            node_hash_capability_queue.append(node_hash_tmp[i])
            continue

        if i == node_number - 1:
            node_hash_capability_queue.append(1 - node_hash_tmp[i])
            break

        tmp = abs(node_hash_tmp[i] - node_hash_tmp[i - 1])
        node_hash_capability_queue.append(tmp)

    node_hash_capability_queue.sort()
    node_hash_capability_queue.reverse()

    #print(node_hash_capability_queue)

if __name__ == '__main__':
    main_block_set = {}
    weak_block_set = {}

    random_node_calculate_hash()
    history_second_round_difficulty(100.0)
    history_first_round_difficulty.append(100.0)
    
    # security args
    

    loop = 1
    for i in range(0, total_cycle - 1):
        if loop == 1:
            if i == 0:
                first_round_d = initial_difficulty
            else:
                first_round_d = history_first_round_difficulty[i-1] * 
            
            # random choose node to be the first major
            first_round_successor = random.randint(0, 20)
            first_block_time = random.random()
            first_block_time = first_block_time * 

            continue
        if loop == 2:
            if i == 0:
                second_round_d = initial_difficulty
            else:
                second_round_d = history_second_round_difficulty * 
            
            # random to be the 

            loop = 1
            continue

        loop += 1
    