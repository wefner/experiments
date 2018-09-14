#!/usr/bin/env python3


import os
from time import time
from utils import load_csv, write_results, check_open_port

start = time()
top_sites = f'{os.path.dirname(os.path.realpath(__file__))}/top-1m.csv'
endpoints = load_csv(top_sites)[0:100]
results = {}

for endpoint in endpoints:
    endpoint, result = check_open_port(endpoint, timeout=1)
    results[endpoint] = result

write_results(results, 'synchronous')
end = time()
print(f"Endpoints took {end-start} seconds")
