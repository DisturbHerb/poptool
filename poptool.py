from pathvalidate import sanitize_filename
from time import sleep

import csv
import datetime
import json 
import urllib.request

remote_url = "https://node.goonhub.com/status?server="
servers = ["main1", "main3", "main4"]
output_prefix = "output"

def get_server_totals():
    total = 0

    for server in servers:
        with urllib.request.urlopen((remote_url + server)) as url:
            data = json.loads(url.read())['response']
            total += int(data['players'])

    return total

def main():
    output_filename = sanitize_filename(output_prefix + "-" + str(datetime.datetime.now().isoformat()) + ".csv")

    with open(output_filename, "w", newline='') as output_file:
        output_writer = csv.writer(output_file)
        output_writer.writerow(["timestamp", "total"])

    with open(output_filename, "a", newline='') as output_file:
        output_writer = csv.writer(output_file)
        output_writer.writerow([datetime.datetime.now().isoformat(), get_server_totals()])

main()