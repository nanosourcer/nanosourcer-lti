#!/usr/bin/env python

import os
import requests
import urllib

# import httplib as http_client
# http_client.HTTPConnection.debuglevel = 1

FEDORA_ROOT = os.getenv('UTLS_FEDORA_ROOT')
FEDORA_USER = os.getenv('UTLS_FEDORA_USER')
FEDORA_PASSWORD = os.getenv('UTLS_FEDORA_PASSWORD')

inline = """{

	"title" : "tester01",
	"metadata" : [

		{

			"dcTerm" : "title",
			"uri" : "BIC.Box_1.EN[Photographs].20151007.PH.0243.F"

		},
		{

			"dcTerm" : "creator",
			"label" : "Rio Mursinna, initials ARM (scanner); Jamie Aprile (supervisor)",
			"uri" : "null"

		},
		{

			"dcTerm" : "creator",
			"label" : "William J. Battle",
			"uri" : "http://vocab.getty.edu/ulan/500011739"

		},
		{

			"dcTerm" : "date",
			"label" : "Date Created",
			"uri" : "09/03/2015"

		},
		{

			"dcTerm" : "date",
			"label" : "Start Date",
			"uri" : "550 BC"

		},
		{

			"dcTerm" : "date",
			"label" : "End Date",
			"uri" : "500 BC"

		},
		{

			"dcTerm" : "temporal",
			"label" : "Classical",
			"uri" : "http://n2t.net/ark:/99152/p0qhb66wcdj"

		},
		{

			"dcTerm" : "spatial",
			"label" : "Baalbek",
			"uri" : "http://pleiades.stoa.org/places/678179"

		},
		{

			"dcTerm" : "rights",
			"label" : "Creative Commons",
			"uri" : "null"

		},
		{

			"dcTerm" : "subject",
			"label" : "Temple",
			"uri" : "http://vocab.getty.edu/aat/300007595"

		}

	]


}
"""

pid = "islandora:95"

url = "http://islandora716.ctl.utexas.edu:8080/fedora/objects/{0}/datastreams/JSONTEST".format(pid)

print(url)

post_data = {}

post_data['data'] = inline

params = {'mimeType': 'application/json',
          'dsLabel': 'JSON datastream',
          'controlGroup': 'M'}

headers = {'Content-Type': 'application/json',
           'Content-Length': len(inline)}

s = requests.Session()
s.auth = (FEDORA_USER, FEDORA_PASSWORD)

response = s.post(url, params=params, headers=headers, **post_data)

print(response.content)

