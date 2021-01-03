import os
import random
import math
import numpy as np
import time

# init difficulty
initial_difficulty = 0.01

# node number
node_number = 4096
node_arr = [x for x in range(node_number)]

# first_round_d and second_round_d
first_round_d = initial_difficulty 
second_round_d = 0

# runner_up
runner_up_nodes_rate = 0.005
runner_up_number = int(node_number * runner_up_nodes_rate)
runner_up_difficulty_args = 0.8
runner_up_node_cap = []
runner_up_block_create_time = []
runner_up_real_node_index = []

# cycles
total_cycle = 10000
total_block_number = 0

# time
block_create_time = []
micro_block_create_time_tmp = []
main_block_create_time_tmp = {}

# time windows
difficulty_block_number = 0

# test file
f1 = open('/Users/liu/myexperiment/time.txt', 'w+')
f2 = open('/Users/liu/myexperiment/diff.txt', 'w+')

# node hash cap
node_hash_capability_queue = np.random.dirichlet(np.ones(node_number), size = node_number)

# expect time
expect_time = 3.7

# security args
difficulty_security_args = 1.0

if __name__ == '__main__':
    main_block_set = []
    micro_block_set = []

    loop = 1
    for j in range(total_cycle):
        if loop == 1:
            if j == 0:
                # first round difficulty
                first_round_d = initial_difficulty
            else:
                if difficulty_block_number == 200:
                    total_time = 0
                    for i in range(200):
                        total_time += block_create_time[total_block_number - i - 1]
                    difficulty_block_number = 0

                    rate = total_time / (expect_time * 200)
                    print(total_time)
                    if rate < 1:
                        first_round_d = first_round_d / rate
                    else:
                        first_round_d = first_round_d * rate
                    
                    f2.write('diff:')
                    f2.write(str(first_round_d))
                    f2.write('\n')

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
            block_create_time.append(main_block_create_time_tmp[key][index])

            # add this to queue
            main_block_set.append(index) 

            # record to file
            f1.write('round:')
            f1.write(str(j))
            f1.write('\t')
            f1.write("time:")
            f1.write(str(main_block_create_time_tmp[key][index]))
            f1.write('\n')

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
                    rate = round(1 - tmp, 18)
                else:
                    rate = round(runner_up_node_cap[i] / total_cap, 18)
                    tmp += rate
                runner_up_node_cap_new.append(rate)

            tmp = 0
            for i in range(runner_up_number):
                tmp += runner_up_node_cap_new[i]

            loop += 1
            difficulty_block_number += 1
            total_block_number += 1

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
            block_create_time.append(micro_block_create_time_tmp[index])
            micro_block_set.append(runner_up_real_node_index[index])

            # clear first round data
            runner_up_node_cap.clear()
            runner_up_node_index.clear()
            micro_block_create_time_tmp.clear()
            micro_block_set.clear()

            loop = 1
            difficulty_block_number += 1
            total_block_number += 1

            continue
    
    f1.close()
    f2.close()