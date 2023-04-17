#!/usr/bin/env python3


import asyncio
import os
import aiohttp
from time import time
from utils import load_csv


async def get_url(session, domain_name):
    results = {}
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "}
    try:
        async with session.get(f"https://www.{domain_name}", allow_redirects=False, headers=headers) as response:
            await response.read()
            results[domain_name] = response.status
    except asyncio.exceptions.TimeoutError:
        results[domain_name] = "timeout"
    except aiohttp.ClientError:
        results[domain_name] = "clienterror"
    return results


async def main(endpoints):
    timeout_seconds = 3
    timeout = aiohttp.ClientTimeout(total=None, sock_connect=timeout_seconds, sock_read=timeout_seconds)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        results = await asyncio.gather(*[get_url(session, endpoint) for endpoint in endpoints])
    return results


if __name__ == '__main__':
    site_chunk = [10, 100, 500, 1000]

    top_sites = f'{os.path.dirname(os.path.realpath(__file__))}/top-1m.csv'
    endpoints = load_csv(top_sites)
    for n in site_chunk:
        start = time()
        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(main(endpoints[0:n]))
        end = time()
        print(f"{n} endpoints took {end-start:.2f} seconds")
