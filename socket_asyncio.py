#!/usr/bin/env python3

# https://docs.python.org/3/library/asyncio-task.html#example-parallel-execution-of-tasks


import asyncio
import os
import socket
from time import time
from utils import load_csv, write_results


async def check_open_port(endpoint, port=443):
    result = 'Open'
    try:
        print(f"Opening socket to {endpoint}")
        await asyncio.wait_for(asyncio.open_connection(endpoint,
                                                       port,
                                                       ssl=False),
                               timeout=5,
                               loop=loop)
    except asyncio.TimeoutError:
        result = 'Timeout'
    except ConnectionRefusedError:
        result = 'Refused'
    except socket.gaierror:
        result = 'nodename not known'
    except Exception:
        result = 'some other error'
    print(f"Done socket on {endpoint} with result {result}")
    return endpoint, result


async def main(endpoints):
    results = {}
    coroutines = [asyncio.create_task(check_open_port(endpoint)) for endpoint in endpoints]
    completed, pending = await asyncio.wait(coroutines)
    for c in completed:
        results[c.result()[0]] = c.result()[1]
    write_results(results, 'asyncio')


if __name__ == '__main__':
    start = time()
    top_sites = f'{os.path.dirname(os.path.realpath(__file__))}/top-1m.csv'
    endpoints = load_csv(top_sites)[0:100]
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(asyncio.gather(main(endpoints)))
        loop._default_executor.shutdown(wait=True)
    finally:
        loop.close()
    end = time()
    print(f"Endpoints took {end-start} seconds")
