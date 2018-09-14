#!/usr/bin/env python3

import os
from multiprocessing import Pool
from time import time
from utils import load_csv, write_results, check_open_port

start = time()
results = {}
endpoint_processes = []
n_processes = 10
top_sites = f'{os.path.dirname(os.path.realpath(__file__))}/top-1m.csv'
endpoints = load_csv(top_sites)[0:100]

pool = Pool(processes=n_processes)
# We chunk our list of endpoints by the number of processes we spawn
for endpoint in zip(*[iter(endpoints)] * n_processes):
    endpoint_processes.extend(pool.map(check_open_port, endpoint))
    for process in endpoint_processes:
        results[process[0]] = process[1]


write_results(results, 'multiprocessing')
pool.close()
end = time()
print(f"Endpoints took {end-start} seconds")
