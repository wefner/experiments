#!/usr/bin/env python3


import csv
import json
import os
import socket


def load_csv(filename):
    with open(filename, newline='') as csvfile:
        sites = csv.reader(csvfile, delimiter=',', quotechar='|')
        all_sites = [site[1] for site in sites]
    return all_sites


def write_results(results, output_file):
    out = f'{os.path.dirname(os.path.realpath(__file__))}/{output_file}.json'
    with open(out, 'w') as outfile:
        json.dump(results, outfile, indent=4)


def check_open_port(endpoint, port=443, timeout=1):
    result = 'Open'
    try:
        print(f"Opening socket to {endpoint}")
        socket.create_connection((endpoint, port), timeout=timeout)
    except socket.timeout:
        result = 'Timeout'
    except ConnectionRefusedError:
        result = 'Refused'
    except socket.gaierror:
        result = 'nodename not known'
    except Exception as ex:
        print(ex)
        result = 'some other error'
    print(f"Done socket on {endpoint} with result {result}")
    return endpoint, result
