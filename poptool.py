from pathvalidate import sanitize_filename
from time import sleep

import csv
import datetime
import json 
import schedule
import urllib.request

DAY_SECONDS = 86400
SAMPLE_INTERVAL = 15 # In minutes.

REMOTE_URL = "https://node.goonhub.com/status?server="
SERVERS = ["main1", "main3", "main4"]
OUTPUT_PREFIX = "output"

now_start = datetime.datetime.now(datetime.timezone.utc)

def get_server_totals():
    total = 0

    for server in SERVERS:
        with urllib.request.urlopen((REMOTE_URL + server)) as url:
            data = json.loads(url.read())['response']
            total += int(data['players'])

    return total

def write_server_totals(target_file):
    with open(target_file, "a", newline='') as output_file:
        output_writer = csv.writer(output_file)
        output_writer.writerow([now_start.isoformat(), get_server_totals()])

def main():
    output_filename = sanitize_filename(OUTPUT_PREFIX + "-" + now_start.isoformat() + ".csv")

    with open(output_filename, "w", newline='') as output_file:
        output_writer = csv.writer(output_file)
        output_writer.writerow(["timestamp", "total"])

    start_time = ((int(now_start.timestamp()) // DAY_SECONDS) + 1) * DAY_SECONDS
    start_timestamp = datetime.datetime.fromtimestamp(start_time, datetime.timezone.utc)

    stop_time = start_time + DAY_SECONDS
    stop_timestamp = datetime.datetime.fromtimestamp(stop_time, datetime.timezone.utc)

    print("Start time set to " + start_timestamp.isoformat() + ". Current time is " + now_start.isoformat() + ". Stoppping at " + stop_timestamp.isoformat() + ".")

    while True:
        if datetime.datetime.now(datetime.timezone.utc) >= start_timestamp:
            while True:
                schedule.every(SAMPLE_INTERVAL).minutes.do(write_server_totals(output_filename))
                if datetime.datetime.now(datetime.timezone.utc) >= stop_timestamp:
                    break
            break
        else:
            sleep(100)

    print("Execution finished, verify output at " + output_filename)

main()