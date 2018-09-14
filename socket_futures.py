#!/usr/bin/env python3


import os
import concurrent.futures
from time import time
from utils import load_csv, write_results, check_open_port


# https://docs.python.org/3/library/concurrent.futures.html#threadpoolexecutor-example

start = time()
results = {}
top_sites = f'{os.path.dirname(os.path.realpath(__file__))}/top-1m.csv'
endpoints = load_csv(top_sites)[0:100]
max_workers = 10

# We can use a with statement to ensure threads are cleaned up promptly
with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
    # Start the load operations and mark each future with its endpoint
    futures = {executor.submit(check_open_port, endpoint): endpoint for endpoint in endpoints}
    for future in concurrent.futures.as_completed(futures):
        endpoint = futures[future]
        try:
            data = future.result()
            results[data[0]] = data[1]
        except Exception as exc:
            print('%r generated an exception: %s' % (endpoint, exc))

write_results(results, 'futures')
end = time()
print(f"Endpoints took {end-start} seconds")
