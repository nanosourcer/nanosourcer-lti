#!/usr/bin/env python

import os
import requests
import urllib
import re

# import httplib as http_client
# http_client.HTTPConnection.debuglevel = 1

FEDORA_ROOT = os.getenv('UTLS_FEDORA_ROOT')
FEDORA_USER = os.getenv('UTLS_FEDORA_USER')
FEDORA_PASSWORD = os.getenv('UTLS_FEDORA_PASSWORD')

pid = "islandora:7"

qstr = "objects/{0}/datastreams/JSON/content".format(pid)

url = "{0}/{1}".format(FEDORA_ROOT, qstr) 

params = {u'resultFormat': u'json'}

s = requests.Session()
s.auth = (FEDORA_USER, FEDORA_PASSWORD)

response = s.get(url, params=params)

result = response.json()

collectionName = result.get('collectionName', {})

collectionIndex = result.get('collectionMetadataIndex', {})

for item in collectionIndex:
    dcTerm = item.get('dcTerm', None)
    type = item.get('type', None)
    dcTermUri = item.get('dcTermUri', None)

    print("=" * 64)
    print('dcTerm      {0}'.format(dcTerm))
    print('type        {0}'.format(type))
    print('dcTermUri   {0}'.format(dcTermUri))

