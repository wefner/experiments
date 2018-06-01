#/usr/bin/env python3


import os
from utils import load_csv, write_results, check_open_port


top_sites = f'{os.path.dirname(os.path.realpath(__file__))}/top-1m.csv'
endpoints = load_csv(top_sites)[0:1000]
results = {'results': {}}
for endpoint in endpoints:
    endpoint, result = check_open_port(endpoint)
    results['results'][endpoint] = result
write_results(results, 'synchronous')
