# bug-bounty
Scripts for hunting bugs.

## Subdomain Enumeration
```bash
host="example.com"

# Using crt.sh
curl -s "https://crt.sh/?q=%25.$host&output=json" | jq -r '.[].name_value' | grep -Po "(([\w.-]*)\.([\w]*)\.([A-z]))\w+" | sort -u

# Using RapidDNS (https://github.com/nullt3r/rapiddns)
rapiddns --subdomains $host

# Using AnubisDB
curl -s "https://jldc.me/anubis/subdomains/$host" | grep -Po "((http|https):\/\/)?(([\w.-]*)\.([\w]*)\.([A-z]))\w+" | sort -u

# Using DNSdumpster (somewhat hackerish Bash script I wrote 🥴)
r=$(curl -i -s https://dnsdumpster.com | grep csrf)

csrftoken=$(echo $r | grep "csrftoken" | cut -d "=" -f 2 | cut -d ";" -f 1)

csrfmiddlewaretoken=$(echo $r | cut -d "=" -f 12 | tr -d '">')

subdomains=$(curl -s -X POST -H "Referer: https://dnsdumpster.com/" -H "Cookie: csrftoken=$csrftoken" -d "csrfmiddlewaretoken=$csrfmiddlewaretoken&targetip=$host&user=free" https://dnsdumpster.com | grep "<tr><td class=\"col-md-4\">" | grep $host | grep -Po "(([\w.-]*)\.([\w]*)\.([A-z]))\w+")
echo $subdomains | sed 's/ /\n/g'
```
