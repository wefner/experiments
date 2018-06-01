#/usr/bin/env python3

import os
from multiprocessing import Pool
from utils import load_csv, write_results, check_open_port


results = []
n_processes = 100
top_sites = f'{os.path.dirname(os.path.realpath(__file__))}/top-1m.csv'
endpoints = load_csv(top_sites)[0:1000]
pool = Pool(processes=n_processes)
for endpoint in zip(*[iter(endpoints)] * n_processes):
    results.extend(pool.map(check_open_port, endpoint))
write_results(dict(results=results), 'multiprocessing')
pool.close()
