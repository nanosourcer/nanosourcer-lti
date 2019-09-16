#!/usr/bin/env python

import os
import requests
import urllib
import re
from time import sleep

# import httplib as http_client
# http_client.HTTPConnection.debuglevel = 1

FEDORA_ROOT = os.getenv('UTLS_FEDORA_ROOT')
FEDORA_USER = os.getenv('UTLS_FEDORA_USER')
FEDORA_PASSWORD = os.getenv('UTLS_FEDORA_PASSWORD')

s = requests.Session()
s.auth = (FEDORA_USER, FEDORA_PASSWORD)

collection_pid = "islandora:7"
collection_pid = "islandora:battleimagecollection"

sparql = "select ?s from <#ri> where { ?s<info:fedora/fedora-system:def/relations-external#isMemberOfCollection> <info:fedora/" + collection_pid + "> }"

post_data = {'query': sparql,
             'type': 'tuples',
             'lang': 'sparql',
             'format': 'json',
             'limit': '2000',
             'dt': 'on'
            }

url = "http://islandora716.ctl.utexas.edu:8080/fedora/risearch"

print('checkpoint 01')

response = s.post(url, data=post_data)

item_list = response.json().get('results', [])

pid_list = []

for item in item_list:
    
    val = item.get('s', None)
    if not val or 'info:fedora/' not in val:
        continue
    val = re.sub('info:fedora/', '', val) 
    pid_list.append(val)

params = {u'resultFormat': u'xml'}

label_hash = {}

p = re.compile(r'^.*<label>(.*)</label>.*$')

print("Image PIDs found:")
for pid in pid_list:
    print(pid)

fedlist = [
"islandora:1879",
]


params = {}
    
for pid in fedlist:
    url = "{0}/objects/{1}/datastreams/JSON/content".format(FEDORA_ROOT, pid)
    print(url)
    response = s.get(url)
    chunk = response.json()
    image_title = chunk.get('title', '')
    label_hash[pid] = image_title

for k, v in label_hash.items():
    print(k, v)

for k, v in label_hash.items():
    print("UPDATE ns_image SET title = '{0}' WHERE image_pid = '{1}';".format(v, k))

# for pid in pid_list:
#     retries = 10
#     url = "http://islandora716.ctl.utexas.edu:8080/fedora/objects?pid=true&label=true&query=pid={0}".format(pid)
#     while retries > 0:
#         print('checkpoint 02 {0}'.format(url))
#         try:
#             response = s.get(url, params=params)
#             retries = 0
#         except requests.exceptions.ConnectionError:
#             retries -= 1
#             sleep(3)
# 
#     if not retries:
#         continue
#         
#     xml_chunk = response.content
#     xml_chunk = xml_chunk.replace('\n', '')
#     m = p.match(xml_chunk)
#     if m:
#         label = m.group(1)
#     label_hash[pid] = label
# 
# for k, v in label_hash.items():
#     print(k, v)
# 
