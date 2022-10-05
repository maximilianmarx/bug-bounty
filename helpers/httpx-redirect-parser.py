#!/usr/bin/env python3

# Removes out-of-scope URLs based on redirects from httpx' output
# A bad redirect looks like this: https://www.example.com [301] [https://www.notinscope.com] []
# The domain www.example.com might still be in-scope, however it redirects to an out-of-scope domain

# Example httpx usage:
#   httpx -list domains.txt -sc -location -o httpx.out

import argparse
from urllib.parse import urlparse

parser = argparse.ArgumentParser()
parser.add_argument('-domain', required=True, help="The root domain")
parser.add_argument('-r', type=int, required=True, help="Index of the redirect locaion")
parser.add_argument('-httpx', required=True, help="Output from httpx")
args = parser.parse_args()

domain = args.domain
httpx = args.httpx
redirect_index = int(args.r) - 1

urls_allowed = []

l = open(httpx).readlines()
out = f = open('httpx-3xx-cleaned.out', "a")

for i in l:
        url = i.split(" ")[0]

        # I'm really sorry for this frankenstein line of code
	# Extracts the redirect location
        redirect_location = i.split("[")[redirect_index].split("]")[0]

        # We don't have to filter for 3xx status codes, because we target the redirect location
        #   the redirect locations of HTTP status codes 2xx, 4xx etc. are empty
        if(len(redirect_location) != 0):
                o = urlparse(redirect_location)

                if(len(o.netloc) == 0):
                        # Domain is empty indicating that it redirects to the same origin but just to another path
                        # For safety reasons we'll be parsing the URL to verify that it's not out-of-scope
                        if(urlparse(url).netloc.endswith("." + domain)):
                                urls_allowed.append(url)
		# The redirect location is another domain, verify that it is still in-scope
                elif(o.netloc.endswith("." + domain)):
                        urls_allowed.append(url)

for i in urls_allowed:
        f.write((i + "\n"))

print("[*] File saved as httpx-3xx-cleaned.out")

out.close()
