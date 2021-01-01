import os
import random
import math
import numpy as np
import time

# init difficulty
initial_difficulty = 0.01

# node number
node_number = 100
node_arr = [x for x in range(node_number)]

# first_round_d and second_round_d
first_round_d = initial_difficulty 
second_round_d = 0

# runner_up
runner_up_nodes_rate = 0.05
runner_up_number = int(node_number * runner_up_nodes_rate)
runner_up_difficulty_args = 0.8

runner_up_node_cap = []
runner_up_block_create_time = []
runner_up_real_node_index = []


total_cycle = 1000
main_block_difficulty_queue = []
micro_block_difficulty_queue = []

main_block_create_time = []
micro_block_create_time = []
micro_block_create_time_tmp = []
main_block_create_time_tmp = {}

node_hash_capability_queue = np.random.dirichlet(np.ones(node_number), size = 100)

if __name__ == '__main__':
    main_block_set = []
    micro_block_set = []

    # security args
    difficulty_security_args = 1.0
    # expect time
    expect_time = 1

    loop = 1
    for j in range(total_cycle):
        if loop == 1:
            if j == 0:
                # first round difficulty
                first_round_d = initial_difficulty
            else:
                # other round difficulty
                key = f'round_{tmp}'
                rate = main_block_create_time[j - 1] / expect_time
                print(main_block_create_time[j - 1])
                print(rate)
                
                # here is the problem, tomorrow to do 
                if rate < 1:
                    first_round_d = main_block_difficulty_queue[j - 1] / rate
                else:
                    first_round_d = main_block_difficulty_queue[j - 1] * rate

            print(first_round_d)
            time.sleep(5)
            print('--------')

            # set the default key name
            key = f'round_{j}'
            main_block_create_time_tmp.setdefault(key, [])
            
            # every node start to mine create time
            for i in range(node_number):
                first_time = node_hash_capability_queue[0][i] / first_round_d
                main_block_create_time_tmp[key].append(first_time)
            
            # choose a node to be the main member
            p = np.array(node_hash_capability_queue[0])
            index = np.random.choice(node_arr, p = p.ravel())
            
            # append the time to queue
            main_block_create_time.append(main_block_create_time_tmp[key][index])

            # append difficulty to queue
            main_block_difficulty_queue.append(first_round_d)

            # add this to queue
            main_block_set.append(index) 

            # choose runner up difficulty
            runner_up_difficulty = first_round_d * runner_up_difficulty_args

            # choose specific nodes
            p = np.array(node_hash_capability_queue[0])
            for i in range(runner_up_number):
                tmp = np.random.choice(node_arr, p = p.ravel())
                while tmp == index:
                    tmp = np.random.choice(node_arr, p = p.ravel())
                runner_up_real_node_index.append(tmp)
                runner_up_node_cap.append(node_hash_capability_queue[0][tmp])

            total_cap = 0
            for i in range(runner_up_number):
                total_cap += runner_up_node_cap[i]
            
            runner_up_node_cap_new = []
            tmp = 0
            for i in range(runner_up_number):
                if i == runner_up_number - 1:
                    rate = round(1 - tmp, 2)
                else:
                    rate = round(runner_up_node_cap[i] / total_cap, 2)
                    tmp += rate
                runner_up_node_cap_new.append(rate)
            
            tmp = 0
            for i in range(runner_up_number):
                tmp += runner_up_node_cap_new[i]

            loop += 1

        if loop == 2:
            second_hash_cap = 0
            for i in range(runner_up_number):
                second_hash_cap += runner_up_node_cap[i]
            
            second_round_d = second_hash_cap * second_hash_cap / 1

            # create time
            for i in range(runner_up_number):
                tmp_time = runner_up_node_cap[i] / second_round_d
                micro_block_create_time_tmp.append(tmp_time)
            
            runner_up_node_index = [x for x in range(runner_up_number)]
            p = np.array(runner_up_node_cap_new)
            index = np.random.choice(runner_up_node_index, p = p.ravel())
            micro_block_create_time.append(micro_block_create_time_tmp[index])
            micro_block_set.append(runner_up_real_node_index[index])

            # clear first round data
            runner_up_node_cap.clear()
            runner_up_node_index.clear()
            micro_block_create_time_tmp.clear()
            micro_block_set.clear()

            loop = 1
            continue
