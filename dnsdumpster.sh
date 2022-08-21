# Enumerates subdomains for a given domain via DNSdumpster

host="example.com"
r=$(curl -i -s https://dnsdumpster.com | grep csrf)

csrftoken=$(echo $r | grep "csrftoken" | cut -d "=" -f 2 | cut -d ";" -f 1)
csrfmiddlewaretoken=$(echo $r | cut -d "=" -f 12 | tr -d '">')

subdomains=$(curl -s -X POST -H "Referer: https://dnsdumpster.com/" -H "Cookie: csrftoken=$csrftoken" -d "csrfmiddlewaretoken=$csrfmiddlewaretoken&targetip=$host&user=free" https://dnsdumpster.com | grep "<tr><td class=\"col-md-4\">" | grep $host | grep -Po "(([\w.-]*)\.([\w]*)\.([A-z]))\w+")
echo $subdomains | sed 's/ /\n/g'
