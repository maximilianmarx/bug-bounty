#!/usr/bin/env python3

# Parses HackerOne's Burp configuration file extracting the regex for the out of scope domains

import json

f = open('<HackerOne>.json')
data = json.load(f)
f.close()

f = open("oos-regex.txt", "a")

j = data["target"]["scope"]["exclude"]
for i in j:
	f.write((i["host"] + "\n"))

f.close()
