#!/usr/bin/env python3

# Removes out-of-scope URLs based on redirects from httpx' output
# A bad redirect looks like this: https://www.example.com [301] [https://www.notinscope.com] []
# The domain www.example.com might still be in-scope, however it redirects to an out-of-scope domain

# Example httpx usage:
#   httpx -list domains.txt -sc -location -o httpx.out

import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-domain', required=True, help="The root domain")
parser.add_argument('-r', type=int, required=True, help="Index of the redirect locaion")
parser.add_argument('-httpx', required=True, help="Output from httpx")
args = parser.parse_args()

domain = args.domain
httpx = args.httpx
redirect_index = int(args.r) - 1

out_of_scope = []
all_urls = []

l = open(httpx).readlines()
out = f = open('httpx-cleaned.out', "a")

for i in l:
	# Save all URLs from the list so that we can remove the out-of-scope ones later on
	url = i.split(" ")[0]
	if(url not in all_urls):
		all_urls.append(url)

	# Lines with a status code
	# We don't have to filter for 30x, because we target the redirect
	#   the redirect of 200, 404 etc. are empty  
	redirect = re.findall(r'\[.*?\]', i)[redirect_index][1:-1]

	# We're only worried about redirects to other webservers
	if((len(redirect) != 0) and (re.search('^https?://', redirect) != None)):

		# Extract the URLs where the root domain is not within the redirect
		if(not re.search(('^https?:\/\/([a-z0-9|-]+\.)*' + re.escape(domain)),redirect)):
			url = i.split(" ")[0]
			out_of_scope.append(url)

# List without the out-of-scope URLs
diff = [x for x in all_urls if x not in out_of_scope]

for i in diff:
	f.write((i + "\n"))

print("[*] File saved as httpx-cleaned.out")

out.close()
