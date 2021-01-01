import numpy as np

node_number = 100

node_hash_capability_queue = np.random.dirichlet(np.ones(node_number), size = 100)

tmp = 0
for x in range(node_number):
    tmp += node_hash_capability_queue[0][x]

res = tmp / 100

print(res)