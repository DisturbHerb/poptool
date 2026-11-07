from datetime import datetime, timezone
from pathvalidate import sanitize_filename
from time import sleep

import csv
import datetime
import json 
import schedule
import urllib.request

SAMPLE_INTERVAL = 15 # In minutes.

REMOTE_URL = "https://node.goonhub.com/status?server="
SERVERS = ["main1", "main3", "main4"]
OUTPUT_PREFIX = "output"

def get_server_totals():
    total = 0

    for server in SERVERS:
        try:
            with urllib.request.urlopen((REMOTE_URL + server)) as url:
                data = json.loads(url.read())['response']
                total += int(data['players'])
        except:
            print(datetime.datetime.now(timezone.utc).isoformat() + ": Unable to get player count data for " + server)

    return total

def write_server_totals(target_file):
    now = datetime.datetime.now(timezone.utc)
    total = get_server_totals()

    with open(target_file, "a", newline='') as output_file:
        output_writer = csv.writer(output_file)
        output_writer.writerow([now.isoformat(), total])

    print(now.isoformat() + ": " + str(total) + " players online.")

def main():
    output_filename = sanitize_filename(OUTPUT_PREFIX + "-" + datetime.datetime.now(timezone.utc).isoformat() + ".csv")

    with open(output_filename, "w", newline='') as output_file:
        output_writer = csv.writer(output_file)
        output_writer.writerow(["timestamp", "total"])

    schedule.every(SAMPLE_INTERVAL).minutes.do(write_server_totals, target_file = output_filename)

    while True:
        schedule.run_pending()
        sleep(1)

main()