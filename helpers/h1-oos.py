#!/usr/bin/env python3

# Parses HackerOne's Burp configuration file extracting the regex for the out of scope domains

import json

scope_all = []
scope_unique = []

f = open('<HackerOne>.json')
data = json.load(f)
f.close()

f = open("hosts-ignore.txt", "a")

j = data["target"]["scope"]["exclude"]

for i in j:
	scope_all.append(i["host"])

# Remove duplicate entries, since an entry might be listed for both 80 and 443
scope_unique = list(dict.fromkeys(scope_all))

for i in scope_unique:
	f.write((i + "\n"))

f.close()

