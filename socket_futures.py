#!/usr/bin/env python3

import os
import concurrent.futures
from time import time
from utils import load_csv, get_url


def main(endpoints):
    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(get_url, endpoint): endpoint for endpoint in endpoints}
        for future in concurrent.futures.as_completed(futures):
            endpoint = futures[future]
            try:
                results.append(future.result())
            except Exception as exc:
                print('%r generated an exception: %s' % (endpoint, exc))
    return results


if __name__ == '__main__':
    top_sites = f'{os.path.dirname(os.path.realpath(__file__))}/top-1m.csv'
    endpoints = load_csv(top_sites)
    site_chunk = [10, 100, 500, 1000]
    for n in site_chunk:
        start = time()
        results = main(endpoints[0:n])
        end = time()
        print(f"{n} endpoints took {end-start:.2f} seconds")
