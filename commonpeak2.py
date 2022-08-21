#!/usr/bin/env python3

# Generates a list of subdomains (~485k) using the commonspeak2 wordlist
# https://github.com/assetnote/commonspeak2-wordlists/blob/master/subdomains/subdomains.txt

domain = 'example.com'

wordlist = open('/usr/share/wordlists/commonspeak2.txt').read().split('\n')
f = open("commonspeak2.out", "a")

for word in wordlist:
	if not word.strip():
		continue
	s = '{}.{}'.format(word.strip(), domain)
	f.write((s + "\n"))

wordlist.close()
f.close()
