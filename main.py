import os
import path
import math

initial_difficulty = 

node_number = 100
first_round_d = 
second_round_d = 
runner_up_list = []
total_cycle = 1000
node_hash_capability = []

def random_node_calculate_hash():
    for i in range(0, node_number - 1):
        tmp = random.randint(0, 1)
        while tmp in node_hash_capability:
            tmp = random.randint(0, 1)
        
        node_hash_capability.append(tmp)

        print(node_hash_capability)

if __init__ == '__main__':
    main_block_set = {}
    weak_block_set = {}

    random_node_calculate_hash()
    

    


    loop = 1
    for i in range(0, total_cycle - 1):
        if loop == 1:
            

        if loop == 2:
            

            loop = 1
            continue

        loop += 1
        