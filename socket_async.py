#/usr/bin/env python3


# https://docs.python.org/3/library/asyncio-task.html#example-parallel-execution-of-tasks


import asyncio
import os
import socket
from utils import load_csv, write_results


async def check_open_port(endpoint, port, timeout=1):
    result = 'Open'
    try:
        socket.create_connection((endpoint, port), timeout=timeout)
    except socket.timeout:
        result = 'Timeout'
        await asyncio.sleep(0.001)
    except ConnectionRefusedError:
        result = 'Refused'
    except socket.gaierror:
        result = 'nodename not known'
    if not result == 'Open':
        await asyncio.sleep(0.001)
    return endpoint, result


async def main(endpoints):
    results = {'results': {}}

    coroutines = [check_open_port(endpoint, 443) for endpoint in endpoints]
    completed, pending = await asyncio.wait(coroutines)

    for c in completed:
        results['results'][c.result()[0]] = c.result()[1]
    write_results(results, 'asyncio')

    return completed, pending


if __name__ == '__main__':
    top_sites = f'{os.path.dirname(os.path.realpath(__file__))}/top-1m.csv'
    endpoints = load_csv(top_sites)[0:1000]
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(asyncio.gather(main(endpoints)))
    finally:
        loop.close()
