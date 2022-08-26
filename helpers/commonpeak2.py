#!/usr/bin/env python3

# Generates a list of subdomains (~485k) using the commonspeak2 wordlist
# https://github.com/assetnote/commonspeak2-wordlists/blob/master/subdomains/subdomains.txt

import os
import sys

if(len(sys.argv) < 2):
        sys.exit("[*] Usage: commonspeak.py <domain>")

domain = str(sys.argv[1])
wordlist = open('/usr/share/wordlists/commonspeak2.txt').read().split('\n')

out = os.path.join(os.getcwd(),"commonspeak2.out")
f = open(out, "a")

for word in wordlist:
        if not word.strip():
                continue
        s = '{}.{}'.format(word.strip(), domain)
        f.write((s + "\n"))

f.close()

print("[*] File written in " + str(out))
