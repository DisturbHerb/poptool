import json 
import urllib.request

remote_url = "https://node.goonhub.com/status?server="
servers = ["main1", "main3", "main4"]

total = 0

for server in servers:
    with urllib.request.urlopen((remote_url + server)) as url:
        data = json.loads(url.read())['response']
        total += int(data['players'])

print(total)