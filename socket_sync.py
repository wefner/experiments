#!/usr/bin/env python3

import os
from time import time
from utils import load_csv, get_url

site_chunk = [10, 100, 500, 1000]
top_sites = f'{os.path.dirname(os.path.realpath(__file__))}/top-1m.csv'
endpoints = load_csv(top_sites)

for n in site_chunk:
    start = time()
    results = [get_url(endpoint) for endpoint in endpoints[0:n]]
    end = time()
    # print(results)
    print(f"{n} endpoints took {end-start:.2f} seconds")
