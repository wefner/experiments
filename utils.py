#!/usr/bin/env python3

import csv
import os
import requests
import zipfile


def download_sites(sites):
    with open(sites, 'wb') as f:
        url = "http://s3.amazonaws.com/alexa-static/top-1m.csv.zip"
        response = requests.get(url, stream=True)
        f.writelines(response.iter_content(1024))
    return


def unzip_sites():
    sites = 'top-1m.csv'
    download_sites(f"{sites}.zip")
    with zipfile.ZipFile(f"{sites}.zip", 'r') as zf:
        zf.extractall('.')
    return


def load_csv(filename):
    all_sites = []
    if not os.path.exists(filename):
        print("Downloading site file")
        unzip_sites()
    with open(filename, newline='') as csvfile:
        sites = csv.reader(csvfile, delimiter=',', quotechar='|')
        for site in sites:
            try:
                all_sites.append(site[1])
            except IndexError:
                pass
    return all_sites


def get_url(domain_name):
    results = {}
    try:
        response = requests.get(f"https://www.{domain_name}", timeout=3, allow_redirects=False)
        result = response.status_code
    except requests.exceptions.ReadTimeout:
        result = "timeout"
    except requests.exceptions.ConnectionError:
        result = "connection error"
    except Exception as e:
        result = str(e)
    results[domain_name] = result
    return results
